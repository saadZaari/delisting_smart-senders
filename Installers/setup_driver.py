import os
import sys
import subprocess

# Dynamically determine the path to geckodriver by navigating from the current script's folder
current_folder = os.path.dirname(os.path.abspath(__file__))  # Get the folder where the script is located
geckodriver_folder = os.path.join(current_folder, '..', 'Delisting Scripts')  # Go one folder up and then into 'scripts'
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
        print("Please download geckodriver and place it in the 'scripts' folder.")

if __name__ == "__main__":
    main()
