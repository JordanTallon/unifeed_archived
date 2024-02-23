from django.test import TestCase
from ai_analysis.utils import text_to_md5_hash


class AIAnalysisUtilsTests(TestCase):
    def test_generate_text_md5(self):

        # Generate an md5 hash for the model from the string "Hello World"
        md5_text = text_to_md5_hash("Hello World")

        # Check if the hash is equal to the hash value for "Hello World" (deterministic)
        self.assertEqual(md5_text, 'b10a8db164e0754105b7a99be72e3fe5')
