#!/bin/bash

# === Check arguments ===
if [ $# -ne 2 ]; then
  echo "Usage: $0 <username> <domain>"
  exit 1
fi

USERNAME=$1
DOMAIN=$2

# === Create User ===
sudo adduser $USERNAME

# === Create Public HTML Directory ===
USER_HOME="/home/$USERNAME"
WEB_DIR="$USER_HOME/domains/$DOMAIN/public_html"

mkdir -p "$WEB_DIR"

# === Set Ownership and Permissions ===
sudo chown -R $USERNAME:$USERNAME "$USER_HOME"
sudo chmod -R 755 "$USER_HOME"

echo "✅ User '$USERNAME' created and web directory '$WEB_DIR' is ready."
