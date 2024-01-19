import json
import requests
from colorama import Fore

def send(webhook_url, content="test"):
    data = {
        "content": content
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200 or 204:
            return True
        else:
            print(f"{Fore.RED}[ERROR] Unexpected status code: {response.status_code}")
            return False

    except Exception:
        print(f"{Fore.RED}[ERROR] Connection error!")
        return False
