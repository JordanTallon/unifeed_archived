from django.test import TestCase, Client
from django.urls import reverse
from .factories import ArticleAnalysisResultsFactory
from ..models import BiasAnalysis, ArticleAnalysisResults
import json


""" class test_political_bias_analysis_api_routes(TestCase):
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
 """


class test_political_bias_analysis_data_creation(TestCase):
    def test_detect_political_bias_api_post_exists(self):
        # Check if POST request is allowed.
        response = self.client.options(reverse('analyse-political-bias'))
        self.assertIn('POST', response['Allow'])

    def test_detect_political_bias_api_post_new_data(self):
        # Get the count of analysis request objects before new addition
        length = len(BiasAnalysis.objects.all())

        # Data for the new model
        data = {
            'url': 'http://www.example.com',
            'status': 'processing'
        }

        # Post the data to the url
        response = self.client.post(
            reverse('analyse-political-bias'), data=data)

        # 202 = accepted
        self.assertEqual(response.status_code, 202)

        # Check if the objects contain the newly posted object (length + 1)
        new_length = len(BiasAnalysis.objects.all())
        self.assertEqual(new_length, length + 1)

        # Check if the request returned an analysis id
        response_data = json.loads(response.content)
        self.assertIn('analysis_id', response_data)

    def test_detect_political_bias_api_post_invalid_url(self):
        # Get the count of objects before new addition
        length = len(BiasAnalysis.objects.all())

        # Post the data to the url
        response = self.client.post(
            reverse('analyse-political-bias'), data={'url': '123'})

        # 400 = HTTP bad request error
        self.assertEqual(response.status_code, 400)

        # Ensure no new BiasAnalysis object was added
        new_length = len(BiasAnalysis.objects.all())
        self.assertEqual(new_length, length)

        # Assert that the object wasn't created
        self.assertFalse(BiasAnalysis.objects.exists())
