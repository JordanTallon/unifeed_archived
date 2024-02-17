from feeds.models import FeedFolder, UserFeed


def global_context(request):
    sidebar_data = {'user_folders': []}

    if request.user.is_authenticated:
        # Get all folders for the current user
        user_folders = FeedFolder.objects.filter(user=request.user)

        # For each folder, get the associated userfeeds
        for folder in user_folders:
            folder_feeds = UserFeed.objects.filter(
                user=request.user, folder=folder)

            # Adding the folder and its feeds to the sidebar data as a pair
            sidebar_data['user_folders'].append({
                'folder': folder,
                'feeds': folder_feeds
            })

    return {
        'sidebar_data': sidebar_data
    }
