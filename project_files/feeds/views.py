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
from .forms import FeedFolderForm, UserFeedForm, EditUserFeedForm
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

    # Check if a feed already exists with the RSS url, if not create it
    feed, created = Feed.objects.get_or_create(
        url=url
    )

    try:
        rss, rss_channel_data = parse_rss_feed(url)
    except Exception as e:
        raise ValueError("Error in parsing RSS feed: " + str(e))

    # Update the feed object with the rss_channel_data and save it
    save_feed(feed, rss_channel_data)

    # Send a signal to import articles from the feed
    rss_feed_imported.send(sender=import_rss_feed,
                           rss=rss, rss_channel_data=rss_channel_data, feed=feed)

    return feed, created


def save_feed(feed, rss_channel_data):
    feed.link = rss_channel_data.get('link', feed.link)
    feed.name = rss_channel_data.get('title', feed.name)
    feed.description = rss_channel_data.get('description', feed.description)
    feed.image_url = rss_channel_data.get('image_url', feed.image_url)
    feed.ttl = rss_channel_data.get('ttl', feed.ttl)
    feed.last_updated = timezone.now()
    feed.save()


def parse_rss_feed(url):
    try:
        rss = read_rss_feed(url)
    except ValueError as e:
        raise ValueError(f"Error fetching RSS feed: {e}")

    # Parse out relevant information within the 'feed' of the parsed RSS.
    rss_channel_data = read_rss_channel_elements(rss)

    return rss, rss_channel_data


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
    # Get the user model, followed by the user using the user_id
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)

    # If there is a mismatch with the users, do not proceed.
    if request.user != user:
        return HttpResponseForbidden("You are not authorized to view this.")

    # Get the folder
    folder = get_object_or_404(FeedFolder, pk=folder_id)

    # Get all user feeds in the folder
    folder_userfeeds = UserFeed.objects.filter(user=user, folder=folder)

    # If a userfeed was specified by ID, display only that feed.
    if userfeed_id:
        # Find the userfeed associated with that ID and return the articles in it
        userfeed = get_object_or_404(
            UserFeed, user=user, folder=folder, pk=userfeed_id)
        userfeed_articles = Article.objects.filter(feed=userfeed.feed)
    else:
        # If no userfeed ID was present, get all userfeeds within the folder, and return all their articles.
        userfeed = None
        userfeed_articles = Article.objects.filter(
            feed__in=folder_userfeeds.values_list('feed', flat=True))

    # Sort/order the articles by newest first
    userfeed_articles = userfeed_articles.order_by('-publish_datetime')
    return render(request, 'feeds/view_feed.html', {
        'folder': folder,
        'folder_userfeeds': folder_userfeeds,
        'userfeed': userfeed,
        'userfeed_articles': userfeed_articles,
    })


@login_required
def edit_userfeed(request, userfeed_id):
    userfeed = get_object_or_404(UserFeed, id=userfeed_id, user=request.user)

    if request.method == 'POST':
        form = EditUserFeedForm(request.POST, instance=userfeed)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Feed successfully updated.')
            except IntegrityError:
                messages.error(request, 'Failed to update feed.')
        else:
            messages.error(request, 'Failed to update feed.')
    else:
        form = EditUserFeedForm(instance=userfeed)

    return render(request, 'feeds/edit_userfeed.html', {'form': form, 'userfeed_name': userfeed.name})


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
def edit_folder(request, folder_id):
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


@login_required
def delete_userfeed(request, userfeed_id):
    """
    Deletes a user feed with the given userfeed_id (if it belongs to the current user).
    Redirects to the folder that contained the userfeed and displays a deletion confirmation message.
    """
    userfeed = get_object_or_404(UserFeed, id=userfeed_id, user=request.user)

    feed_name = userfeed.name
    feed_folder = userfeed.folder
    userfeed.delete()
    messages.success(request, 'The ' + feed_name +
                     " feed was successfully deleted.")
    return redirect('view_userfeed', user_id=request.user.id, folder_id=feed_folder.id)
