from celery import shared_task
from .models import Feed
from datetime import timedelta
from django.utils import timezone
from .utils import import_rss_feed


@shared_task
def update_all_feeds():
    feeds = Feed.objects.all()
    # Current time
    now = timezone.now()

    for feed in feeds:
        # Next update is due at the feeds last update + its time to live
        next_update_due = feed.last_updated + timedelta(minutes=feed.ttl)

        if now >= next_update_due:
            print("Updating Feed", feed.name)
            print(feed.last_updated)
            print(feed.last_updated + timedelta(minutes=feed.ttl))
            print(now)
            try:
                import_rss_feed(feed.url)
                print("Update succesful")
            except Exception as e:
                print(f"Failed to update feed {feed.id}: {e}")
