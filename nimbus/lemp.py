import subprocess

class Lemp:

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
        
        php_version = "8.3"
        print(f"➕ Adding PHP {php_version} repository (ppa:ondrej/php)...")
        subprocess.run(['sudo', 'apt', 'install', '-y', 'software-properties-common'], check=True)
        subprocess.run(['sudo', 'add-apt-repository', '-y', f'ppa:ondrej/php'], check=True)
        subprocess.run(['sudo', 'apt', 'update'], check=True)

        print(f"🌐 Installing Nginx, MySQL, PHP {php_version}, and essential modules...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'nginx',
            'mysql-server',
            f'php{php_version}-fpm',
            f'php{php_version}-mysql',  # Note: php{php_version}-fpm instead of libapache2-mod-php{php_version}
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
        
        # Start and enable Nginx
        print("🚀 Starting and enabling Nginx...")
        subprocess.run(['sudo', 'systemctl', 'start', 'nginx'], check=True)
        subprocess.run(['sudo', 'systemctl', 'enable', 'nginx'], check=True)
        
        # Start and enable PHP-FPM
        print("🚀 Starting and enabling PHP-FPM...")
        subprocess.run(['sudo', 'systemctl', 'start', f'php{php_version}-fpm'], check=True)
        subprocess.run(['sudo', 'systemctl', 'enable', f'php{php_version}-fpm'], check=True)

        # Configure PHP-FPM for better performance
        print("⚙️ Optimizing PHP-FPM configuration...")
        subprocess.run(['sudo', 'sed', '-i', f's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/', f'/etc/php/{php_version}/fpm/php.ini'], check=True)
        
        # Restart PHP-FPM to apply changes
        subprocess.run(['sudo', 'systemctl', 'restart', f'php{php_version}-fpm'], check=True)

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
            'python3-certbot-nginx'
        ], check=True)

        # Create a default Nginx server block for PHP
        print("📝 Creating default Nginx server block for PHP...")
        nginx_config = f"""
server {{
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.php index.html index.htm;
    
    server_name _;
    
    location / {{
        try_files $uri $uri/ =404;
    }}
    
    location ~ \.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php{php_version}-fpm.sock;
    }}
    
    location ~ /\.ht {{
        deny all;
    }}
}}
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

        print(f"✅ All done! LEMP stack with PHP {php_version}, Python, Certbot, and tools installed.")
        # print("🌐 Test PHP at: http://YOUR_SERVER_IP/info.php")
        # print("ℹ️  Remember to delete info.php after testing for security!")