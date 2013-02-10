from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['email'], request.POST['email'], '')
        user.is_active = False;
        user.save()
    return HttpResponseRedirect('/')
