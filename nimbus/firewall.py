import subprocess

class Firewall:
    
    @staticmethod
    def setup():
        print("🔄 Setting up firewall...")
        subprocess.run(['sudo', 'ufw', 'default', 'deny', 'incoming'], check=True)
        subprocess.run(['sudo', 'ufw', 'default', 'allow', 'outgoing'], check=True)
        subprocess.run(['sudo', 'ufw', 'allow', 'ssh'], check=True)
        subprocess.run(['sudo', 'ufw', 'allow', 'http'], check=True)
        subprocess.run(['sudo', 'ufw', 'allow', 'https'], check=True)
        subprocess.run(['sudo', 'ufw', 'enable'], check=True)
        subprocess.run(['sudo', 'ufw', 'status', 'verbose'], check=True)
        print("✅ Firewall setup complete!")