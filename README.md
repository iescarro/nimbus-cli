# 🌩️ Nimbus CLI

A lightweight command-line tool to manage user accounts and domain directories on a Linux server.

## ✨ Features

- Create Linux users with associated domain directories
- Easily set up web directories under `/home/<username>/domains/<domain>/public_html`
- Simple `hello` command for testing and fun 🎉

---

## 🚀 Installation

You can install Nimbus CLI directly from GitHub:

```bash
sudo apt update
sudo apt install python3-venv python3-pip -y
python3 -m venv ~/nimbus-env
source ~/nimbus-env/bin/activate

# Install with all dependencies in one command
pip install pyyaml paramiko scp git+https://github.com/iescarro/nimbus-cli.git
```

Make sure pip is using Python 3 and your environment is properly set up (e.g., with python3 -m venv if needed).

## 🛠️ Usage

### 👋 Say hello

```bash
nimbus hello
```

Output:

```cpp
👋 Hello, friend!
```

### 🚀 Install LAMP Stack

To install the LAMP (Linux, Apache, MySQL/MariaDB, PHP) stack using Nimbus:

```bash
nimbus install-lamp
```

This command sets up the essential components for running PHP-based web applications on your system.

**⚠️ Node.js Note**

If you are installing Node.js as part of your development stack and encounter package conflicts (common on Ubuntu systems with pre-installed Node.js), you must remove the conflicting packages before running nimbus install-lamp.

**🛠️ Fix Node.js installation conflict**

```bash
sudo apt remove -y nodejs libnode72
sudo apt autoremove -y
```

This ensures that a clean version of Node.js (LTS) and npm can be installed from the official NodeSource repository without conflicts.

### ✅ Create a new user and web directory

```bash
nimbus create-user <username> <domain>
```

Example:

```bash
nimbus create-user alice example.com
```

This creates:

* Linux user alice
* Directory `/home/alice/domains/example.com/public_html`
* Correct ownership and permissions

> ℹ️ Note:
The user is created with a disabled password by default.
To allow su - alice or terminal login, manually set a password:

```bash
sudo passwd alice
```

Then follow the prompt to enter a new password for the user.

✅ Set Up the Website (Apache VirtualHost)

```bash
nimbus create-site <username> <domain>
```

Example:
```bash
nimbus create-site alice example.com
```

This will:
* Create an Apache VirtualHost for example.com
* Enable the site and reload Apache
* Generate a default index.html inside public_html with a "Nimbus is Ready!" page like this:

<p align="center"> <img src="https://raw.githubusercontent.com/iescarro/nimbus-cli/main/art/sample.png?v=1" alt="Nimbus is Ready!" width="400"/> </p>

> 📁 This confirms your LAMP setup is working. You can now upload your site files to the public_html directory.

### ✅ Create Subdomain

```bash
nimbus create-subdomain alice example.com sub
```

This command will create the subdomain sub.example.com under the user alice and associate it with the domain example.com.

✅ Request SSL Certificate (Let's Encrypt via Certbot)

After creating the subdomain, you can request a free SSL certificate using Certbot:

```bash
sudo certbot --apache -d sub.example.com
```

## 🔄 Upgrade

To upgrade nimbus-cli to the latest version from GitHub:

```bash
pip install --upgrade --force-reinstall git+https://github.com/iescarro/nimbus-cli.git
```

This command ensures that:
* The latest code from the main branch is downloaded
* The package is reinstalled, even if the version number hasn't changed

> 💡 Tip: To avoid unnecessary reinstalls, always update the version in setup.py when making changes.

## 📦 Development

If you're working on the project:

```bash
git clone https://github.com/iescarro/nimbus-cli.git
cd nimbus-cli
pip install -e .
```

This installs it in editable mode, so changes take effect immediately.

## 🧪 Example Project Structure

```arduino
nimbus-cli/
├── nimbus/
│   └── __main__.py
├── setup.py
├── README.md
```

## 🔐 Requirements

* Python 3.6+
* sudo privileges for user creation

## 🛠️ Troubleshooting

### ✅ Issue: nimbus: command not found after installation

This usually happens because the nimbus CLI was installed to a directory not included in your system’s PATH.

### ✅ Solution: Add ~/.local/bin to your PATH

1. Edit your shell profile (choose the one that applies):

For bash:

```bash
nano ~/.bashrc
```

2. Add this line at the end:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

3. Apply the change:

```bash
source ~/.bashrc   # or source ~/.zshrc if you're using zsh
```

4. Test it:

```bash
which nimbus
nimbus hello
```

### ✅ Expected output:

```bash
Hello, friend!
```

## 📄 License
MIT License — feel free to use and contribute!

## 🙌 Author
Made with ❤️ by ICE Solutions
