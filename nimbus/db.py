import yaml
import os
import paramiko
from scp import SCPClient
from os.path import expanduser
from paramiko import SSHClient, AutoAddPolicy

import subprocess
import sys

class DB:
    @staticmethod
    def create_database(db_name, db_user, db_password):
        print(f"📦 Creating MySQL database '{db_name}' and user '{db_user}'...")

        sql = f"""
        CREATE DATABASE IF NOT EXISTS `{db_name}`;
        CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';
        GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'localhost';
        FLUSH PRIVILEGES;
        """

        try:
            subprocess.run(['sudo', 'mysql', '-u', 'root', '-e', sql], check=True)
            print(f"✅ Database '{db_name}' and user '{db_user}' created successfully.")
        except subprocess.CalledProcessError:
            print("❌ Failed to create database or user.")
            sys.exit(1)

    def ssh_connect(self, key_path, host, port, user):
        # print(f"$ ssh -i {key_path} -p {port} {user}@{host}")
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            hostname=host,
            port=port,
            username=user,
            key_filename=expanduser(key_path)
        )
        return client

    def run_ssh_command(self, client, command):
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print(f"⚠️  Error:\n{error}")
        return output

    def create_backup(self, client, db_user, db_password, db_name):
        print("📦 Creating MySQL dump and zipping it...")
        dump_cmd = f"mysqldump -u {db_user} -p'{db_password}' {db_name} > {db_name}.sql && zip {db_name}.zip {db_name}.sql"
        # print(f"Running command: {dump_cmd}")
        return self.run_ssh_command(client, dump_cmd)

    def transfer_file_from_source(self, source_client, remote_path, local_path):
        print("📥 Downloading backup file to local machine...")
        with SCPClient(source_client.get_transport()) as scp:
            scp.get(remote_path, local_path)

    def transfer_file_to_dest(self, dest_client, local_path, remote_path):
        print("📤 Uploading backup file to destination server...")
        with SCPClient(dest_client.get_transport()) as scp:
            scp.put(local_path, remote_path)

    def restore_backup(self, client, db_user, db_password, db_name, zip_filename, sql_filename):
        print("🛠️  Restoring database on destination server...")
        unzip_cmd = f"unzip -o {zip_filename}"
        restore_cmd = f"mysql -u {db_user} -p'{db_password}' {db_name} < {sql_filename}"
        self.run_ssh_command(client, unzip_cmd)
        self.run_ssh_command(client, restore_cmd)

def main():
    with open("db.yml", "r") as f:
        config = yaml.safe_load(f)["db"]

    src = config["source"]
    dest = config["destination"]
    zip_filename = f"{src['db_name']}.zip"
    sql_filename = f"{src['db_name']}.sql"

    db = DB()

    # Step 1: Connect to source server
    print("🔌 Connecting to source server...")
    src_client = db.ssh_connect(src["ssh_key"], src["host"], src["port"], src["user"])
    db.create_backup(src_client, src["db_user"], src["db_password"], src["db_name"])

    # Step 2: Download to local
    db.transfer_file_from_source(src_client, f"{src['db_name']}.zip", f"./{zip_filename}")
    src_client.close()

    # # Step 3: Upload to destination
    print("🔌 Connecting to destination server...")
    dest_client = db.ssh_connect(dest["ssh_key"], dest["host"], dest["port"], dest["user"])
    db.transfer_file_to_dest(dest_client, f"./{zip_filename}", f"./{zip_filename}")

    # # Step 4: Restore
    db.restore_backup(dest_client, dest["db_user"], dest["db_password"], dest["db_name"], zip_filename, sql_filename)
    dest_client.close()

    print("✅ Backup and restore complete.")

if __name__ == "__main__":
    main()
