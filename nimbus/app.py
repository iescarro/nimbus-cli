import subprocess

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