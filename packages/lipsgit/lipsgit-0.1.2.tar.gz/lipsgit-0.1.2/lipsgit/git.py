import subprocess


def get_base_git_repo_path():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        git_toplevel_path = result.stdout.strip()
        return git_toplevel_path
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to get Git top-level directory. {e}")
        return None


def git_commit(title: str, description: str):
    commit_args = ["git", "commit", "-m", title, "-m", description]
    try:
        # Use subprocess to run the git command
        subprocess.run(commit_args, check=True)
        print("Git commit successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Git commit failed. {e}")


def get_last_commit_message():
    try:
        # Run the git log command and capture the output
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Handle any errors, if necessary
        print(f"Error running 'git log': {e}")
        return None
