"""
This handles sending the approved email. Defaults to dry-run (prints instead of
sending) until real SMTP credentials are configured and DRY_RUN=false.
"""

import smtplib
from email.mime.text import MIMEText

from src.email_agent import config


def send_email(recipient: str, subject: str, body: str) -> None:
    if config.DRY_RUN:
        _dry_run_send(recipient, subject, body)
    else:
        _real_send(recipient, subject, body)


def _dry_run_send(recipient: str, subject: str, body: str) -> None:
    print("\n[DRY RUN — no email actually sent]")
    print(f"To:      {recipient}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}\n")


def _real_send(recipient: str, subject: str, body: str) -> None:
    if not all([config.SMTP_HOST, config.SMTP_USERNAME, config.SMTP_PASSWORD]):
        raise RuntimeError(
            "SMTP credentials are not configured. Set SMTP_HOST, SMTP_USERNAME, "
            "and SMTP_PASSWORD environment variables, or keep EMAIL_DRY_RUN=true."
        )

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = config.SMTP_USERNAME
    message["To"] = recipient

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_USERNAME, [recipient], message.as_string())

    print(f"\n[SENT] Email delivered to {recipient}\n")