import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


MAIL_USERNAME = os.getenv(
    "MAIL_USERNAME"
)

MAIL_PASSWORD = os.getenv(
    "MAIL_PASSWORD"
)


def send_email(
    receiver_email: str,
    subject: str,
    body: str
):

    message = MIMEMultipart()

    message["From"] = MAIL_USERNAME
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        MAIL_USERNAME,
        MAIL_PASSWORD
    )

    server.sendmail(
        MAIL_USERNAME,
        receiver_email,
        message.as_string()
    )

    server.quit()