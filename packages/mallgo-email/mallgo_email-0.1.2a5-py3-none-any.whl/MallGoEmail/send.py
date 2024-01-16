import requests
import logging

logger = logging.getLogger(__name__)


def send_email(data, auth_key):
    if auth_key is None:
        logger.error('MALLGO_AUTH_KEY is not defined in settings.py')
        return False
    body = {
        "headers": {
            'Authorization': auth_key
        }, "body": {
            'from_email': data.from_email,
            'to_email': data.to,
            'cc_email': data.cc,
            'bcc_email': data.bcc,
            'subject': data.subject,
            'body': data.body,
        }
    }
    if data.template is not None:
        body['body']['template_id'] = data.template
        if data.template_vars is not None:
            body['body']['template_vars'] = data.template_vars
        else:
            body['body']['template_vars'] = {}
    url = 'https://api.email.mallgo.co/send-email/'
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, json=body, headers=headers)
    logger.debug(response.content)
    if response.status_code != 200:
        logger.error("MallGo could not send the email, endpoint response: %s" % response.content)
        return False
    # TODO Return the uuid of the email sent
    logger.debug("Email sent successfully %s" % response.content)
    return True
