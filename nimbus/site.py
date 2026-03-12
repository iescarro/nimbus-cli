import subprocess
import os
from .app import write_nimbus_index

def create_apache_site(username, domain):
    base_dir = f"/home/{username}/domains/{domain}/public_html"
    conf_file = f"/etc/apache2/sites-available/{domain}.conf"
    log_name = domain.replace('.', '_')

    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
    write_nimbus_index(base_dir)

    subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', f'/home/{username}/domains/{domain}'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', f'/home/{username}/domains/{domain}'], check=True)

    # Apache config content
    apache_config = f"""
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot {base_dir}
    ServerName {domain}
    ServerAlias www.{domain}

    <Directory {base_dir}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${{APACHE_LOG_DIR}}/{log_name}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{log_name}_access.log combined
</VirtualHost>
"""

    # Write Apache config to file
    with open('/tmp/apache_temp.conf', 'w') as temp_conf:
        temp_conf.write(apache_config.strip())

    subprocess.run(['sudo', 'mv', '/tmp/apache_temp.conf', conf_file], check=True)
    subprocess.run(['sudo', 'a2ensite', f'{domain}.conf'], check=True)
    subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'], check=True)

    print(f"✅ Site setup complete for {domain} under user {username}")

def create_apache_subdomain(username, domain, subdomain):
    fqdn = f"{subdomain}.{domain}"
    base_dir = f"/home/{username}/domains/{domain}/{subdomain}"
    conf_file = f"/etc/apache2/sites-available/{fqdn}.conf"
    log_name = f"{subdomain}_{domain}".replace('.', '_')

    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
    write_nimbus_index(base_dir)

    subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', f'/home/{username}/domains/{domain}/{subdomain}'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', f'/home/{username}/domains/{domain}/{subdomain}'], check=True)

    # Apache config content
    apache_config = f"""
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot {base_dir}
    ServerName {fqdn}

    <Directory {base_dir}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${{APACHE_LOG_DIR}}/{log_name}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{log_name}_access.log combined
</VirtualHost>
"""

    # Write Apache config to file
    with open('/tmp/apache_sub_temp.conf', 'w') as temp_conf:
        temp_conf.write(apache_config.strip())

    subprocess.run(['sudo', 'mv', '/tmp/apache_sub_temp.conf', conf_file], check=True)
    subprocess.run(['sudo', 'a2ensite', f'{fqdn}.conf'], check=True)
    subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'], check=True)

    print(f"✅ Subdomain setup complete: {fqdn} under user {username}")

def enable_ssl(domain):
    print(f"🔐 Enabling SSL for {domain} using Certbot...")
    try:
        subprocess.run(['sudo', 'certbot', '--apache', '-d', domain], check=True)
        print(f"✅ SSL enabled for {domain}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to enable SSL for {domain}. Please check your DNS and Apache config.")