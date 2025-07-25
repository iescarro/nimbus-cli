
def say_hello():
    print("👋 Hello, friend!")

def print_usage():
    print("""📦 Nimbus CLI — LAMP site manager
Usage:
  nimbus <command> [options]

Available Commands:
  hello                                   Greet the user
  install-lamp                            Install Apache, MySQL, PHP, Python, Composer, Certbot
  create-user <user> <domain>             Create a Linux user and web directory
  create-site <user> <domain>             Set up Apache site config and public_html
  create-subdomain <user> <domain> <sub>  Create subdomain site under user
  create-database <name> <user> <pass>    Create MySQL DB and user
  enable-ssl <domain>                     Enable SSL using Certbot (Let's Encrypt)

Other Options:
  -v, --version                             Show current version

Example:
  nimbus create-user alice example.com
""")