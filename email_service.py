import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

from config import DEPARTMENT_EMAILS


load_dotenv()


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(
    recipient_email: str,
    subject: str,
    body: str,
) -> tuple[bool, str]:
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        return False, "SMTP credentials are missing."

    if not recipient_email:
        return False, "Recipient email is missing."

    message = EmailMessage()
    message["From"] = SMTP_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=30,
        ) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()

            server.login(
                SMTP_EMAIL,
                SMTP_PASSWORD,
            )

            server.send_message(message)

        return True, "Email sent successfully."

    except Exception as error:
        return False, str(error)
def send_department_notification(
    ticket_id: str,
    complaint: str,
    location: str,
    student_email: str,
    category: str,
    priority: str,
    department: str,
    summary: str,
) -> tuple[bool, str]:
    department_email = DEPARTMENT_EMAILS.get(department)

    if not department_email:
        return (
            False,
            f"No email address configured for {department}.",
        )

    subject = (
        f"New Complaint Assigned - {ticket_id}"
    )

    body = f"""
Dear {department},

A new complaint has been analysed and assigned to your department.

Ticket ID: {ticket_id}

Student Email: {student_email}

Category: {category}

Priority: {priority}

Location: {location or "Not provided"}

Complaint:
{complaint}

Summary:
{summary}

Current Status: New

Please review the complaint and take the necessary action.

Regards,
ResolveAI
"""

    return send_email(
        recipient_email=department_email,
        subject=subject,
        body=body,
    )

def send_resolution_notification(
    ticket_id: str,
    student_email: str,
    complaint: str,
    department: str,
) -> tuple[bool, str]:
    subject = f"Complaint Resolved - {ticket_id}"

    body = f"""
Dear Student,

Your complaint has been resolved.

Ticket ID: {ticket_id}

Complaint:
{complaint}

Department:
{department}

Status:
Resolved

Please contact the concerned department if the issue still persists.

Regards,
ResolveAI
"""

    return send_email(
        recipient_email=student_email,
        subject=subject,
        body=body,
    )