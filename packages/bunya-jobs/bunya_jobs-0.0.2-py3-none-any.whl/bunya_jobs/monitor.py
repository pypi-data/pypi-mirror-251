import subprocess


def list_my_jobs():
    """list bunya jobs
    """
    bunya_command = "squeue --me"
    return subprocess.run(bunya_command)
