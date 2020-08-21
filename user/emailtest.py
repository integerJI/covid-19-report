from django.core.mail.message import EmailMessage

def send_email():
    subject = "message"
    to = ["jjs9536@gmail.com"]
    from_email = "kodag.developer@gmail.com"
    message = "메지시 테스트 222222"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
