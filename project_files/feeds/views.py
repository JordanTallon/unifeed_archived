from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from articles.models import Article
from .models import *
from .forms import FeedFolderForm, UserFeedForm
from .utils import *
from .serializers import *
from .signals import rss_feed_imported
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages


def import_rss_feed(url):

    # Verify that the 'url' param contained a genuine URL
    validate = URLValidator()
    try:
        validate(url)
    except:
        raise ValueError("Invalid URL.")

    # Check if the feed already exists, return it if so.
    existing_feed = Feed.objects.filter(url=url).first()
    if existing_feed:
        return existing_feed

    try:
        rss = read_rss_feed(url)
    except ValueError as e:
        raise ValueError(f"Error fetching RSS feed: {e}")

    if not rss:
        raise ValueError("Unable to import an RSS feed for the given URL")

    # Feedparse marks the rss as 'bozo' if the url contains incorrect rss data
    if rss.bozo:
        raise ValueError("Unable to parse an RSS feed at the given URL")

    # Parse out relevant information within the 'feed' of the parsed RSS.
    rss_channel_data = read_rss_channel_elements(rss)

    feed = Feed.objects.create(
        url=url,
        link=rss_channel_data.get('link'),
        name=rss_channel_data.get('title'),
        description=rss_channel_data.get('description'),
        image_url=rss_channel_data.get('image_url'),
        ttl=rss_channel_data.get('ttl'),
    )

    feed.save()

    rss_feed_imported.send(sender=import_rss_feed,
                           rss=rss, rss_channel_data=rss_channel_data, feed=feed)

    return feed


@api_view(['POST'])
@login_required
def import_new_feed(request):

    data = request.data

    # Check if a 'url' param was even given in the request data
    url = data.get('url')

    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        feed = import_rss_feed(url)
        serialized_feed = FeedSerializer(feed).data
        return Response({"message": "RSS Feed imported successfully.", "Imported Feed": serialized_feed}, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def add_user_feed_to_folder(request, folder_name):

    if request.method == "POST":
        form = UserFeedForm(request.POST)

        if form.is_valid():

            feed = form.cleaned_data.get('feed')

            # If there's no feed, there but me be a url
            if not feed:
                try:
                    url = form.cleaned_data.get('url')
                    # Check if the feed is valid or already in the database (can reuse it from another user).
                    # If not, the function creates it.
                    feed = import_rss_feed(url)
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, 'feeds/add_new_feed.html', {'form': form})

            user = request.user
            folder = get_object_or_404(FeedFolder, name=folder_name)

            if UserFeed.objects.filter(folder=folder, feed=feed).exists():
                messages.error(
                    request, f"The {folder.name} folder already contains this feed.")
                return render(request, 'feeds/add_new_feed.html', {'form': form})

            try:
                new_user_feed = form.save(commit=False)
                new_user_feed.feed = feed
                new_user_feed.user = user
                new_user_feed.folder = folder
                new_user_feed.save()

                messages.success(request, 'New feed successfully imported.')
                return redirect('view_userfeed', user_id=request.user.id, folder_id=folder.id, userfeed_id=new_user_feed.id)

            except ValueError as e:
                messages.error(request, str(e))
                return render(request, 'feeds/add_new_feed.html', {'form': form})
        else:
            messages.error(request, 'Failed to import Feed.')
            return render(request, 'feeds/add_new_feed.html', {'form': form})

    else:  # Not a POST request
        form = UserFeedForm()

    return render(request, 'feeds/add_new_feed.html', {'form': form})


@login_required
def view_folder(request, user_id, folder_id):
    User = get_user_model()

    folder = get_object_or_404(FeedFolder, pk=folder_id)
    user = get_object_or_404(User, pk=user_id)
    userfeeds = UserFeed.objects.filter(user=user, folder=folder)

    if request.user != user:
        return HttpResponseForbidden("You are not authorized to view this folder.")

    repeat_times = range(3)
    return render(request, 'feeds/view_feed.html', {'folder': folder, 'userfeeds': userfeeds, 'repeat': repeat_times})


@login_required
def view_userfeed(request, user_id, folder_id,  userfeed_id=None):
    User = get_user_model()

    folder = get_object_or_404(FeedFolder, pk=folder_id)
    user = get_object_or_404(User, pk=user_id)
    folder_userfeeds = UserFeed.objects.filter(user=user, folder=folder)

    if request.user != user:
        return HttpResponseForbidden("You are not authorized to view this folder.")

    # If an ID was present
    if userfeed_id:
        # Find the userfeed associated with that ID and return the articles in it
        userfeed = get_object_or_404(
            UserFeed, user=user, folder=folder, pk=userfeed_id)
        userfeed_articles = Article.objects.filter(feeds__in=[userfeed.feed])
    else:
        # If no userfeed ID was present, get all userfeeds within the folder, and return all their articles.
        userfeed = None
        userfeed_articles = Article.objects.filter(
            feeds__in=folder_userfeeds.values_list('feed', flat=True))

    return render(request, 'feeds/view_feed.html', {
        'folder': folder,
        'folder_userfeeds': folder_userfeeds,
        'userfeed': userfeed,
        'userfeed_articles': userfeed_articles,
    })


@login_required
def add_new_folder(request):
    if request.method == 'POST':
        form = FeedFolderForm(request.POST)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.user = request.user
            try:
                new_folder.save()
                return redirect('view_userfeed', user_id=request.user.id, folder_id=new_folder.id)
            except IntegrityError:
                messages.error(
                    request, 'A folder with that name already exists.')
        else:
            messages.error(request, 'Failed to add new folder,')
    else:
        form = FeedFolderForm()

    return render(request, 'feeds/add_new_folder.html', {'form': form})


@login_required
def edit_existing_folder(request, folder_id):
    folder = get_object_or_404(FeedFolder, id=folder_id, user=request.user)

    if request.method == 'POST':
        form = FeedFolderForm(request.POST, instance=folder)
        if form.is_valid():
            try:
                form.save()
                return redirect('view_userfeed', user_id=request.user.id, folder_id=folder.id)
            except IntegrityError:
                messages.error(
                    request, 'A folder with that name already exists.')
        else:
            messages.error(request, 'Failed to update folder.')
    else:
        form = FeedFolderForm(instance=folder)

    return render(request, 'feeds/edit_existing_folder.html', {'form': form, 'folder_name': folder.name, 'folder_id': folder_id})


@login_required
def delete_folder(request, folder_id):
    """
    Deletes a folder with the given folder_id (if it belongs to the current user).
    Redirects to the home page and displays a deletion confirmation message.
    """
    folder = get_object_or_404(FeedFolder, id=folder_id, user=request.user)

    folder_name = folder.name
    folder.delete()
    messages.success(request, 'The ' + folder_name +
                     " folder was successfully deleted.")
    return redirect('home')
