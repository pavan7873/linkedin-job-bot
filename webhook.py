import requests,os
from dotenv import load_dotenv
    

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def trigger_n8n(summary):

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=summary,
            timeout=30
        )

        print(f"Webhook Status : {response.status_code}")
        print(response.text)

    except Exception as e:
        print(f"Webhook Error : {e}")

