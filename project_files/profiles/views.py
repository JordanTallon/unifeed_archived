from .forms import UserProfileForm
from django.shortcuts import render, redirect


def UserProfile(request):
    # This is just adapted from the register form system
    # To be changed later.
    form = UserProfileForm()

    if request.method == "POST":
        form = UserProfileForm(request.POST)

        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, "profiles/profile_update.html", context)
