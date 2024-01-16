import subprocess


def list_my_jobs() -> str:
    """list bunya jobs for the current user logged in
    """
    return subprocess.run(['squeue', '--me'], stdout=subprocess.PIPE)
