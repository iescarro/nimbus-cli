#!/bin/bash

# Usage: ./create-subdomain.sh USER DOMAIN SUBDOMAIN
# Example: ./create-subdomain.sh user site subdomain
# Check for required parameters
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Usage: $0 USER DOMAIN SUBDOMAIN"
    exit 1
fi

USER="$1"
DOMAIN="$2"
SUBDOMAIN="$3"
FQDN="$SUBDOMAIN.$DOMAIN"
BASE_DIR="/home/$USER/domains/$DOMAIN/$SUBDOMAIN"
CONF_FILE="/etc/apache2/sites-available/$FQDN.conf"
LOG_NAME=$(echo "${SUBDOMAIN}_${DOMAIN}" | tr '.' '_')

# Create directory structure
mkdir -p "$BASE_DIR"
chown -R "$USER:$USER" "/home/$USER/domains/$DOMAIN"
chmod -R 755 "/home/$USER/domains/$DOMAIN"

# Create Apache config
cat <<EOF | sudo tee "$CONF_FILE" > /dev/null
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot $BASE_DIR
    ServerName $FQDN
    ServerAlias www.$FQDN

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
sudo a2ensite "$FQDN.conf"
sudo systemctl reload apache2

echo "✅ Subdomain setup complete: $FQDN under user $USER"
