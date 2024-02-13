from django.test import TestCase
from ..models import ArticleAnalysisResults


class AIAnalysisModelTests(TestCase):

    def article_analysis_results_model_exists(self):
        results = ArticleAnalysisResults.objects.count()
        self.assertEqual(results, 0)

    def test_add_new_article_analysis_results(self):
        analysis = ArticleAnalysisResults(
            url="http://example.com",
        )

        analysis.save()

        added_analysis = ArticleAnalysisResults.objects.first()

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
