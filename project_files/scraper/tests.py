from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from scraper.utils import scrape_data


class ScraperViewsTest(TestCase):
    def test_scaper_post_response(self):

        content = scrape_data('https://example.com')

        self.assertIn(
            "This domain is for use in illustrative examples in documents", content)
