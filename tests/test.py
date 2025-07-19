


def is_wsl():
    """Detect if the script is running under Windows Subsystem for Linux."""
    try:
        with open("/proc/sys/kernel/osrelease", "r") as f:
            return "microsoft" in f.read().lower()
    except FileNotFoundError:
        return False
    

print(f"Detected WSL: {is_wsl()}")  # Debugging line to check WSL detection