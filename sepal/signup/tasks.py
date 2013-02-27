from celery import task
from django.core.mail import send_mail
from sepal.settings import EMAIL_HOST_USER 

@task()
def send_request_email(user, *args, **kwargs):
    send_mail('New Signup Invite Request by {}'.format(user.email),
                    'A new user requested beta signup for sepal. Go here to set them a password ' +
                    'and then send them an email.\n http://sepalbio.com/admin/auth/user/'+str(user.id)+'/', 
                    EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False)