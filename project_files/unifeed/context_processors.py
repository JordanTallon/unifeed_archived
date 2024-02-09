from feeds.models import FeedFolder


def global_context(request):

    if request.user.is_authenticated:
        # Get all folders for the current user
        user_folders = FeedFolder.objects.filter(user=request.user)
    else:
        user_folders = []

    return {
        'sidebar_data': {
            'user_folders': user_folders,
        }
    }
