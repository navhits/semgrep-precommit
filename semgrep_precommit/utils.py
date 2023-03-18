import os
import subprocess
import typing


def is_file(filename: str) -> bool:
    """is_file checks if a given value is valid a file.

    Args:
        filename (str): The filename to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if os.path.isfile(filename):
        return True
    return False

def commit_staged_files(message: str = "Dummy commit by semgrep pre-commit hook") -> bool:
    """commit_staged_files commits all staged files with a given message.

    Args:
        message (str, optional): A commit message. 
        Defaults to "Dummy commit by semgrep pre-commit hook".

    Returns:
        bool: True if the commit was successful, False otherwise.
    """
    try:
        # We use -n to avoid running the pre-commit hook again
        subprocess.run(["git", "commit", "-n", "-m", message], stdout=subprocess.DEVNULL)
    except Exception:
        return False
    else:
        return True

def get_last_two_commit_ids() -> typing.Tuple[str | None, str | None]:
    """get_last_two_commit_ids returns the last two commit IDs of the current branch

    Returns:
        typing.Tuple[str | None, str | None]: The last two commit IDs
    """
    commit_ids = None, None
    try:
        proc = subprocess.run(["git", "log", "--pretty=format:%H", "-n", "2"], 
                              capture_output=True)
        if proc.returncode == 0:
            commit_ids = proc.stdout.decode("utf-8").strip("\n").split("\n")
    except Exception:
        return None, None
    else:
        return tuple(commit_ids)

def soft_reset_to_commit(commit_id: str) -> bool:
    """git_soft_reset_to_commit performs a soft reset to the previous commit

    Args:
        commit_id (str): The commit ID to reset to

    Returns:
        bool: True if the soft reset was successful, False otherwise
    """
    try:
        subprocess.run(["git", "reset", "--soft", commit_id], stdout=subprocess.DEVNULL)
    except Exception:
        return False
    else:
        return True
