from scraper.utils import scrape_data
from .utils import analyse_sentences_for_bias, extract_ideal_sentences, text_to_md5_hash
from celery import shared_task
from .models import BiasAnalysis, ArticleAnalysisResults


# Shared task is basically telling the function to be picked up by a celery worker
# This lets me hook onto the synchronous scraper function I implemented in scraper.utils
# with an asynchronous version that calls it but does not interfere with its functionality or unit tests
@shared_task
def scrape(url, analysis_id):
    try:
        article_text = scrape_data(url)

    except (ValueError):
        print("An error occured when scraping from:", url)
        analysis_failed(analysis_id)
        return

    sentences = extract_ideal_sentences(article_text)
    analyse_sentences.delay(analysis_id, sentences, article_text)


# retry 3 times in 20 second intervals
@shared_task(bind=True, max_retries=3, default_retry_delay=20)
def analyse_sentences(self, analysis_id, sentences, article_text):
    try:
        results = analyse_sentences_for_bias(sentences)

        print("analysis results", results)

        # Check if the HuggingFace inference api is sleeping (it does if it wasn't called for a few minutes)
        if any('error' in result and 'currently loading' in result['error'] for result in results.values()):
            raise ValueError("Model is currently loading")

        bias_results = {
            # will be based on the biased sentence, e.g 9/10 sentences are left bias: conclusion=left
            'conclusion': 'None',
            'sentence_results': results,
        }

        analysis_complete(analysis_id, bias_results, article_text)
    except ValueError as exc:
        if self.request.retries < self.max_retries:
            # Retry the analysis
            self.retry(exc=exc)
        else:
            # Already tried 3 times, mark as failed
            analysis_failed(analysis_id)


def analysis_failed(analysis_id):
    analysis = BiasAnalysis.objects.get(id=analysis_id)
    analysis.status = 'failed'
    analysis.save()


def analysis_complete(analysis_id, bias_results, article_text):

    analysis = BiasAnalysis.objects.get(id=analysis_id)
    analysis.status = 'completed'

    sentence_results = bias_results['sentence_results']

    analysis_results = ArticleAnalysisResults.objects.create()
    analysis_results.url = analysis.id
    analysis_results.article_text_md5 = text_to_md5_hash(article_text)
    analysis_results.sentence_results = sentence_results

    analysis_results.save()

    analysis.results = analysis_results
    analysis.save()
