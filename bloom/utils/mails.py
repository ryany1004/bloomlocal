from django.core.mail.message import EmailMessage


def send_email(subject: str, message: str, from_email: str = None, recipient_list: list = None, bcc: list = None, **kwargs):
    from django.conf import settings
    if not from_email:
        from_email = settings.FROM_EMAIL_DEFAULT
    if not recipient_list:
        recipient_list = []
    if not bcc:
        bcc = []

    msg = EmailMessage(
        subject=subject, body=message, from_email=from_email,
        to=recipient_list, bcc=bcc, **kwargs
    )
    msg.content_subtype = "html"
    msg.send(fail_silently=True)
