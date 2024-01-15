from io import BytesIO
from typing import Union

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives

from db_email.models import Email, EmailAlternative, EmailAttachment


class EmailBackend(BaseEmailBackend):

    @staticmethod
    def write_message(message: Union[EmailMessage, EmailMultiAlternatives]):
        email = Email(
            subject=message.subject,
            body=message.body,
            from_email=message.from_email,
            to=message.to,
            cc=message.cc,
            bcc=message.bcc
        )
        email.full_clean()
        email.save()
        if isinstance(message, EmailMultiAlternatives):
            for content, mimetype in message.alternatives:
                email_alternative = EmailAlternative(
                    email=email,
                    content=content,
                    mimetype=mimetype
                )
                email_alternative.full_clean()
                email_alternative.save()
        if message.attachments:
            for filename, content, mimetype in message.attachments:
                fh = BytesIO(content.encode())
                email_attachment = EmailAttachment(
                    email=email,
                    mimetype=mimetype
                )
                email_attachment.full_clean()
                email_attachment.file.save(filename, fh)

    def send_messages(self, email_messages):
        """Write all messages to the stream in a thread-safe way."""
        if not email_messages:
            return
        msg_count = 0
        try:
            for message in email_messages:
                self.write_message(message)
                msg_count += 1
        except Exception:
            if not self.fail_silently:
                raise
        return msg_count
