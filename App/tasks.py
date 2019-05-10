from celery import shared_task
from django.core.mail import send_mail
from django.template import loader

from axf.settings import EMAIL_HOST_USER, SERVER_HOST

@shared_task
def send_email_activate(username, receive, u_token):

    subject = '%s AXF Activate' % username

    from_email = EMAIL_HOST_USER

    recipient_list = [receive, ]

    data = {
        'username': username,
        'activate_url': 'http://{}/axf/activate/?u_token={}'.format(SERVER_HOST, u_token)
    }

    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject=subject, message="", html_message=html_message, from_email=from_email, recipient_list=recipient_list)
