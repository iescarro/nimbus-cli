#!/usr/bin/env python3

import os
import sys
import subprocess

from .__version__ import __version__

from .nimbus import say_hello, print_usage
from .app import App, init, install_lamp_stack, open_app
from .lemp import Lemp
from .db import DB
from .site import enable_ssl, create_apache_site, create_apache_subdomain
from .user import User
from .swap import Swap

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
    elif command == "open":
        if len(sys.argv) == 2:
            open_app()
        elif len(sys.argv) == 3:
            env, app = sys.argv[2].split(':')
            open_app(environment=env, app_name=app)
        else:
            print("Usage: nimbus open [app]")
            sys.exit(1)
    elif command == "deploy":
        if len(sys.argv) == 2:
            deploy_app()  # Uses default:default
        elif len(sys.argv) == 3:
            if ':' in sys.argv[2]:
                env, app = sys.argv[2].split(':')
                deploy_app(environment=env, app_name=app)
            else:
                deploy_app(app_name=sys.argv[2])  # Uses default env
        else:
            print("Usage: nimbus deploy [env:app|app]")
            sys.exit(1)

    # System setup commands
    elif command == "install-lamp":
        install_lamp_stack()
    elif command == "install-lemp":
        Lemp.install()

    elif command == "swap-on":
        swap = Swap()
        swap.on()
    elif command == "swap-off":
        swap = Swap()
        swap.off()

    elif command == "create-user":
        if len(sys.argv) != 4:
            print("Usage: nimbus.py create-user <username> <domain>")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        User.create(username, domain)s
    elif command == "delete-user":
        if len(sys.argv) != 3:
            print("Usage: nimbus.py delete-user <username>")
            sys.exit(1)
        username = sys.argv[2]
        User.delete(username)

    # Database management commands
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
    elif command == "db:backup":
        if len(sys.argv) < 2:
            print("Usage: nimbus db:backup <source_app:db>")
            sys.exit(1)
        source = sys.argv[2] if len(sys.argv) > 2 else "default:default"
        DB.backup(source)
    elif command == "db:restore":
        if len(sys.argv) < 2:
            print("Usage: nimbus db:restore <destination_app:db> <db_name>")
            sys.exit(1)
        destination = sys.argv[2] if len(sys.argv) > 2 else "default:default"
        db_name = sys.argv[3] if len(sys.argv) > 3 else None
        DB.restore(destination, db_name)

    # Site management commands
    elif command == "create-site":
        if len(sys.argv) <= 4:
            print("Usage: nimbus create-site <username> <domain> [--nginx] [--apache]")
            print("  --nginx   Create an Nginx site (default)")
            print("  --apache  Create an Apache site")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        server_type = "nginx"
        if len(sys.argv) > 4:
            if "--apache" in sys.argv:
                server_type = "apache"
            elif "--nginx" in sys.argv:
                server_type = "nginx"
        if server_type == "apache":
            from .site import create_apache_site
            create_apache_site(username, domain)
        else:
            from .nginx import create_nginx_site
            create_nginx_site(username, domain)
    elif command == "create-subdomain":
        if len(sys.argv) <= 5:
            print("Usage: nimbus create-subdomain <username> <domain> <subdomain> [--nginx] [--apache]")
            print("  --nginx   Create an Nginx subdomain (default)")
            print("  --apache  Create an Apache subdomain")
            sys.exit(1)
        username = sys.argv[2]
        domain = sys.argv[3]
        subdomain = sys.argv[4]
        server_type = "nginx"
        if len(sys.argv) > 5:
            if "--apache" in sys.argv:
                server_type = "apache"
            elif "--nginx" in sys.argv:
                server_type = "nginx"        
        if server_type == "apache":
            from .site import create_apache_subdomain
            create_apache_subdomain(username, domain, subdomain)
        else:
            from .nginx import create_nginx_subdomain
            create_nginx_subdomain(username, domain, subdomain)
    elif command == "enable-ssl":
        if len(sys.argv) < 3:
            print("Usage: nimbus enable-ssl <domain> [--apache] [--nginx]")
            print("  --apache  Use Apache (default)")
            print("  --nginx   Use Nginx")
            sys.exit(1)
        domain = sys.argv[2]
        web_server = "apache"
        if len(sys.argv) > 3:
            if "--apache" in sys.argv:
                web_server = "apache"
            elif "--nginx" in sys.argv:
                web_server = "nginx"
        enable_ssl(domain, web_server)
    # elif command == "db:migrate":
    #     if len(sys.argv) != 2:
    #         print("Usage: nimbus db:migrate")
    #         sys.exit(1)
    #     DB.migrate()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
