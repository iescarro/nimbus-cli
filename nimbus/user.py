import subprocess
import time

from .site import write_nimbus_index

def wait_for_user(username, timeout=5):
    """Wait for user to be registered in the system, printing '.' for progress."""
    print(f"⏳ Waiting for user '{username}' to be registered:", end='', flush=True)
    for _ in range(timeout * 10):  # check every 0.1s for up to `timeout` seconds
        try:
            import pwd
            pwd.getpwnam(username)
            print(" ✅")  # user found, finish line
            return True
        except KeyError:
            print(".", end='', flush=True)
            time.sleep(0.1)
    return False

def is_wsl():
    """Detect if the script is running under Windows Subsystem for Linux."""
    try:
        with open("/proc/sys/kernel/osrelease", "r") as f:
            return "microsoft" in f.read().lower()
    except FileNotFoundError:
        return False

def create_user(username, domain):
    user_home = f"/home/{username}"
    web_dir = f"/home/{username}/domains/{domain}/public_html"

    try:
        import pwd
        pwd.getpwnam(username)
        print(f"⚠️ User '{username}' already exists. Skipping user creation.")
    except KeyError:
        subprocess.run(['sudo', 'adduser', '--disabled-password', '--gecos', '', username], check=True)
        print(f"✅ User '{username}' created.")

        # Wait a moment to allow system to register the user
        if not wait_for_user(username):
            print(f"❌ Timeout: user '{username}' was not registered properly.")
            return

        if is_wsl():
            print("⏳ Detected WSL. Sleeping for 3 seconds to finalize user registration...")
            time.sleep(3)  # Give WSL time to finalize user registration

        # Create the web directory as root
        subprocess.run(['sudo', 'mkdir', '-p', web_dir], check=True)
        write_nimbus_index(web_dir)

        subprocess.run(['sudo', 'chown', '-R', f"{username}:{username}", user_home], check=True)
        subprocess.run(['sudo', 'chmod', '-R', '755', user_home], check=True)

        print(f"✅ User '{username}' ready. Web directory: {web_dir}")