import subprocess

class Lamp:

    @staticmethod
    def install():
        print("🔄 Updating system...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)

        print("🛡️ Installing security and system management tools...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'ufw',
            'rsyslog',
            'qemu-guest-agent',
            'fail2ban',
            'unattended-upgrades'
        ], check=True)
        
        php_version = '7.4'
        print(f"➕ Adding PHP {php_version} repository (ppa:ondrej/php)...")
        subprocess.run(['sudo', 'apt', 'install', '-y', 'software-properties-common'], check=True)
        subprocess.run(['sudo', 'add-apt-repository', '-y', f'ppa:ondrej/php'], check=True)
        subprocess.run(['sudo', 'apt', 'update'], check=True)

        print(f"🌐 Installing Apache, MySQL, PHP {php_version}, and essential modules...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'apache2',
            'mysql-server',
            f'php{php_version}',
            f'libapache2-mod-php{php_version}',
            f'php{php_version}-mysql',
            'zip',
            'unzip'
        ], check=True)

        print(f"🧩 Installing PHP {php_version} extensions...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            f'php{php_version}-mbstring',
            f'php{php_version}-xml',
            f'php{php_version}-curl',
            f'php{php_version}-mysql',
            f'php{php_version}-zip',
            f'php{php_version}-gd',
            f'php{php_version}-sqlite3',
            'sqlite3'
        ], check=True)

        # Set PHP as the default CLI version
        print(f"⚙️ Setting PHP {php_version} as default...")
        subprocess.run(['sudo', 'update-alternatives', '--set', 'php', f'/usr/bin/php{php_version}'], check=True)
        
        # Enable PHP for Apache
        print(f"🔧 Enabling PHP {php_version} in Apache...")
        subprocess.run(['sudo', 'a2enmod', f'php{php_version}'], check=True)
        
        # Enable Apache rewrite module
        print("🔄 Enabling Apache rewrite module...")
        subprocess.run(['sudo', 'a2enmod', 'rewrite'], check=True)
        print("✅ Apache rewrite module enabled")

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
        setup_cmd = 'curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -'
        subprocess.run(setup_cmd, shell=True, check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'], check=True)

        print("🔐 Installing Certbot for SSL (Let's Encrypt)...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'certbot',
            'python3-certbot-apache'
        ], check=True)

        # Restart Apache to apply all changes
        print("🔄 Restarting Apache...")
        subprocess.run(['sudo', 'systemctl', 'restart', 'apache2'], check=True)

        print(f"✅ All done! LAMP stack with PHP {php_version}, Python, Certbot, and tools installed.")