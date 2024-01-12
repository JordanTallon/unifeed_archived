from django.test import TestCase, Client
from django.urls import reverse
from .factories import PoliticalBiasAnalysisFactory
from ..models import PoliticalBiasAnalysis
import json


class test_political_bias_analysis_api_routes(TestCase):
    def setUp(self):
        self.client = Client()
        # Add 50 instances of the PoliticalBiasAnalysis model with dummy data (see factories.py)
        PoliticalBiasAnalysisFactory.create_batch(50)

    def test_detect_political_bias_api_get_exists(self):
        # Create a GET request.
        response = self.client.get(reverse('get-political-bias'))
        self.assertEqual(response.status_code, 200)

    def test_detect_political_bias_get_returns_serialized_data(self):
        # Create a GET request.
        response = self.client.get(reverse('get-political-bias'))

        self.assertEqual(response.status_code, 200)

        # Read the content of the response as json.
        response_data = json.loads(response.content.decode('utf-8'))

        # Make sure all 50 models are serialized in the data (batch size in setUp).
        self.assertEqual(len(response_data), 50)

    def test_detect_political_bias_api_post_exists(self):
        # Create a POST request.
        response = self.client.post(reverse('add-political-bias'))
        self.assertEqual(response.status_code, 200)

    def test_detect_political_bias_api_post_new_data(self):
        # Get the count of objects before new addition
        length = len(PoliticalBiasAnalysis.objects.all())

        # Data for the new model
        data = {
            'article_url': 'www.example.com',
            'article_text_md5': '1234123',
            'political_bias': 100
        }

        # Post the data to the url
        response = self.client.post(reverse('add-political-bias'), data=data)

        # 201 = created
        self.assertEqual(response.status_code, 201)

        # Check if the objects contain the newly posted object (length + 1)
        new_length = len(PoliticalBiasAnalysis.objects.all())
        self.assertEqual(new_length, length + 1)
