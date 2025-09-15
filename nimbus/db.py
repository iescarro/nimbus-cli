import yaml
import os
import paramiko
from scp import SCPClient
from os.path import expanduser
from paramiko import SSHClient, AutoAddPolicy
from .ssh import ssh_connect, run_ssh_command

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

    def create_backup(self, client, db_user, db_password, db_name):
        print("📦 Creating MySQL dump and zipping it...")
        dump_cmd = f"mysqldump -u {db_user} -p'{db_password}' {db_name} > {db_name}.sql && zip {db_name}.zip {db_name}.sql"
        # print(f"Running command: {dump_cmd}")
        return run_ssh_command(client, dump_cmd)

    def transfer_file_from_source(self, source_client, remote_path, local_path):
        print("📥 Downloading backup file to local machine...")
        with SCPClient(source_client.get_transport()) as scp:
            scp.get(remote_path, local_path)

    def transfer_file_to_dest(self, dest_client, local_path, remote_path):
        print("📤 Uploading backup file to destination server...")
        with SCPClient(dest_client.get_transport()) as scp:
            scp.put(local_path, remote_path)

    def restore_backup(self, client, db_user, db_password, db_name, zip_filename, sql_filename):
        print("🛠️ Restoring database on destination server...")
        unzip_cmd = f"unzip -o {zip_filename}"
        restore_cmd = f"mysql -u {db_user} -p'{db_password}' {db_name} < {sql_filename}"
        run_ssh_command(client, unzip_cmd)
        run_ssh_command(client, restore_cmd)

    @staticmethod
    def migrate(source, target):
        with open("nimbus.yaml", "r") as f:
            config = yaml.safe_load(f)["environments"]  
               
        # Parse source and target
        src_app, src_db_name = source.split(':')
        dst_app, dest_db_name = target.split(':')
        
        # Get configurations
        src = config[src_app]
        dest = config[dst_app]

        src_db = src["databases"][src_db_name]
        zip_filename = f"{src_db['name']}.zip"
        sql_filename = f"{src_db['name']}.sql"

        db = DB()

        # Step 1: Connect to source server
        print("🔌 Connecting to source server...")
        src_client = ssh_connect(src["ssh"]["ssh_key"], src["host"], src["ssh"]["port"], src["ssh"]["user"])
        db.create_backup(src_client, src_db["user"], src_db["password"], src_db["name"])

        # Step 2: Download to local
        db.transfer_file_from_source(src_client, f"{src_db['name']}.zip", f"./{zip_filename}")
        src_client.close()

        # # Step 3: Upload to destination
        print("🔌 Connecting to destination server...")
        dest_client = ssh_connect(dest["ssh"]["ssh_key"], dest["host"], dest["ssh"]["port"], dest["ssh"]["user"])
        db.transfer_file_to_dest(dest_client, f"./{zip_filename}", f"./{zip_filename}")

        # # Step 4: Restore
        dest_db = dest["databases"][dest_db_name]
        db.restore_backup(dest_client, dest_db["user"], dest_db["password"], dest_db["name"], zip_filename, sql_filename)
        dest_client.close()

        print("✅ Backup and restore complete.")

    @staticmethod
    def backup(source):
        with open("nimbus.yaml", "r") as f:
            config = yaml.safe_load(f)["environments"]  
               
        # Parse source and target
        src_app, src_db_name = source.split(':')
        
        # Get configurations
        src = config[src_app]

        src_db = src["databases"][src_db_name]
        zip_filename = f"{src_db['name']}.zip"

        db = DB()

        # Step 1: Connect to source server
        print("🔌 Connecting to source server...")
        src_client = ssh_connect(src["ssh"]["ssh_key"], src["host"], src["ssh"]["port"], src["ssh"]["user"])
        db.create_backup(src_client, src_db["user"], src_db["password"], src_db["name"])

        # Step 2: Download to local
        db.transfer_file_from_source(src_client, f"{src_db['name']}.zip", f"./{zip_filename}")
        src_client.close()

        print("✅ Backup complete.")

    @staticmethod
    def restore(target, dest_db_filename = None):
        with open("nimbus.yaml", "r") as f:
            config = yaml.safe_load(f)["environments"]  
               
        # Parse source and target
        dst_app, dest_db_name = target.split(':')
        
        # Get configurations
        dest = config[dst_app]
        dest_db = dest["databases"][dest_db_name]

        # Use dest_db_filename if provided, otherwise use dest_db['name']
        base_filename = dest_db_filename if dest_db_filename is not None else dest_db['name']

        zip_filename = f"{base_filename}.zip"
        sql_filename = f"{base_filename}.sql"

        db = DB()

        # # Step 3: Upload to destination
        print("🔌 Connecting to destination server...")
        dest_client = ssh_connect(dest["ssh"]["ssh_key"], dest["host"], dest["ssh"]["port"], dest["ssh"]["user"])
        db.transfer_file_to_dest(dest_client, f"./{zip_filename}", f"./{zip_filename}")

        # # Step 4: Restore
        dest_db = dest["databases"][dest_db_name]
        db.restore_backup(dest_client, dest_db["user"], dest_db["password"], dest_db["name"], zip_filename, sql_filename)
        dest_client.close()

        print("✅ Backup and restore complete.")