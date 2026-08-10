import requests,os
from dotenv import load_dotenv
from datetime import datetime

def log(msg):
    with open(r"C:\Users\pavan\Projects\linkedin-job-bot\debug.txt", "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def trigger_n8n(summary):

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=summary,
            timeout=30
        )

        log(f"Webhook Status : {response.status_code}")
        log(response.text)

    except Exception as e:
        log(f"Webhook Error : {e}")

