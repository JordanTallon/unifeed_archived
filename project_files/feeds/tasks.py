from celery import shared_task
from .models import Feed
from datetime import timedelta
from django.utils import timezone


@shared_task
def update_all_feeds():
    feeds = Feed.objects.all()
    # Current time
    now = timezone.now()

    for feed in feeds:
        # Next update is due at the feeds last update + its time to live
        next_update_due = feed.last_update + timedelta(minutes=feed.ttl)

        if now >= next_update_due:
            try:
                update_rss_feed(feed.id)
            except Exception as e:
                print(f"Failed to update feed {feed.id}: {e}")
