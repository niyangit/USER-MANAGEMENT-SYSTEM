import os
import requests

BREVO_API_KEY = os.getenv(
    "BREVO_API_KEY"
)

SENDER_EMAIL = os.getenv(
    "MAIL_USERNAME"
)


def send_email(
    receiver_email: str,
    subject: str,
    body: str
):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "User Management System",
            "email": SENDER_EMAIL
        },
        "to": [
            {
                "email": receiver_email
            }
        ],
        "subject": subject,
        "textContent": body
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20
    )

    if response.status_code not in [200, 201]:
        raise Exception(
            f"Brevo Error: {response.text}"
        )