import subprocess


def list_my_jobs():
    """list bunya jobs
    """
    byte_sdtdout = subprocess.run(['squeue', '--me'], stdout=subprocess.PIPE)
    return byte_sdtdout.stdout.decode('utf-8')
