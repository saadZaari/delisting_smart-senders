import subprocess
import os

def update_repo(repo_path, branch='master'):
    try:
        # Print the repository path for debugging
        print(f"Repository path: {repo_path}")

        # Change the current working directory to your repo path
        os.chdir(repo_path)
        print("Changed working directory to:", os.getcwd())

        # Check if .git directory exists to confirm it's a git repository
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print("Error: No .git directory found in the specified path.")
            return

        # Print the current branch and status
        subprocess.run(['git', 'status'])

        # Fetch the latest changes from the remote repository
        print(f"Pulling the latest changes from {branch} branch...")
        result = subprocess.run(['git', 'pull', 'origin', branch], capture_output=True, text=True)

        # Print the output and any errors from git pull
        print(result.stdout)
        print(result.stderr)

        if result.returncode == 0:
            print("Repository updated successfully.")
        else:
            print(f"Git pull failed with exit code {result.returncode}. Check the above output for details.")

    except subprocess.CalledProcessError as e:
        print(f"Error while updating the repository: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Path to your local git repository (two levels up from the script's location)
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Goes up two folders

    # Pull from the 'master' branch
    update_repo(repo_path, 'master')
