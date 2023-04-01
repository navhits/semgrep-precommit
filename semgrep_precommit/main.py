import os
import subprocess
import sys

from semgrep_precommit.utils import *

def run_semgrep(arguments: list[str]) -> int:
    """run_semgrep runs semgrep with the given arguments.

    Args:
        arguments (list[str]): A list of arguments to pass to semgrep.

    Returns:
        int: The exit code of the semgrep command.
    """
    command = ["semgrep", "scan"]
    command += arguments
    proc = subprocess.run(command)
    return proc.returncode

def main() -> None:
    """main is the entrypoint for the pre-commit hook.
    """
    arguments = list(sys.argv[1:])
    for argument in list(arguments):
        if is_file(argument):
            arguments.remove(argument)
    temp_dir = make_tmp_dir()
    is_copied = copy_to_tmp(dest=temp_dir, src="/src")
    if not is_copied:
        print("Failed to copy files to temporary directory")
        sys.exit(1)
    else:
        add_safe_git_dir(temp_dir.name)
    current_commit, commit_before_current = None, None
    is_commit = commit_staged_files(temp_dir.name)
    if is_commit:
        current_commit, commit_before_current = get_last_two_commit_ids(temp_dir.name)
        os.environ["SEMGREP_BASELINE_REF"] = commit_before_current
    exit_code = run_semgrep(arguments)
    if is_commit:
        soft_reset_to_commit(temp_dir.name, commit_before_current)
    temp_dir.cleanup()
    sys.exit(exit_code)

if __name__ == "__main__":
    raise main()
