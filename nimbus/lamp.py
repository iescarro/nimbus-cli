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
        
        print("➕ Adding PHP 8.3 repository (ppa:ondrej/php)...")
        subprocess.run(['sudo', 'apt', 'install', '-y', 'software-properties-common'], check=True)
        subprocess.run(['sudo', 'add-apt-repository', '-y', 'ppa:ondrej/php'], check=True)
        subprocess.run(['sudo', 'apt', 'update'], check=True)

        print("🌐 Installing Apache, MySQL, PHP 8.3, and essential modules...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'apache2',
            'mysql-server',
            'php8.3',
            'libapache2-mod-php8.3',
            'php8.3-mysql',
            'zip',
            'unzip'
        ], check=True)

        print("🧩 Installing PHP 8.3 extensions...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'php8.3-mbstring',
            'php8.3-xml',
            'php8.3-curl',
            'php8.3-mysql',
            'php8.3-zip',
            'php8.3-gd',
            'php8.3-sqlite3',
            'sqlite3'
        ], check=True)

        # Set PHP 8.3 as the default CLI version
        print("⚙️ Setting PHP 8.3 as default...")
        subprocess.run(['sudo', 'update-alternatives', '--set', 'php', '/usr/bin/php8.3'], check=True)
        
        # Enable PHP 8.3 for Apache
        print("🔧 Enabling PHP 8.3 in Apache...")
        subprocess.run(['sudo', 'a2enmod', 'php8.3'], check=True)
        
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

        print("✅ All done! LAMP stack with PHP 8.3, Python, Certbot, and tools installed.")