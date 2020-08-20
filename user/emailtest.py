from django.core.mail.message import EmailMessage

def send_email():
    subject = "message"
    to = ['id@gmail.com']
    from_email = 'id@gmail.com'
    message = "Successful message transmission"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
