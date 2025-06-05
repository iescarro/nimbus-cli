#!/usr/bin/env python3

import os
import sys
import subprocess

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

    print("✅ All done! LAMP stack, Python, and tools installed.")

def create_user(username, domain):
    user_home = f"/home/{username}"
    web_dir = os.path.join(user_home, f"domains/{domain}/public_html")

    # Create user
    subprocess.run(['sudo', 'adduser', '--disabled-password', '--gecos', '', username], check=True)

    # Create web directory
    os.makedirs(web_dir, exist_ok=True)

    # Set permissions
    subprocess.run(['sudo', 'chown', '-R', f"{username}:{username}", user_home], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', user_home], check=True)

    print(f"✅ User '{username}' created and web directory '{web_dir}' is ready.")
    
def create_site(username, domain):
    base_dir = f"/home/{username}/domains/{domain}/public_html"
    conf_file = f"/etc/apache2/sites-available/{domain}.conf"
    log_name = domain.replace('.', '_')

    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
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
    subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', f'/home/{username}/domains/{domain}'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', f'/home/{username}/domains/{domain}'], check=True)

    # Apache config content
    apache_config = f"""
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot {base_dir}
    ServerName {fqdn}
    ServerAlias www.{fqdn}

    <Directory {base_dir}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${{{{APACHE_LOG_DIR}}}}/{log_name}_error.log
    CustomLog ${{{{APACHE_LOG_DIR}}}}/{log_name}_access.log combined
</VirtualHost>
"""

    # Write Apache config to file
    with open('/tmp/apache_sub_temp.conf', 'w') as temp_conf:
        temp_conf.write(apache_config.strip())

    subprocess.run(['sudo', 'mv', '/tmp/apache_sub_temp.conf', conf_file], check=True)
    subprocess.run(['sudo', 'a2ensite', f'{fqdn}.conf'], check=True)
    subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'], check=True)

    print(f"✅ Subdomain setup complete: {fqdn} under user {username}")

def main():
    if len(sys.argv) < 2:
        print("Usage: nimbus.py <command> [args]")
        sys.exit(1)

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
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
