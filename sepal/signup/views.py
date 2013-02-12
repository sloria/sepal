from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail

from sepal.signup.forms import SignupForm
from sepal.settings import EMAIL_HOST_USER 

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], '')
            user.is_active = False;
            user.save()
            send_mail('New Signup Invite Request by '+user.email, 'A new user requested beta signup for sepal. Go here to set them a password and then send them an email.\n http://sepalbio.com/admin/auth/user/'+str(user.id)+'/', EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False)
    return HttpResponseRedirect('/')
