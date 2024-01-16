from typing import Any
from django.core.mail.backends.base import BaseEmailBackend
from MallGoEmail.send import send_email
from django.core.exceptions import ImproperlyConfigured


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

    def send_messages(self, email_messages):
        results = []
        for message in email_messages:
            email_result = send_email(message, self.auth_key)
            results.append(email_result)
        self.delivery_result = results
        return True

    def send_message(self, email_message):
        email_data = {
            "from_email": email_message.from_email,
            "subject": email_message.subject,
            "body": email_message.body,
            "template": email_message.template,
            "template_vars": email_message.template_vars,
        }
        if self.separate_email_addresses:
            emails = []
            for email in email_message.recipients():
                current_data = email_data.copy()
                current_data['to'] = email
            return self.send_messages(emails)
        else:
            email_data['to'] = email_message.to
            email_data['cc'] = email_message.cc
            email_data['bcc'] = email_message.bcc
            return self.send_messages([email_data])
