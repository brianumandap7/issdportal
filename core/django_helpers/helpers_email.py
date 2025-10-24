from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from email.utils import formataddr

#===============================================================================================
#WITHOUT ATTACHEDMENT AND EMAIL FROM NAME
#===============================================================================================
def send_custom_email(subject, message, recipient_list, from_email=None, fail_silently=False):
    """
    Helper to send email in Django.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=fail_silently,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
#===============================================================================================
#WITHOUT ATTACHEDMENT AND WITH EMAIL FROM NAME
#===============================================================================================
def send_custom_email_name(subject, message, recipient_list, from_email=None, from_name=None, fail_silently=False):
    """
    Helper to send email in Django with optional sender name.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # Add sender name if provided
    if from_name:
        from_email = formataddr((from_name, from_email))

    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=fail_silently,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
#===============================================================================================
#WITH ATTACHEDMENT AND EMAIL FROM NAME
def send_email_with_attachment_name(
    subject,
    body,
    recipient_list,
    from_name=None,
    from_email=None,
    attachments=None,
    fail_silently=False,
    html=False
):
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # Add sender name if provided
    if from_name:
        from_email = formataddr((from_name, from_email))

    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=recipient_list,
        )

        if html:
            email.content_subtype = "html"

        if attachments:
            for attachment in attachments:
                if isinstance(attachment, str):
                    email.attach_file(attachment)
                elif isinstance(attachment, tuple) and len(attachment) == 3:
                    email.attach(*attachment)

        email.send(fail_silently=fail_silently)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
#===============================================================================================
def send_email_with_attachment(
    subject,
    body,
    recipient_list,
    from_email=None,
    attachments=None,
    fail_silently=False,
    html=False
):
    """
    Send email with optional attachments.
    
    :param subject: Email subject
    :param body: Email body (plain text or HTML)
    :param recipient_list: List of recipients
    :param from_email: Optional from email
    :param attachments: List of file paths or (filename, content, mimetype) tuples
    :param html: If True, send HTML email
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=recipient_list,
        )

        # If HTML email
        if html:
            email.content_subtype = "html"

        # Handle attachments
        if attachments:
            for attachment in attachments:
                if isinstance(attachment, str):
                    # File path
                    email.attach_file(attachment)
                elif isinstance(attachment, tuple) and len(attachment) == 3:
                    # (filename, content, mimetype)
                    email.attach(*attachment)

        email.send(fail_silently=fail_silently)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
#===============================================================================================
