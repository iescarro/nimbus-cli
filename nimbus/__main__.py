#!/usr/bin/env python3

import os
import sys
import subprocess

def create_user(username, domain):
    user_home = f"/home/{username}"
    web_dir = os.path.join(user_home, f"domains/{domain}/public_html")

    # Create user
    subprocess.run(['sudo', 'adduser', '--disabled-password', '--gecos', '', username], check=True)

    # Create web directory
    os.makedirs(web_dir, exist_ok=True)

    # Set permissions
    subprocess.run(['sudo', 'chown', '-R', f"{username}:{username}", user_home], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', user_home], check=True)

    print(f"✅ User '{username}' created and web directory '{web_dir}' is ready.")

def main():
    if len(sys.argv) < 2:
        print("Usage: nimbus.py <command> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create-user":
        if len(sys.argv) != 4:
            print("Usage: nimbus.py create-user <username> <domain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        create_user(username, domain)

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
