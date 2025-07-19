#!/usr/bin/env python3

import os
import sys
import subprocess
import pwd
import time

from .__version__ import __version__

def say_hello():
    print("👋 Hello, friend!")

def install_lamp_stack():
    print("🔄 Updating system...")
    subprocess.run(['sudo', 'apt', 'update'], check=True)
    subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)

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

    print("🔐 Installing Certbot for SSL (Let's Encrypt)...")
    subprocess.run([
        'sudo', 'apt', 'install', '-y', 'certbot', 'python3-certbot-apache'
    ], check=True)

    print("✅ All done! LAMP stack, Python, Certbot, and tools installed.")

def enable_ssl(domain):
    print(f"🔐 Enabling SSL for {domain} using Certbot...")
    try:
        subprocess.run(['sudo', 'certbot', '--apache', '-d', domain], check=True)
        print(f"✅ SSL enabled for {domain}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to enable SSL for {domain}. Please check your DNS and Apache config.")

def wait_for_user(username, timeout=5):
    """Wait for user to be registered in the system."""
    for _ in range(timeout * 10):  # check every 0.1s for up to `timeout` seconds
        try:
            pwd.getpwnam(username)
            return True
        except KeyError:
            time.sleep(0.1)
    return False

def create_user(username, domain):
    user_home = f"/home/{username}"
    web_dir = f"/home/{username}/domains/{domain}/public_html"

    try:
        pwd.getpwnam(username)
        print(f"⚠️ User '{username}' already exists. Skipping user creation.")
    except KeyError:
        subprocess.run(['sudo', 'adduser', '--disabled-password', '--gecos', '', username], check=True)
        print(f"✅ User '{username}' created.")

        # Wait a moment to allow system to register the user
        if not wait_for_user(username, 10):
            print(f"❌ Timeout: user '{username}' was not registered properly.")
            return

        # Create the web directory as root
        subprocess.run(['sudo', 'mkdir', '-p', web_dir], check=True)
        write_nimbus_index(web_dir)

        subprocess.run(['sudo', 'chown', '-R', f"{username}:{username}", user_home], check=True)
        subprocess.run(['sudo', 'chmod', '-R', '755', user_home], check=True)

        print(f"✅ User '{username}' ready. Web directory: {web_dir}")

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
        <p>Your LAMP server is up and running.</p>
        <p>Place your website files here in <code>public_html</code>.</p>
    </div>
</body>
</html>
"""
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "w") as f:
        f.write(index_html.strip())

def create_site(username, domain):
    base_dir = f"/home/{username}/domains/{domain}/public_html"
    conf_file = f"/etc/apache2/sites-available/{domain}.conf"
    log_name = domain.replace('.', '_')

    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
    write_nimbus_index(base_dir)

    subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', f'/home/{username}/domains/{domain}'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', f'/home/{username}/domains/{domain}'], check=True)

    # Apache config content
    apache_config = f"""
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot {base_dir}
    ServerName {domain}
    ServerAlias www.{domain}

    <Directory {base_dir}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${{APACHE_LOG_DIR}}/{log_name}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{log_name}_access.log combined
</VirtualHost>
"""

    # Write config file
    with open('/tmp/apache_temp.conf', 'w') as temp_conf:
        temp_conf.write(apache_config.strip())

    subprocess.run(['sudo', 'mv', '/tmp/apache_temp.conf', conf_file], check=True)
    subprocess.run(['sudo', 'a2ensite', f'{domain}.conf'], check=True)
    subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'], check=True)

    print(f"✅ Site setup complete for {domain} under user {username}")

def create_subdomain(username, domain, subdomain):
    fqdn = f"{subdomain}.{domain}"
    base_dir = f"/home/{username}/domains/{domain}/{subdomain}"
    conf_file = f"/etc/apache2/sites-available/{fqdn}.conf"
    log_name = f"{subdomain}_{domain}".replace('.', '_')

    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
    write_nimbus_index(base_dir)

    subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', f'/home/{username}/domains/{domain}'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', f'/home/{username}/domains/{domain}'], check=True)

    # Apache config content
    apache_config = f"""
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot {base_dir}
    ServerName {fqdn}

    <Directory {base_dir}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${{APACHE_LOG_DIR}}/{log_name}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{log_name}_access.log combined
</VirtualHost>
"""

    # Write Apache config to file
    with open('/tmp/apache_sub_temp.conf', 'w') as temp_conf:
        temp_conf.write(apache_config.strip())

    subprocess.run(['sudo', 'mv', '/tmp/apache_sub_temp.conf', conf_file], check=True)
    subprocess.run(['sudo', 'a2ensite', f'{fqdn}.conf'], check=True)
    subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'], check=True)

    print(f"✅ Subdomain setup complete: {fqdn} under user {username}")

def print_usage():
    print("""📦 Nimbus CLI — LAMP site manager
Usage:
  nimbus <command> [options]

Available Commands:
  hello                                   Greet the user
  install-lamp                            Install Apache, MySQL, PHP, Python, Composer, Certbot
  create-user <user> <domain>             Create a Linux user and web directory
  create-site <user> <domain>             Set up Apache site config and public_html
  create-subdomain <user> <domain> <sub>  Create subdomain site under user
  create-database <name> <user> <pass>    Create MySQL DB and user
  enable-ssl <domain>                     Enable SSL using Certbot (Let's Encrypt)

Other Options:
  -v, --version                             Show current version

Example:
  nimbus create-user alice example.com
""")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Handle --version or -v globally
    if sys.argv[1] in ["--version", "-v"]:
        print(f"nimbus-cli version {__version__}")
        sys.exit(0)

    command = sys.argv[1]

    if command == "hello":
        say_hello()
    elif command == "install-lamp":
        install_lamp_stack()
    elif command == "create-user":
        if len(sys.argv) != 4:
            print("Usage: nimbus.py create-user <username> <domain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        create_user(username, domain)
    elif command == "create-database":
        if len(sys.argv) != 5:
            print("Usage: nimbus create-database <db_name> <db_user> <db_password>")
            sys.exit(1)
        db_name = sys.argv[2]
        db_user = sys.argv[3]
        db_password = sys.argv[4]
        create_database(db_name, db_user, db_password)
    elif command == "create-site":
        if len(sys.argv) != 4:
            print("Usage: nimbus create-site <username> <domain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        create_site(username, domain)
    elif command == "create-subdomain":
        if len(sys.argv) != 5:
            print("Usage: nimbus create-subdomain <username> <domain> <subdomain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        subdomain = sys.argv[4]
        create_subdomain(username, domain, subdomain)
    elif command == "enable-ssl":
        if len(sys.argv) != 3:
            print("Usage: nimbus enable-ssl <domain>")
            sys.exit(1)
        domain = sys.argv[2]
        enable_ssl(domain)
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
