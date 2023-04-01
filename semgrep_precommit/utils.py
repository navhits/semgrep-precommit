import os
import shutil
import subprocess
import tempfile
import typing


def add_safe_git_dir(path: str) -> None:
    """add_safe_git_dir marks the directory safe for git

    Args:
        path (str): The path to directory
    """
    try:
        subprocess.run(["git", "config", "--add", "safe.directory", path], cwd=path)
    except Exception:
        return

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

def commit_staged_files(path: str, message: str = "Dummy commit by semgrep pre-commit hook") -> bool:
    """commit_staged_files commits all staged files with a given message.

    Args:
        path (str): The path to the git repository.
        message (str, optional): A commit message. 
        Defaults to "Dummy commit by semgrep pre-commit hook".

    Returns:
        bool: True if the commit was successful, False otherwise.
    """
    try:
        # We use -n to avoid running the pre-commit hook again
        subprocess.run(["git", "commit", "-n", "-m", message], stdout=subprocess.DEVNULL,
                       cwd=path)
    except Exception:
        return False
    else:
        return True

def get_last_two_commit_ids(path: str) -> typing.Tuple[str | None, str | None]:
    """get_last_two_commit_ids returns the last two commit IDs of the current branch

    Args:
        path (str): The path to the git repository.

    Returns:
        typing.Tuple[str | None, str | None]: The last two commit IDs
    """
    commit_ids = None, None
    try:
        proc = subprocess.run(["git", "log", "--pretty=format:%H", "-n", "2"], 
                              capture_output=True, cwd=path)
        if proc.returncode == 0:
            commit_ids = proc.stdout.decode("utf-8").strip("\n").split("\n")
    except Exception:
        return None, None
    else:
        return tuple(commit_ids)

def soft_reset_to_commit(path: str, commit_id: str) -> bool:
    """git_soft_reset_to_commit performs a soft reset to the previous commit

    Args:
        commit_id (str): The commit ID to reset to

    Returns:
        bool: True if the soft reset was successful, False otherwise
    """
    try:
        subprocess.run(["git", "reset", "--soft", commit_id], stdout=subprocess.DEVNULL, cwd=path)
    except Exception:
        return False
    else:
        return True

def make_tmp_dir() -> tempfile.TemporaryDirectory:
    """
    make_tmp_dir: Creates a temporary directory

    Returns:
        tempfile.TemporaryDirectory: The tempfile.TemporaryDirectory object
    """
    temp_dir = tempfile.TemporaryDirectory()
    return temp_dir

def copy_to_tmp(dest: str | tempfile.TemporaryDirectory, src: str = "/src") -> bool:
    """
    copy_to_tmp: Copies the contents of the src directory to the dest directory

    Args:
        dest (str | tempfile.TemporaryDirectory): A tempfile.TemporaryDirectory object or a string
        src (str, optional): The source path to be copied. Defaults to "/src".

    Returns:
        bool: True if the copy was successful, False otherwise
    """
    dest_name = dest
    if isinstance(dest_name, tempfile.TemporaryDirectory):
        dest_name = dest.name

    try:
        shutil.copytree(src, dest_name, dirs_exist_ok=True)
        return True
    except Exception:
        return False
