import os
import sys
import subprocess
import winreg

# Dynamically determine the path to geckodriver by navigating from the current script's folder
current_folder = os.path.dirname(os.path.abspath(__file__))  # Get the folder where the script is located
geckodriver_folder = os.path.join(current_folder, '..', 'Delisting Scripts')  # Go one folder up and then into 'Delisting Scripts'
GECKODRIVER_PATH = os.path.join(geckodriver_folder, 'geckodriver.exe')  # Final path to geckodriver.exe

def check_geckodriver():
    """Check if geckodriver exists in the specified folder."""
    if os.path.exists(GECKODRIVER_PATH):
        print(f"Found geckodriver at {GECKODRIVER_PATH}.")
        return GECKODRIVER_PATH
    else:
        print(f"geckodriver not found in {geckodriver_folder}. Please make sure the driver is placed correctly.")
        return None

def add_to_path():
    """Add the geckodriver folder to the system PATH environment variable."""
    # Get the current PATH
    current_path = os.environ.get('PATH', '')
    
    # Check if the folder is already in the PATH
    if geckodriver_folder in current_path:
        print(f"{geckodriver_folder} is already in the PATH.")
        return True

    # Add geckodriver folder to the system PATH
    new_path = current_path + os.pathsep + geckodriver_folder
    
    # Update the PATH for the current session
    os.environ['PATH'] = new_path
    print(f"Added {geckodriver_folder} to the current PATH.")

    # Persist the new PATH for future sessions (Windows registry)
    try:
        # For Windows, update the system PATH in the registry
        subprocess.run(['setx', 'PATH', new_path], check=True)
        print(f"Persisted {geckodriver_folder} to system PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update the system PATH: {e}")
        return False

    return True

def set_python_as_default_for_py_files():
    """Set Python as the default application to open .py files on Windows."""
    try:
        # Get the path to the current Python executable
        python_path = sys.executable
        
        # Define registry keys for the default app for .py files
        py_auto_file_key = r"Software\Classes\Python.File\shell\open\command"
        py_extension_key = r"Software\Classes\.py"
        
        # Set .py files to be associated with Python
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, py_extension_key, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Python.File")

        # Set Python executable as the command for opening .py files
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, py_auto_file_key, 0, winreg.KEY_SET_VALUE) as key:
            command = f'"{python_path}" "%1" %*'
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)

        print("Python is now set as the default application for .py files.")
    except Exception as e:
        print(f"An error occurred while setting Python as the default app: {e}")

def initialize_git_repo():
    """Initialize a Git repository in the current directory."""
    try:
        result = subprocess.run(['git', 'init'], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Git init errors: {result.stderr}")
        else:
            print("Initialized an empty Git repository in the current directory.")
    except Exception as e:
        print(f"An error occurred while initializing the Git repository: {e}")

def main():
    # Check if geckodriver exists
    geckodriver_path = check_geckodriver()
    if geckodriver_path:
        # Add geckodriver folder to the PATH
        if add_to_path():
            print("Geckodriver setup completed successfully.")
        else:
            print("Failed to set up geckodriver in the PATH.")
    else:
        print("Please download geckodriver and place it in the 'Delisting Scripts' folder.")
    
    # Set Python as the default application for .py files
    set_python_as_default_for_py_files()

    # Initialize Git repository
    initialize_git_repo()

if __name__ == "__main__":
    main()
