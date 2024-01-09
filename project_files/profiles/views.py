from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from .models import UserProfile
from .forms import UserProfileForm

class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profiles/profile_info.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.username

user_profile = UserProfileView.as_view()


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user.username

user_profile_update = UserProfileUpdateView.as_view()

