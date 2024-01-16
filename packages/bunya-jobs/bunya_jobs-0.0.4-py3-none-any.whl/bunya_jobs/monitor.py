import subprocess


def list_my_jobs() -> str:
    """list bunya jobs for the current user logged in
    """
    byte_sdtdout = subprocess.run(['squeue', '--me'], stdout=subprocess.PIPE)
    byte_sdtdout.stdout.decode('utf-8')
