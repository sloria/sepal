from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from sepal.signup.tasks import send_request_email

from sepal.signup.forms import SignupForm

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create an inactive new user
            user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], '')
            user.is_active = False
            user.save()
            # Send an email to notify admin of the new request
            send_request_email.delay(user)
    return HttpResponseRedirect('/')
