from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from scraper.utils import scrape_data


class ScraperViewsTest(TestCase):
    def test_scaper_succesful_response(self):

        content = scrape_data('https://example.com')

        self.assertIn(
            "This domain is for use in illustrative examples in documents", content)

    def test_scaper_bad_url_response(self):

        with self.assertRaises(ValueError):
            scrape_data('1')

    def test_scaper_non_existent_url_response(self):

        with self.assertRaises(ValueError):
            scrape_data('https://www.ca326unifeedprojecttesting.com/')
