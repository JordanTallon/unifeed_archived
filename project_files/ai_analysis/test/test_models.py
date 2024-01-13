from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from ..models import PoliticalBiasAnalysis


class PoliticalBiasAnalysisModelTest(TestCase):
    def political_bias_analysis_model_exists(self):
        biases = PoliticalBiasAnalysis.objects.count()
        self.assertEqual(biases, 0)

    def test_add_new_political_bias_analysis(self):
        bias = PoliticalBiasAnalysis(
            article_url="http://example.com",
            article_text_md5="0e7807a9fc2fc9c1acff9e5560e1de24",
            political_bias=50
        )

        bias.save()

        added_bias = PoliticalBiasAnalysis.objects.first()

        self.assertIsNotNone(added_bias)

    def test_generate_article_text_md5(self):
        bias = PoliticalBiasAnalysis(
            article_url="http://example.com",
            political_bias=50
        )
        # Generate an md5 hash for the model from the string "Hello World"
        bias.article_text_to_md5_hash("Hello World")

        # Check if the hash is equal to the hash value for "Hello World" (deterministic)
        self.assertEqual(bias.article_text_md5,
                         'b10a8db164e0754105b7a99be72e3fe5')
