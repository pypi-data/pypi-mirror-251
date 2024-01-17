from django.core.mail import EmailMessage


class MallGoEmailMessage(EmailMessage):
    def __init__(self, *args, template=None, template_vars={}, **kwargs):
        self.connection = None
        self.template = template
        self.template_vars = template_vars
        super().__init__(*args, **kwargs)

    def send(self, fail_silently=False):
        from MallGoEmail.backend import MallGoEmailBackend
        if not self.connection:
            self.connection = MallGoEmailBackend(fail_silently=fail_silently)
        return self.connection.send_messages([self])
