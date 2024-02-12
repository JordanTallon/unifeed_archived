from scraper.utils import scrape_data
from .utils import analyse_sentences_for_bias, extract_ideal_sentences
from celery import shared_task
from .models import BiasAnalysis


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
    analyse_sentences.delay(sentences, analysis_id)


# retry 3 times in 20 second intervals
@shared_task(bind=True, max_retries=3, default_retry_delay=20)
def analyse_sentences(self, sentences, analysis_id):
    try:
        results = analyse_sentences_for_bias(sentences)

        print("analysis results", results)

        # Check if the HuggingFace inference api is sleeping (it does if it wasn't called for a few minutes)
        if any('error' in result and 'currently loading' in result['error'] for result in results.values()):
            raise ValueError("Model is currently loading")

        analysis = BiasAnalysis.objects.get(id=analysis_id)
        analysis.status = 'completed'
        analysis.save()
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
