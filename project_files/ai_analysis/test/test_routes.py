from django.test import TestCase, Client
from django.urls import reverse
from .factories import PoliticalBiasAnalysisFactory
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

        print(response.content)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

        # Read the content of the response as json.
        response_data = json.loads(response.content.decode('utf-8'))

        # Make sure all 50 models are serialized in the data (batch size in setUp).
        self.assertEqual(len(response_data), 50)
