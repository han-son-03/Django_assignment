from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOFIN_URL)
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def login(request):

    return render(request, 'registration/login.html')


def logout(request):
    return render(request, 'registration/logout.html')