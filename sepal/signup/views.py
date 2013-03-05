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
            opts = {
            	'user': user
            }   
            form.save(**opts)         
    return HttpResponseRedirect('/')
