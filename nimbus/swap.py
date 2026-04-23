class Swap:

    def __init__(self):
        pass

    def off(self):
        import subprocess
        
        commands = [
            "sudo swapoff -a",
            "free -h",
            "sudo rm /swapfile",
            "ls -la /swapfile"
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                print(f"Command: {cmd}")
                print(f"Output: {result.stdout}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
            except Exception as e:
                print(f"Failed to execute {cmd}: {e}")

    def on(self, size = "2G"):
        import subprocess
        
        commands = [
            f"sudo fallocate -l {size} /swapfile",
            "sudo chmod 600 /swapfile",
            "sudo mkswap /swapfile",
            "sudo swapon /swapfile",
            "free -h",
            "echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab"
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                print(f"Command: {cmd}")
                print(f"Output: {result.stdout}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
            except Exception as e:
                print(f"Failed to execute {cmd}: {e}")
                