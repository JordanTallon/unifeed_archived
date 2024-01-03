from django.shortcuts import render
from .forms import UserRegistrationForm
# Create your views here.


def registration(request):
    form = UserRegistrationForm()
    context = {'form': form}
    return render(request, "accounts/registration.html", context)
