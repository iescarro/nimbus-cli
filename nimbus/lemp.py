import subprocess

class Lemp:

    @staticmethod
    def install():
        print("🔄 Updating system...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)
        
        print("➕ Adding PHP 8.3 repository (ppa:ondrej/php)...")
        subprocess.run(['sudo', 'apt', 'install', '-y', 'software-properties-common'], check=True)
        subprocess.run(['sudo', 'add-apt-repository', '-y', 'ppa:ondrej/php'], check=True)
        subprocess.run(['sudo', 'apt', 'update'], check=True)

        print("🌐 Installing Nginx, MySQL, PHP 8.3, and essential modules...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'nginx',
            'mysql-server',
            'php8.3-fpm',
            'php8.3-mysql',  # Note: php8.3-fpm instead of libapache2-mod-php8.3
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
        
        # Start and enable Nginx
        print("🚀 Starting and enabling Nginx...")
        subprocess.run(['sudo', 'systemctl', 'start', 'nginx'], check=True)
        subprocess.run(['sudo', 'systemctl', 'enable', 'nginx'], check=True)
        
        # Start and enable PHP-FPM
        print("🚀 Starting and enabling PHP-FPM...")
        subprocess.run(['sudo', 'systemctl', 'start', 'php8.3-fpm'], check=True)
        subprocess.run(['sudo', 'systemctl', 'enable', 'php8.3-fpm'], check=True)

        # Configure PHP-FPM for better performance
        print("⚙️ Optimizing PHP-FPM configuration...")
        subprocess.run(['sudo', 'sed', '-i', 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/', '/etc/php/8.3/fpm/php.ini'], check=True)
        
        # Restart PHP-FPM to apply changes
        subprocess.run(['sudo', 'systemctl', 'restart', 'php8.3-fpm'], check=True)

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
            'sudo', 'apt', 'install', '-y', 'certbot', 'python3-certbot-nginx'  # Note: certbot-nginx instead of apache
        ], check=True)

        # Create a default Nginx server block for PHP
        print("📝 Creating default Nginx server block for PHP...")
        nginx_config = """
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        
        root /var/www/html;
        index index.php index.html index.htm;
        
        server_name _;
        
        location / {
            try_files $uri $uri/ =404;
        }
        
        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        }
        
        location ~ /\.ht {
            deny all;
        }
    }
    """
        
        # Write the config to file
        with open('/tmp/nginx-default', 'w') as f:
            f.write(nginx_config)
        
        subprocess.run(['sudo', 'mv', '/tmp/nginx-default', '/etc/nginx/sites-available/default'], check=True)
        
        # Test Nginx configuration
        print("🔍 Testing Nginx configuration...")
        subprocess.run(['sudo', 'nginx', '-t'], check=True)
        
        # Restart Nginx to apply changes
        print("🔄 Restarting Nginx...")
        subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'], check=True)

        # Create a test PHP file
        # print("📄 Creating test PHP file...")
        # php_info = "<?php phpinfo(); ?>"
        # with open('/tmp/info.php', 'w') as f:
        #     f.write(php_info)
        # subprocess.run(['sudo', 'mv', '/tmp/info.php', '/var/www/html/info.php'], check=True)

        print("✅ All done! LEMP stack with PHP 8.3, Python, Certbot, and tools installed.")
        # print("🌐 Test PHP at: http://YOUR_SERVER_IP/info.php")
        # print("ℹ️  Remember to delete info.php after testing for security!")