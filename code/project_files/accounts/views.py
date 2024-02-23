from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, AccountSettingsForm


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
                # Redirect to the reading list after succesful login
                return redirect(reverse('reading_list'))

    context = {'form': form}
    return render(request, "accounts/login.html", context)


@login_required
def account_settings(request):
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account settings successfully updated.')
            return redirect('account_settings')
    else:
        form = AccountSettingsForm(instance=request.user)

    return render(request, 'accounts/settings.html', {'form': form})


def account_logout(request):
    logout(request)
    return redirect(reverse('reading_list'))
