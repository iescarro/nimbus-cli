#!/bin/bash

# Usage: ./create-subdomain.sh USER subdomain.domain.com IP_ADDRESS [DOCUMENT_ROOT]

$USER=$1
SUBDOMAIN=$2
IP=$3
DOCROOT=$4

if [ -z "$SUBDOMAIN" ] || [ -z "$IP" ]; then
  echo "Usage: $0 subdomain.domain.com IP_ADDRESS [DOCUMENT_ROOT]"
  exit 1
fi

# Extract short domain (e.g. pustahe from pustahe.net)
DOMAIN_NAME=$(echo "$SUBDOMAIN" | cut -d'.' -f2,3)

# Default document root if not provided
if [ -z "$DOCROOT" ]; then
  DOCROOT="/home/$USER/domains/$SUBDOMAIN/public_html"
fi

# Create directories if they don't exist
mkdir -p "$DOCROOT"

# Set permissions
chown -R "$USER":"$USER" "/home/$USER/domains"
chmod -R 755 "/home/$USER/domains"

# Apache config
CONF_FILE="/etc/apache2/sites-available/$SUBDOMAIN.conf"

cat <<EOF | sudo tee "$CONF_FILE" > /dev/null
<VirtualHost $IP:80>
    ServerAdmin webmaster@$DOMAIN_NAME
    DocumentRoot $DOCROOT
    ServerName $SUBDOMAIN
    ServerAlias www.$SUBDOMAIN

    <Directory $DOCROOT>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/${SUBDOMAIN}_error.log
    CustomLog \${APACHE_LOG_DIR}/${SUBDOMAIN}_access.log combined
</VirtualHost>
EOF

# Enable site & mod_rewrite, then restart Apache
sudo a2ensite "$SUBDOMAIN.conf"
sudo a2enmod rewrite
sudo systemctl reload apache2

echo "✅ Subdomain $SUBDOMAIN configured and Apache reloaded."
