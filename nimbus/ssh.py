from os.path import expanduser
from paramiko import SSHClient, AutoAddPolicy

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
        print(f"⚠️ Error: {error}")
    return output