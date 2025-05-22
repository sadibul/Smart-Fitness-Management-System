import subprocess
import os
import sys

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error details: {e.stderr}")
        return None

def check_git_installed():
    """Check if git is installed."""
    try:
        version = run_command("git --version")
        if version:
            print(f"Git is installed: {version}")
            return True
        return False
    except:
        return False

def setup_git_repo():
    """Set up git repository and push to GitHub."""
    repo_url = "https://github.com/sadibul/Smart-Fitness-Management-System.git"
    
    print("\n=== Setting up Git repository ===\n")
    
    # Check if git is installed
    if not check_git_installed():
        print("Git is not installed. Please install Git and try again.")
        return False
    
    # Check if .git directory already exists
    if os.path.exists(".git"):
        print("Git repository already initialized.")
    else:
        # Initialize git repository
        print("Initializing Git repository...")
        if not run_command("git init"):
            return False
    
    # Create .gitignore file
    print("Creating .gitignore file...")
    with open(".gitignore", "w") as f:
        f.write("__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.env\n.venv\nenv/\nvenv/\nENV/\n")
    
    # Add files to git
    print("Adding files to git...")
    if not run_command("git add ."):
        return False
    
    # Commit changes
    print("Committing changes...")
    if not run_command('git commit -m "Initial commit of Smart Fitness Management System"'):
        return False
    
    # Add remote repository
    print(f"Adding remote repository: {repo_url}")
    if run_command("git remote"):
        print("Remote already exists. Updating...")
        if not run_command(f"git remote set-url origin {repo_url}"):
            return False
    else:
        if not run_command(f"git remote add origin {repo_url}"):
            return False
    
    # Push to GitHub
    print("Pushing to GitHub...")
    result = run_command("git push -u origin master")
    if not result:
        # Try pushing to main branch instead
        print("Trying to push to main branch instead...")
        result = run_command("git push -u origin main")
        if not result:
            print("\nPush failed. You might need to:")
            print("1. Ensure you have the correct access permissions to the repository")
            print("2. Use a personal access token if required")
            print("3. Push manually with: git push -u origin main")
            return False
    
    print("\n=== Success! ===")
    print(f"Your code has been pushed to: {repo_url}")
    return True

if __name__ == "__main__":
    setup_git_repo()
