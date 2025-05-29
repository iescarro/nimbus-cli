#!/bin/bash

# Usage: ./create-site.sh USER DOMAIN
# Example: ./create-site.sh nebulom bagdok.online

# Check for required parameters
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 USER DOMAIN"
    exit 1
fi

USER="$1"
DOMAIN="$2"
BASE_DIR="/home/$USER/domains/$DOMAIN/public_html"
CONF_FILE="/etc/apache2/sites-available/$DOMAIN.conf"
LOG_NAME=$(echo "$DOMAIN" | tr '.' '_')

# Create directory structure
mkdir -p "$BASE_DIR"
chown -R "$USER:$USER" "/home/$USER/domains/$DOMAIN"
chmod -R 755 "/home/$USER/domains/$DOMAIN"

# Create Apache config
cat <<EOF | sudo tee "$CONF_FILE" > /dev/null
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot $BASE_DIR
    ServerName $DOMAIN
    ServerAlias www.$DOMAIN

    <Directory $BASE_DIR>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/${LOG_NAME}_error.log
    CustomLog \${APACHE_LOG_DIR}/${LOG_NAME}_access.log combined
</VirtualHost>
EOF

# Enable the site and reload Apache
sudo a2ensite "$DOMAIN.conf"
sudo systemctl reload apache2

echo "✅ Site setup complete for $DOMAIN under user $USER"
