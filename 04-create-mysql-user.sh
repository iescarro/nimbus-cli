#!/bin/bash

# Usage: ./create_mysql_user.sh dbname username password

DB_NAME="$1"
DB_USER="$2"
DB_PASS="$3"

if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ]; then
    echo "Usage: $0 <database_name> <username> <password>"
    exit 1
fi

echo "Creating database and user..."
mysql -u root -p <<EOF
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "Done: Database '$DB_NAME' and user '$DB_USER' created."
