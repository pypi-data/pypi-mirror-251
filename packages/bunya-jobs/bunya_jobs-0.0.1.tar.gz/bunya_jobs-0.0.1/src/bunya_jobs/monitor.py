import subprocess


def list_my_jobs():
    """list bunya jobs
    """
    bunya_command = "queue --me"
    return subprocess.run(bunya_command)
