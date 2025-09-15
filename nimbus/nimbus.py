
def say_hello():
    print("👋 Hello, friend!")

def print_usage():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    📦 Nimbus CLI — LAMP site manager         ║
╚══════════════════════════════════════════════════════════════╛

USAGE:
  nimbus <command> [options] [arguments]

CORE COMMANDS:
  hello                                      Greet the user
  install-lamp                               Install Apache, MySQL, PHP, Python, Composer, Certbot

SITE MANAGEMENT:
  create-user <user> <domain>                Create a Linux user and web directory
  create-site <user> <domain>                Set up Apache site config and public_html
  create-subdomain <user> <domain> <sub>     Create subdomain site under user
  enable-ssl <domain>                        Enable SSL using Certbot (Let's Encrypt)

DATABASE COMMANDS:
  create-database <name> <user> <pass>       Create MySQL DB and user
  db:backup <app:database>                   Back up database from instance
  db:restore <app:database> [db_name]        Restore database (optional: specific backup)
  db:migrate <src:database> <dest:database>  Migrate database between instances

OTHER OPTIONS:
  -v, --version                              Show current version
  -h, --help                                 Show this help message

EXAMPLES:
  nimbus create-user alice example.com
  nimbus create-site alice example.com
  nimbus db:backup production:wordpress
  nimbus db:restore staging:wordpress
  nimbus db:migrate production:wordpress staging:wordpress

💡 Tip: Use 'nimbus <command> --help' for detailed command information
""")