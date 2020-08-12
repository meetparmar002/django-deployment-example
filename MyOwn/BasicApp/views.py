from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

# imports for login and logout
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def index(request):
    return render(request, 'BasicApp/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'BasicApp/register.html', {'user': user_form, 'profile': profile_form, 'is_registered': registered})


@login_required
def special(request):
    return HttpResponse('You are logged in, Nice!')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'BasicApp/index.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user != None:
            if user.is_active:
                login(request, user)
                # return redirect('special/')
                return HttpResponseRedirect(reverse('BasicApp:special'))
            else:
                return HttpResponse("User is NOT ACTIVE!")
        else:
            print('Someone tried to login and failed!')
            print('Username: {} \n Password: {}'.format(username, password))
            return HttpResponse('Invalid login details or User does not exist')
    else:
        return render(request, 'BasicApp/login.html',{})
