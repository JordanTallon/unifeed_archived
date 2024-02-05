# rss_app/views.py
from rest_framework.generics import GenericAPIView

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status 
from .forms import FeedForm
from .models import FeedItem
from .serializers import FeedItemListSerializer
from folder_system.models import Folder
import feedparser

class RssView(GenericAPIView):
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemListSerializer

    def get(self, request):
        name = request.GET.get('folder') 
        if not name:
            return Response({"Error": "please provide folder name in url"}, status=status.HTTP_400_BAD_REQUEST)
        
        feeds = FeedItem.objects.filter(folder__name__icontains=name)
        if not feeds: 
            return Response({"Error": f"couldn't find folder with name {name}"},status=status.HTTP_404_NOT_FOUND)

        return Response(FeedItemListSerializer(feeds).data, status=status.HTTP_200_OK)

def index(request, folder_id=None):
    if request.method == 'POST':
        form = FeedForm(request.POST, folder_id=folder_id)
        if form.is_valid():
            rss_url = form.cleaned_data['rss_url']
            folder_id = form.cleaned_data.get('folder').id if form.cleaned_data.get('folder') else None

            # Use feedparser to parse the RSS feed
            feed = feedparser.parse(rss_url)
            items = feed.entries

            for item in items:
                title = item.title if hasattr(item, 'title') else 'No title'
                description = item.description if hasattr(item, 'description') else 'No description'
                link = item.link if hasattr(item, 'link') else 'No link'

                new_feed = FeedItem(
                    title=title,
                    description=description,
                    link=link,
                    folder_id=folder_id  # Set the folder attribute
                )

                new_feed.save()

    else:
        form = FeedForm(folder_id=folder_id)

    feed_items = FeedItem.objects.all()
    return render(request, 'rss_app/feed_list.html', {'form': form, 'feed_items': feed_items})

def feeds_in_folder(request, folder_id=None):
    form = FeedForm(folder_id=folder_id)

    try:
        if folder_id:
            folder = Folder.objects.get(id=folder_id)
            feeds = FeedItem.objects.filter(folder=folder)
        else:
            folder = None
            feeds = FeedItem.objects.all()

    except Folder.DoesNotExist:
        folder = None
        feeds = []

    return render(request, 'rss_app/feed_list.html', {'form': form, 'folder': folder, 'feed_items': feeds})

def delete_feed(request, feed_id):
    feed_item = get_object_or_404(FeedItem, pk=feed_id)
    feed_item.delete()
    return redirect('feed-list')

def clear_all_feeds(request):
    FeedItem.objects.all().delete()
    return redirect('feed-list')

def add_feed(request):
    form = FeedForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Handle form processing
        rss_url = form.cleaned_data['rss_url']
        folder = form.cleaned_data['folder']

        # Create or save the feed object here

        return redirect('feed_list')  # Redirect to feed list or another appropriate view

    return render(request, 'feed_feed.html', {'form': form})

