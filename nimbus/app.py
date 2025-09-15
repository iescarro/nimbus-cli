import subprocess
import yaml
from pathlib import Path
from .ssh import ssh_connect, run_ssh_command
from os.path import expanduser

import webbrowser

def deploy_app(environment='default', app_name='default'):
    """Deploy the specified app using a single SSH command"""
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
        ssh_config = env_config['ssh']
        
        ssh_cmd = [
            'ssh',
            '-i', expanduser(ssh_config['ssh_key']),
            '-p', str(ssh_config['port']),
            f"{ssh_config['user']}@{env_config['host']}",
            '-t'  # Force pseudo-terminal allocation
        ]
        
        combined_tasks = ' && '.join(app_config['tasks'])
        
        ssh_cmd.append(f'"{combined_tasks}"')
        
        print(f"🚀 Executing deployment for {app_name} on {environment}:")
        print(' '.join(ssh_cmd))
        
        result = subprocess.run(
            ' '.join(ssh_cmd),
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"⚠️ Errors:\n{result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ Successfully deployed {app_name} on {environment}")
            return True
        else:
            print(f"❌ Deployment failed (exit code: {result.returncode})")
            return False            
    except FileNotFoundError:
        print(f"❌ Config file not found at: {config_path.absolute()}")
    except yaml.YAMLError:
        print("❌ Invalid YAML format in config file")
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")    
    return False

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
                "host": "your_host.com",
                "ssh": {
                    "port": 22,
                    "user": "your_ssh_user",
                    "ssh_key": "~/.ssh/id_rsa"
                },
                "apps": {
                    "default": {
                        "name": "your_app",
                        "subdomain": "your_app.your_host.com",
                        "github": "your_token@github.com/your_name/your_repo.git",
                        "branch": "develop",
                        "tasks": [
                            "cd domains/your_domain/your_app",
                            "git pull origin develop",
                            "composer install",
                            "php index.php migrate"
                        ],
                    }
                },
                "databases": {
                    "default": {
                        "user": "your_db_user",
                        "password": "your_db_password",
                        "name": "your_db_name"
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

    print("🌐 Installing Apache, MySQL, PHP 8.3, and essential modules...")
    subprocess.run([
        'sudo', 'apt', 'install', '-y',
        'apache2', 'mysql-server', 'php8.3', 'libapache2-mod-php8.3', 'php8.3-mysql', 'unzip'  # Changed to php8.3 specific
    ], check=True)

    print("🧩 Installing PHP 8.3 extensions...")
    subprocess.run([
        'sudo', 'apt', 'install', '-y',
        'php8.3-mbstring', 'php8.3-xml', 'php8.3-curl', 'php8.3-mysql',
        'php8.3-zip', 'php8.3-gd', 'php8.3-sqlite3', 'sqlite3'
    ], check=True)

    # Set PHP 8.3 as the default CLI version
    print("⚙️ Setting PHP 8.3 as default...")
    subprocess.run(['sudo', 'update-alternatives', '--set', 'php', '/usr/bin/php8.3'], check=True)
    
    # Enable PHP 8.3 for Apache
    print("🔧 Enabling PHP 8.3 in Apache...")
    subprocess.run(['sudo', 'a2enmod', 'php8.3'], check=True)

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

    # Restart Apache to apply PHP changes
    print("🔄 Restarting Apache...")
    subprocess.run(['sudo', 'systemctl', 'restart', 'apache2'], check=True)

    print("✅ All done! LAMP stack with PHP 8.3, Python, Certbot, and tools installed.")