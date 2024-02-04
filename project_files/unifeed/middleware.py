from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


# Guard 'every' page, unless whitelisted here
# Most of UniFeed's features require the user to have an account
# The majority of pages need to be guarded, this middleware automatically guards them.
def RequireLoginMiddleware(get_response):

    def middleware(request):
        response = get_response(request)

        # Ignore this middleware logic when it is called by a unit test
        # This ensures that the unit tests can cover the whole website without needing to be user authenticated
        if settings.TESTING:
            return response

        # List of 'public/whitelisted' paths (don't require user login)
        public_paths = [
            reverse('login'),
            reverse('register')
        ]

        only_public_paths = [
            reverse('login'),
            reverse('register')
        ]

        # If the user isn't logged in
        if not request.user.is_authenticated:
            # And the path they are trying to view isn't in the 'public_paths' list
            if request.path not in public_paths:
                # Redirect them to the login page
                return redirect(settings.LOGIN_URL)
        # If instead, the user is authenticated
        else:
            # And they are trying to view a 'only_public' path
            if request.path in only_public_paths:
                # Redirect them to the home page
                # This prevents already logged in users from 'logging in' or making another account
                return redirect('home')

        return response

    return middleware

# Note: https://docs.djangoproject.com/en/5.0/topics/http/middleware/
