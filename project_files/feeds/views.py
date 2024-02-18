from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import F
from articles.models import Article
from .models import *
from .forms import FeedFolderForm, UserFeedForm, EditUserFeedForm
from .utils import *
from .serializers import *
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required
def add_user_feed_to_folder(request, folder_name):

    user = request.user
    folder = get_object_or_404(FeedFolder, user=user, name=folder_name)
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
                    feed, _ = import_rss_feed(url)
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, 'feeds/add_new_feed.html', {'form': form, 'folder_name': folder.name})

            if UserFeed.objects.filter(folder=folder, feed=feed).exists():
                messages.error(
                    request, f"The {folder.name} folder already contains this feed.")
                return render(request, 'feeds/add_new_feed.html', {'form': form, 'folder_name': folder.name})

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
                return render(request, 'feeds/add_new_feed.html', {'form': form, 'folder_name': folder.name})
        else:
            messages.error(request, 'Failed to import Feed.')
            return render(request, 'feeds/add_new_feed.html', {'form': form, 'folder_name': folder.name})

    else:  # Not a POST request
        form = UserFeedForm()

    return render(request, 'feeds/add_new_feed.html', {'form': form, 'folder_name': folder.name})


@login_required
def view_folder(request, user_id, folder_id):
    User = get_user_model()

    folder = get_object_or_404(FeedFolder, pk=folder_id)
    user = get_object_or_404(User, pk=user_id)
    userfeeds = UserFeed.objects.filter(user=user, folder=folder)

    if request.user != user:
        return HttpResponseForbidden("You are not authorized to view this folder.")

    repeat_times = range(3)
    return render(request, 'feeds/view_feed.html', {'folder': folder, 'userfeeds': userfeeds})


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
    folder_userfeeds = UserFeed.objects.filter(user=user, folder=folder)
    # To pass for HTML context
    userfeed = None
    if userfeed_id:
        # If a userfeed was specified by ID, render only that feed.
        feeds_to_render = [get_object_or_404(
            UserFeed, user=user, folder=folder, pk=userfeed_id).feed]
        userfeed = feeds_to_render[0]
    else:
        # Render all user feeds in the folder
        feeds_to_render = folder_userfeeds.values_list('feed', flat=True)

    userfeed_articles = Article.objects.filter(
        feed__in=feeds_to_render)

    # Sort/order the articles by newest first
    userfeed_articles = userfeed_articles.order_by(
        F('publish_datetime').desc(nulls_last=True))

    # Check if the request is from HTMX (which only needs an updated article list)
    if request.htmx:
        return render(request, 'global/article_grid.html', {
            'article_list': userfeed_articles,
        })

    return render(request, 'feeds/view_feed.html', {
        'folder_id': folder_id,
        'userfeed_id': userfeed_id,
        'folder': folder,
        'userfeed': userfeed,
        'folder_userfeeds': folder_userfeeds,
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

    return render(request, 'feeds/edit_folder.html', {'form': form, 'folder_name': folder.name, 'folder_id': folder_id})


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
