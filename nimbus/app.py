import subprocess
import os
import yaml
from pathlib import Path
from .ssh import ssh_connect, run_ssh_command
from os.path import expanduser

import webbrowser

class App:
    @staticmethod
    def deploy(environment='default', app_name='default'):
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
                        "name": "your_db_name",
                        "user": "your_db_user",
                        "password": "your_db_password",
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

def write_nimbus_index(base_dir):
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome to Nimbus</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            color: #333;
            text-align: center;
            padding-top: 100px;
        }
        .box {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: inline-block;
            padding: 40px;
            max-width: 500px;
        }
        h1 {
            color: #0057ff;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🚀 Nimbus is Ready!</h1>
        <p>Your server is up and running.</p>
        <p>Place your website files here in <code>public_html</code>.</p>
    </div>
</body>
</html>
"""
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "w") as f:
        f.write(index_html.strip())