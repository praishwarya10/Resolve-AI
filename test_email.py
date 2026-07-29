from email_service import send_email


success, message = send_email(
    recipient_email="forprojectsdummyacc@gmail.com",
    subject="ResolveAI SMTP Test",
    body=(
        "This is a test email from the "
        "ResolveAI complaint system."
    ),
)

print("Success:", success)
print("Message:", message)