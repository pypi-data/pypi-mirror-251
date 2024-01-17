from django.conf import settings


def get_email_variables():
    try:
        public_key = settings.MALLGO_PUBLIC_KEY
        private_key = settings.MALLGO_PRIVATE_KEY
    except AttributeError:
        print('MALLGO_PUBLIC_KEY and MALLGO_PRIVATE_KEY are not defined in settings.py')
        public_key = None
        private_key = None
    return {
        'public_key': public_key,
        'private_key': private_key,
    }
