from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
# Create your views here.


def registration(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            # Redirect to the login page after valid registration
            return redirect('/')

    context = {'form': form}
    return render(request, "accounts/registration.html", context)
