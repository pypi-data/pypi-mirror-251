"""
"""
import os
import subprocess


def is_git_repo(
    git_repo_path,
) -> bool:

    if not os.path.isdir(git_repo_path):
        # A git repo can only be inside a dir:
        return False

    sub_proc = subprocess.run(
        [
            "git",
            "-C",
            git_repo_path,
            "rev-parse",
            "--show-toplevel",
        ],
        cwd = git_repo_path,
        capture_output = True,
    )
    exit_code = sub_proc.returncode

    if exit_code == 0:
        return True
    else:
        return False

def get_full_commit_id(
    git_repo_path: str,
) -> str:
    sub_proc = subprocess.run(
        [
            "git",
            "rev-parse",
            "HEAD",
        ],
        cwd = git_repo_path,
        capture_output = True,
    )
    exit_code = sub_proc.returncode

    if exit_code == 0:
        return sub_proc.stdout.decode("utf-8").strip()
    else:
        # If `is_git_repo` returns `True`, this should not happen:
        raise RuntimeError


def get_short_commit_id(
    git_repo_path: str,
) -> str:
    sub_proc = subprocess.run(
        [
            "git",
            "rev-parse",
            "--short",
            "HEAD",
        ],
        cwd = git_repo_path,
        capture_output = True,
    )
    exit_code = sub_proc.returncode

    if exit_code == 0:
        return sub_proc.stdout.decode("utf-8").strip()
    else:
        # If `is_git_repo` returns `True`, this should not happen:
        raise RuntimeError


def get_commit_time(
    git_repo_path: str,
) -> int:
    """
    Returns seconds since epoch (Unix time) for the last commit.
    """

    sub_proc = subprocess.run(
        [
            "git",
            "log",
            "-1",
            "--format=%ct",
        ],
        cwd = git_repo_path,
        capture_output = True,
    )
    exit_code = sub_proc.returncode

    if exit_code == 0:
        return int(sub_proc.stdout.decode("utf-8").strip())
    else:
        # If `is_git_repo` returns `True`, this should not happen:
        raise RuntimeError
