from typing import Any
from django.core.mail.backends.base import BaseEmailBackend
from MallGoEmail.send import send_email
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.message import sanitize_address, DEFAULT_ATTACHMENT_MIME_TYPE


class MallGoEmailBackend(BaseEmailBackend):
    delivery_result = None

    def __init__(self, fail_silently: bool = ..., **kwargs: Any) -> None:
        super(MallGoEmailBackend, self).__init__(fail_silently=fail_silently, **kwargs)
        try:
            from django.conf import settings
            self.auth_key = settings.MALLGO_AUTH_KEY
            self.separate_recipients = getattr(settings, "MALLGO_SEPARATE_RECIPIENTS", True)
        except:
            raise ImproperlyConfigured('MALLGO_AUTH_KEY is not defined in settings.py')

    def _send_mallgo_email(self, message):
        email_data = {
            "from_email": message.from_email,
            "subject": message.subject,
            "reply_to": message.reply_to,
            "body": message.body,
            "template": message.template if hasattr(message, 'template') else None,
            "template_vars": message.template_vars if hasattr(message, 'template_vars') else None,
        }
        # Add HTML body if exists
        if getattr(message, 'alternatives', None) is None:
            message.alternatives = []
        for alt in message.alternatives:
            content, mimetype = alt
            if mimetype == 'text/html':
                email_data['body'] = content
                email_data['body_text'] = message.body
                break
        if self.separate_recipients:
            emails = []
            for email in message.recipients():
                current_data = email_data.copy()
                current_data['to'] = [email]
                emails.append(send_email(current_data, self.auth_key))
            message.mallgo_response = emails
            return emails
        else:
            email_data['to'] = message.to
            email_data['cc'] = message.cc
            email_data['bcc'] = message.bcc
            message.mallgo_response = [send_email(email_data, self.auth_key)]
            return message.mallgo_response

    def send_messages(self, email_messages):
        results = []
        for message in email_messages:
            email_result = self._send_mallgo_email(message)
            if isinstance(email_result, list):
                results.extend(email_result)
            else:
                results.append(email_result)
        self.delivery_result = results
        return True

    def send_message(self, email_message):
        return self.send_messages([email_message])
