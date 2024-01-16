import subprocess
import pandas as pd
import schedule
import time
import os
from typing import Optional
from .hooks.slack import send_slack_message
from .utils.data_processing import stdout_to_dataframe


JOB_FOLDER = "jobs"
JOB_FILE = "latest.csv"
JOB_FILE_PATH = os.path.join(JOB_FOLDER, JOB_FILE)
URL = (
    "https://hooks.slack.com/services/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"
)


def list_user_jobs() -> pd.DataFrame:
    """_summary_ list current jobs of mine

    Returns:
        pd.DataFrame: dataframe of current sbatch job details
    """
    stdout = subprocess.run(["squeue", "--me"], capture_output = True, text = True )
    return stdout_to_dataframe(stdout)


def get_last_monitored_jobs() -> Optional[pd.DataFrame]:
    """_summary_

    Returns:
        pd.DataFrame: dataframe of current sbatch job details
    """
    if os.path.exists(JOB_FILE_PATH):
        return pd.read_csv(JOB_FILE_PATH)
    else:
        return None


def monitor_my_jobs():
    """monitor all jobs"""
    if get_last_monitored_jobs():
        last_monitored_jobs = get_last_monitored_jobs()
        current_jobs = list_user_jobs()
        if last_monitored_jobs != current_jobs:
            diff = pd.concat([last_monitored_jobs, current_jobs]).drop_duplicates(
                keep=False
            )
            try:
                send_slack_message(data=diff.to_dict(), url=URL)
            except Exception as e:
                raise BaseException(
                    "an error occurred while trying to send job completed to slack",
                    str(e),
                )
    else:
        list_user_jobs().to_csv(JOB_FILE_PATH)


def schedule_monitor():
    schedule.every(1).minutes.do(monitor_my_jobs)

    while True:
        schedule.run_pending()
        time.sleep(1)
