from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def account_register(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            # Redirect to the login page after valid registration
            return redirect(reverse('login'))

    context = {'form': form}
    return render(request, "accounts/register.html", context)


def account_login(request):

    form = UserLoginForm()

    if request.method == "POST":
        form = UserLoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the home page after succesful login
                return redirect(reverse('home'))

    context = {'form': form}
    return render(request, "accounts/login.html", context)


def account_logout(request):
    logout(request)
    return redirect(reverse('home'))
