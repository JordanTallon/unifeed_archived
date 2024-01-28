from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse


class ScraperViewsTest(TestCase):
    def test_scaper_post_response(self):
        response = self.client.post(
            reverse('scrape'), {'url': 'https://example.com'})

        content = response.json()['content']

        self.assertIn(
            "This domain is for use in illustrative examples in documents", content)
