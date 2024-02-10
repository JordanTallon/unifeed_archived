from django.test import TestCase
from ..utils import clean_rss_entries
from feeds.utils import read_rss_feed, read_rss_channel_elements


class TestArticleImport(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Note: RSS feeds are unreliable. If this test breaks, check if the RSS feed is the issue first.
        # I have decided to go with this instead of a mock because I want to test the "real" functionality
        # so that this test will fail if the read_rss_feed function breaks. A solution to this may be to
        # maintain multiple rss feeds to fall back on here, so for example: if CNN failed, it could try
        # Fox, then ABC, and so on. It is unlikely all services will fail at once.
        cls.rss = read_rss_feed("http://rss.cnn.com/rss/edition.rss")

    def test_clean_rss_entries(self):
        clean = clean_rss_entries(
            self.rss.entries,
            read_rss_channel_elements(self.rss)
        )

        # Make sure that the cleaned data has at least 1 entry
        self.assertGreater(len(clean), 0, "No entries in cleaned data")

        # Assert that the cleaned rss entries contains all the expected fields
        for entry in clean:
            self.assertIn('title', entry, "Title not in cleaned entry")
            self.assertIn('link', entry, "Link not in cleaned entry")
            self.assertIn('description', entry,
                          "Description not in cleaned entry")
            self.assertIn('image_url', entry, "Image URL not in cleaned entry")
            self.assertIn('author', entry, "Author not in cleaned entry")
            self.assertIn('publish_datetime', entry,
                          "Published datetime not in cleaned entry")
