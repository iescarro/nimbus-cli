import os
import subprocess
from .app import write_nimbus_index

def create_nginx_site(username, domain):
    """
    Create an Nginx site configuration for a given username and domain
    """
    base_dir = f"/home/{username}/domains/{domain}/public_html"
    conf_file = f"/etc/nginx/sites-available/{domain}"
    enabled_link = f"/etc/nginx/sites-enabled/{domain}"
    log_name = domain.replace('.', '_')
    
    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
    write_nimbus_index(base_dir)  # Your existing function
    
    # Set proper permissions
    subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', f'/home/{username}/domains/{domain}'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', f'/home/{username}/domains/{domain}'], check=True)
    
    # Nginx config content
    nginx_config = f"""
server {{
    listen 80;
    listen [::]:80;
    
    server_name {domain} www.{domain};
    
    root {base_dir};
    index index.php index.html index.htm;
    
    access_log /var/log/nginx/{log_name}_access.log;
    error_log /var/log/nginx/{log_name}_error.log;
    
    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}
    
    # PHP-FPM handling (if using PHP)
    location ~ \.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;  # Adjust PHP version as needed
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }}
    
    # Deny access to hidden files
    location ~ /\. {{
        deny all;
        access_log off;
        log_not_found off;
    }}
    
    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg)$ {{
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }}
}}
"""
    
    # Write config to temp file
    with open('/tmp/nginx_temp.conf', 'w') as temp_conf:
        temp_conf.write(nginx_config.strip())
    
    # Move to sites-available
    subprocess.run(['sudo', 'mv', '/tmp/nginx_temp.conf', conf_file], check=True)
    
    # Create symlink to enable site
    if os.path.exists(enabled_link):
        subprocess.run(['sudo', 'rm', enabled_link], check=True)
    subprocess.run(['sudo', 'ln', '-s', conf_file, enabled_link], check=True)
    
    # Test Nginx configuration
    try:
        subprocess.run(['sudo', 'nginx', '-t'], check=True, capture_output=True)
        print("✅ Nginx configuration test passed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Nginx configuration test failed: {e.stderr.decode()}")
        return False
    
    # Reload Nginx
    subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)
    
    print(f"✅ Nginx site setup complete for {domain} under user {username}")
    print(f"📁 Document root: {base_dir}")
    print(f"🔗 Config file: {conf_file}")
    
    return True

def create_nginx_subdomain(username, domain, subdomain):
    fqdn = f"{subdomain}.{domain}"
    base_dir = f"/home/{username}/domains/{domain}/{subdomain}"
    conf_file = f"/etc/nginx/sites-available/{fqdn}.conf"
    log_name = f"{subdomain}_{domain}".replace('.', '_')

    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
    write_nimbus_index(base_dir)

    subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', f'/home/{username}/domains/{domain}/{subdomain}'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '755', f'/home/{username}/domains/{domain}/{subdomain}'], check=True)

    # Detect PHP version for PHP-FPM socket
    # php_version = detect_php_version()
    php_socket = f"unix:/var/run/php/php8.3-fpm.sock"  # Adjust PHP version as needed

    # Nginx config content for subdomain
    nginx_config = f"""
server {{
    listen 80;
    listen [::]:80;
    
    server_name {fqdn};
    
    root {base_dir}/public;
    index index.php index.html index.htm;
    
    access_log /var/log/nginx/{log_name}_access.log;
    error_log /var/log/nginx/{log_name}_error.log;
    
    location / {{
        try_files $uri $uri/ /index.php?$query_string;
    }}
    
    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass {php_socket};
    }}
    
    location ~ /\.ht {{
        deny all;
    }}
}}
"""

    # Write Nginx config to temp file
    with open('/tmp/nginx_sub_temp.conf', 'w') as temp_conf:
        temp_conf.write(nginx_config.strip())

    # Move to sites-available
    subprocess.run(['sudo', 'mv', '/tmp/nginx_sub_temp.conf', conf_file], check=True)
    
    # Create symbolic link to enable site
    subprocess.run(['sudo', 'ln', '-sf', conf_file, f'/etc/nginx/sites-enabled/{fqdn}.conf'], check=True)
    
    # Test Nginx configuration
    subprocess.run(['sudo', 'nginx', '-t'], check=True)
    
    # Reload Nginx
    subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)

    print(f"✅ Nginx subdomain setup complete: {fqdn} under user {username}")
    print(f"   📁 Document root: {base_dir}")