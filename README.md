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

pip install git+https://github.com/iescarro/nimbus-cli.git
nimbus --help
```

Make sure pip is using Python 3 and your environment is properly set up (e.g., with python3 -m venv if needed).

## 🛠️ Usage

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
* Directory /home/alice/domains/example.com/public_html
* Correct ownership and permissions

### 👋 Say hello

```bash
nimbus hello
```

Output:

```cpp
👋 Hello, friend!
```

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
