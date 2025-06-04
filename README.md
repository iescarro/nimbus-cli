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
pip install git+https://github.com/iescarro/nimbus-cli.git
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

###👋 Say hello

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
git clone https://github.com/yourusername/nimbus-cli.git
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

## 📄 License
MIT License — feel free to use and contribute!

## 🙌 Author
Made with ❤️ by ICE Solutions