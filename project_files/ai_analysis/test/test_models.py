from django.test import TestCase
from ..models import BiasAnalysis, ArticleAnalysisResults


class AIAnalysisModelTests(TestCase):
    def bias_analysis_model_exists(self):
        biases = BiasAnalysis.objects.count()
        self.assertEqual(biases, 0)

    def article_analysis_results_model_exists(self):
        results = ArticleAnalysisResults.objects.count()
        self.assertEqual(results, 0)

    def test_add_new_bias_analysis(self):
        analysis = BiasAnalysis(
            url="http://example.com",
            status="processing"
        )

        analysis.save()

        added_analysis = BiasAnalysis.objects.first()

        self.assertIsNotNone(added_analysis)

    def test_add_new_article_analysis_results(self):
        results = ArticleAnalysisResults(
            url="http://example.com",
            article_text_md5="0e7807a9fc2fc9c1acff9e5560e1de24",
            sentence_results={
                "sentence": {'left': 0.1, 'center': 0.8, 'right': 0.1}
            }
        )

        results.save()

        added_results = ArticleAnalysisResults.objects.first()

        self.assertIsNotNone(added_results)
