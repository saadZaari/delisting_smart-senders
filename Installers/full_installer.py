import os
import subprocess
import urllib.request
import tempfile
import shutil
import sys

# Configuration: replace with your repository URL and target directory
REPO_URL = "https://github.com/saadZaari/delisting_smart-senders"
TARGET_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "delisting_smart-senders")
def install_git():
    """Download and install Git silently if not already installed."""
    # Try to get the Git version by running git --version
    try:
        result = subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Git is already installed.")
        return True
    except FileNotFoundError:
        print("Git is not found in PATH, checking common installation directories...")
    
    # Alternatively, check if Git is in standard locations (if not in PATH)
    possible_paths = [
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe"
    ]
    git_path = None
    for path in possible_paths:
        if os.path.exists(path):
            git_path = path
            break

    if git_path:
        print(f"Git is installed at {git_path}.")
        return True

    # Download the Git installer
    git_installer_url = "https://github.com/git-for-windows/git/releases/download/v2.47.0.windows.2/Git-2.47.0.2-64-bit.exe"
    temp_dir = tempfile.gettempdir()
    git_installer_path = os.path.join(temp_dir, "GitInstaller.exe")
    urllib.request.urlretrieve(git_installer_url, git_installer_path)

    # Run the Git installer silently
    try:
        subprocess.run([git_installer_path, "/VERYSILENT", "/NORESTART"], check=True)
        print("Git installation completed successfully.")
    except subprocess.CalledProcessError:
        print("Git installation failed. Please check permissions or network settings.")
        return False
    finally:
        os.remove(git_installer_path)

    # Wait for a moment to ensure the PATH is updated (sometimes requires a restart of the shell)
    print("Waiting for the system to update PATH...")
    import time
    time.sleep(2)

    # Check if Git is now installed (after installation and PATH update)
    try:
        result = subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Git is successfully installed and ready to use.")
        return True
    except subprocess.CalledProcessError:
        print("Git installation did not complete successfully.")
        return False
 
# def clone_or_pull_repo():
#     """Clone the repository if it doesn’t exist, otherwise pull the latest changes."""
#     if not os.path.exists(TARGET_DIR):
#         print("Cloning repository...")
#         subprocess.run(["git", "clone", REPO_URL, TARGET_DIR], check=True)
#         print("Repository cloned successfully.")
#     else:
#         print("Repository already exists. Pulling latest changes...")
#         subprocess.run(["git", "-C", TARGET_DIR, "pull"], check=True)
#         print("Repository updated with the latest changes.")

def main():
    if install_git():
        # clone_or_pull_repo()
        print("Repository update process completed successfully.")
    else:
        print("Failed to install Git. Please try again or check the installation steps.")

if __name__ == "__main__":
    main()