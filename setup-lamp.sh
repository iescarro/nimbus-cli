#!/bin/bash

echo "🔄 Updating system..."
apt update && apt upgrade -y

echo "🌐 Installing Apache, MySQL, PHP, and essential modules..."
apt install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip

echo "🧩 Installing PHP 8.3 extensions..."
apt install -y php8.3-{mbstring,xml,curl,mysql,zip,gd,sqlite3} sqlite3

echo "🧬 Installing Git..."
apt install -y git

echo "🎼 Installing Composer..."
cd /tmp
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
mv composer.phar /usr/local/bin/composer
php -r "unlink('composer-setup.php');"

echo "✅ All done! LAMP stack and tools installed."
