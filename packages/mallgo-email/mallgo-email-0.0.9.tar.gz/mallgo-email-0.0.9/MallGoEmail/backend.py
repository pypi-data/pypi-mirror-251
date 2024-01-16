from typing import Any
from django.core.mail.backends.base import BaseEmailBackend
from MallGoEmail.send import send_email
from django.core.exceptions import ImproperlyConfigured


class MallGoEmailBackend(BaseEmailBackend):

    def __init__(self, fail_silently: bool = ..., **kwargs: Any) -> None:
        super(MallGoEmailBackend, self).__init__(fail_silently=fail_silently, **kwargs)
        try:
            from django.conf import settings
            self.auth_key = settings.MALLGO_AUTH_KEY
        except:
            raise ImproperlyConfigured('MALLGO_AUTH_KEY is not defined in settings.py')

    def send_messages(self, email_messages):
        for message in email_messages:
            mail = send_email(message, self.auth_key)
            if not mail:
                return False
        return True

    def send_message(self, email_message):
        return self.send_messages([email_message])
