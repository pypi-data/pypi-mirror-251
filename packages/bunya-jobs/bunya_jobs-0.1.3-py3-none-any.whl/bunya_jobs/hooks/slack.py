import requests
import json
from typing import Dict


def send_slack_message(data: Dict[str, str], url: str):
    payload = json.dumps(data)
    headers = {"Content-type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response
