import subprocess
import os

def update_repo(repo_path, branch='master'):
    try:
        # Change the current working directory to your repo path
        os.chdir(repo_path)

        # Fetch the latest changes from the remote repository
        print(f"Pulling the latest changes from {branch} branch...")
        subprocess.check_call(['git', 'pull', 'origin', branch])

        print("Repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while updating the repository: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Path to your local git repository (two levels up from the script's location)
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Goes up two folders

    # Pull from the 'master' branch
    update_repo(repo_path, 'master')
