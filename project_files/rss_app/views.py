# rss_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedForm
from .models import FeedItem
from folder_system.models import Folder
import feedparser

def index(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            rss_url = form.cleaned_data['rss_url']
            folder_id = form.cleaned_data.get('folder')

            # Use feedparser to parse the RSS feed
            feed = feedparser.parse(rss_url)
            items = feed.entries

            for item in items:
                new_feed = FeedItem(
                    title=item.title,
                    description=item.summary,
                    link=item.link,
                )

                if folder_id:
                    folder = Folder.objects.get(pk=folder_id)
                    new_feed.folder = folder

                new_feed.save()

    else:
        form = FeedForm()

    feed_items = FeedItem.objects.all()
    return render(request, 'rss_app/feed_list.html', {'form': form, 'feed_items': feed_items})

def feeds_in_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    feed_items = FeedItem.objects.filter(folder=folder)
    return render(request, 'rss_app/feeds_in_folder.html', {'folder': folder, 'feed_items': feed_items})

def delete_feed(request, feed_id):
    feed_item = get_object_or_404(FeedItem, pk=feed_id)
    feed_item.delete()
    return redirect('feed-list')
