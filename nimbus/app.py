import subprocess
import yaml
from pathlib import Path

import webbrowser

def open_app(environment='default', app_name='default'):
    """Open the default app's URL in the default web browser"""
    config_path = Path("nimbus.yaml")
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if environment not in config['environments']:
            available = ", ".join(config['environments'].keys())
            print(f"❌ Environment '{environment}' not found. Available: {available}")
            return False
            
        env_config = config['environments'][environment]
        
        if 'apps' not in env_config or app_name not in env_config['apps']:
            available = ", ".join(env_config['apps'].keys()) if 'apps' in env_config else "none"
            print(f"❌ App '{app_name}' not found in '{environment}'. Available: {available}")
            return False
            
        app_config = env_config['apps'][app_name]
        app_url = f"https://{app_config['name']}"
        
        print(f"🌐 Opening {app_url} in your browser...")
        webbrowser.open_new_tab(app_url)
        return True        
    except FileNotFoundError:
        print(f"❌ Config file not found at: {config_path.absolute()}")
    except KeyError as e:
        print(f"❌ Missing required config key: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")    
    return False

def init():
    config = {
        "environments": {
            "default": {
                "host": "your-host.com",
                "ssh": {
                    "port": 22,
                    "user": "your-ssh-user",
                    "ssh_key": "~/.ssh/id_rsa"
                },
                "apps": {
                    "default": {
                        "name": "default-app",
                        "subdomain": "default.your-host.com",
                        "github": ""
                    }
                },
                "databases": {
                    "default": {
                        "user": "your-db-user",
                        "password": "your-db-password",
                        "name": "your-db-name"
                    }
                }
            }
        }
    }

    # Create the file
    config_path = Path("nimbus.yaml")
    with open(config_path, 'w') as f:
        yaml.dump(config, f, sort_keys=False, default_flow_style=False)
    
    print(f"✅ Config file created at: {config_path.absolute()}")

def install_lamp_stack():
    print("🔄 Updating system...")
    subprocess.run(['sudo', 'apt', 'update'], check=True)
    subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)
    
    print("➕ Adding PHP 8.3 repository (ppa:ondrej/php)...")
    subprocess.run(['sudo', 'apt', 'install', '-y', 'software-properties-common'], check=True)
    subprocess.run(['sudo', 'add-apt-repository', '-y', 'ppa:ondrej/php'], check=True)
    subprocess.run(['sudo', 'apt', 'update'], check=True)

    print("🌐 Installing Apache, MySQL, PHP, and essential modules...")
    subprocess.run([
        'sudo', 'apt', 'install', '-y',
        'apache2', 'mysql-server', 'php', 'libapache2-mod-php', 'php-mysql', 'unzip'
    ], check=True)

    print("🧩 Installing PHP 8.3 extensions...")
    subprocess.run([
        'sudo', 'apt', 'install', '-y',
        'php8.3-mbstring', 'php8.3-xml', 'php8.3-curl', 'php8.3-mysql',
        'php8.3-zip', 'php8.3-gd', 'php8.3-sqlite3', 'sqlite3'
    ], check=True)

    print("🧬 Installing Git...")
    subprocess.run(['sudo', 'apt', 'install', '-y', 'git'], check=True)

    print("🐍 Installing Python 3 and pip...")
    subprocess.run(['sudo', 'apt', 'install', '-y', 'python3', 'python3-pip'], check=True)

    print("🎼 Installing Composer...")
    subprocess.run(['cd', '/tmp'], shell=True)
    subprocess.run(['php', '-r', "copy('https://getcomposer.org/installer', 'composer-setup.php');"], check=True)
    subprocess.run(['php', 'composer-setup.php'], check=True)
    subprocess.run(['sudo', 'mv', 'composer.phar', '/usr/local/bin/composer'], check=True)
    subprocess.run(['php', '-r', "unlink('composer-setup.php');"], check=True)

    print("📦 Installing Node.js (LTS) and npm...")
    subprocess.run('curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -', shell=True, check=True)
    subprocess.run(['sudo', 'apt', 'install', '-y', 'nodejs'], check=True)

    print("🔐 Installing Certbot for SSL (Let's Encrypt)...")
    subprocess.run([
        'sudo', 'apt', 'install', '-y', 'certbot', 'python3-certbot-apache'
    ], check=True)

    print("✅ All done! LAMP stack, Python, Certbot, and tools installed.")