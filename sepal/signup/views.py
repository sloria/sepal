from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from sepal.signup.tasks import send_request_email

from sepal.signup.forms import SignupForm

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if not user_exists(form.cleaned_data['email']):
                # Create an inactive new user
                user = User.objects.create_user(form.cleaned_data['email'], 
                                                form.cleaned_data['email'], '')
                user.is_active = False
                user.save()
                # Send an email to notify admin of the new request
                send_request_email.delay(user)
                messages.success(request, 'Your invite request was sent. \
                Thank you for your interest in Sepal!')
            else:
                # Don't allow multiple requests from the same email
                messages.warning(request, 'An account already exists or an \
                    invite request has already been submitted from this e-mail. \
                    If you are receiving this message in error, please contact \
                    sepalproject@gmail.com.')

    return HttpResponseRedirect('/')

def user_exists(username):
    if User.objects.filter(username=username).count():
        return True
    return False
