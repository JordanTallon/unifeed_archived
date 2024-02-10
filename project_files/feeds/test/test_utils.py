from django.test import TestCase
from ..utils import read_rss_feed


class RssFeedImportTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Note: RSS feeds are unreliable. If this test breaks, check if the RSS feed is the issue first.
        # I have decided to go with this instead of a mock because I want to test the "real" functionality
        # so that this test will fail if the read_rss_feed function breaks. A solution to this may be to
        # maintain multiple rss feeds to fall back on here, so for example: if CNN failed, it could try
        # Fox, then ABC, and so on. It is unlikely all services will fail at once.
        cls.rss = read_rss_feed("http://rss.cnn.com/rss/edition.rss")

    def test_read_rss_entries(self):
        # Assert that a feed was returned by the read_rss_feed function
        self.assertTrue(
            self.rss.entries, "No entries were returned by the RSS feed.")

    def test_read_rss_feed(self):
        # Assert that a feed was returned by the read_rss_feed function
        self.assertTrue(
            self.rss.feed, "No feed (channel elements) could be read from the RSS feed.")
