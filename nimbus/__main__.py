#!/usr/bin/env python3

import os
import sys
import subprocess

from .__version__ import __version__

from .nimbus import say_hello, print_usage
from .app import init, install_lamp_stack
from .db import DB
from .site import enable_ssl, create_site, create_subdomain
from .user import create_user

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Handle --version or -v globally
    if sys.argv[1] in ["--version", "-v"]:
        print(f"nimbus-cli version {__version__}")
        sys.exit(0)

    command = sys.argv[1]

    if command == "hello":
        say_hello()
    elif command == "init":
        init()
    elif command == "install-lamp":
        install_lamp_stack()
    elif command == "create-user":
        if len(sys.argv) != 4:
            print("Usage: nimbus.py create-user <username> <domain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        create_user(username, domain)
    elif command == "create-database":
        if len(sys.argv) != 5:
            print("Usage: nimbus create-database <db_name> <db_user> <db_password>")
            sys.exit(1)
        db_name = sys.argv[2]
        db_user = sys.argv[3]
        db_password = sys.argv[4]
        DB.create_database(db_name, db_user, db_password)
    elif command == "db:migrate":
        if len(sys.argv) != 4:
            print("Usage: nimbus db:migrate <source_app:db> <target_app:db>")
            sys.exit(1)
        DB.migrate(sys.argv[2], sys.argv[3])
    elif command == "create-site":
        if len(sys.argv) != 4:
            print("Usage: nimbus create-site <username> <domain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        create_site(username, domain)
    elif command == "create-subdomain":
        if len(sys.argv) != 5:
            print("Usage: nimbus create-subdomain <username> <domain> <subdomain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        subdomain = sys.argv[4]
        create_subdomain(username, domain, subdomain)
    elif command == "enable-ssl":
        if len(sys.argv) != 3:
            print("Usage: nimbus enable-ssl <domain>")
            sys.exit(1)
        domain = sys.argv[2]
        enable_ssl(domain)
    elif command == "db:migrate":
        if len(sys.argv) != 2:
            print("Usage: nimbus db:migrate")
            sys.exit(1)
        DB.migrate()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
