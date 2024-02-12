from scraper.utils import scrape_data
from .utils import analyse_sentences_for_bias, extract_ideal_sentences, text_to_md5_hash
from celery import shared_task
from .models import ArticleAnalysisResults


# Shared task is basically telling the function to be picked up by a celery worker
# This lets me hook onto the synchronous scraper function I implemented in scraper.utils
# with an asynchronous version that calls it but does not interfere with its functionality or unit tests
@shared_task
def scrape(url, analysis_id):
    try:
        # Scrape the article content
        article_text = scrape_data(url)

        # Extract sentences for analysis
        sentences = extract_ideal_sentences(article_text)

        # Calculate the MD5 hash of the article text
        article_text_md5 = text_to_md5_hash(article_text)

        # Pass the MD5 hash along with other data to the analysis task
        analyse_sentences.delay(analysis_id, sentences, article_text_md5)

    except (ValueError):
        # Log an error message and mark the analysis as failed
        print("An error occured when scraping from:", url)
        analysis_failed(analysis_id)


# retry 3 times in 20 second intervals
@shared_task(bind=True, max_retries=3, default_retry_delay=20)
def analyse_sentences(self, analysis_id, sentences, article_text_md5):
    try:
        # Perform analysis on the sentences
        results = analyse_sentences_for_bias(sentences)

        # Check if the HuggingFace inference api is sleeping (it does if it wasn't called for a few minutes)
        if any('error' in result and 'currently loading' in result['error'] for result in results.values()):
            # If the model is loading, raise an exception to retry the task
            raise ValueError("Model is currently loading")

        # Store the analysis results
        analysis_complete(analysis_id, results, article_text_md5)

    except ValueError as exc:
        # If an error occurs, retry the task up to 3 times
        if self.request.retries < self.max_retries:
            self.retry(exc=exc)
        else:
            # no more retries, mark the analysis as failed
            analysis_failed(analysis_id)


def analysis_failed(analysis_id):
    # Mark the analysis status as 'failed' in the database
    analysis = ArticleAnalysisResults.objects.get(id=analysis_id)
    analysis.status = 'failed'
    analysis.save()


def analysis_complete(analysis_id, bias_results, article_text_md5):
    # Update the analysis object in the database with the results
    analysis = ArticleAnalysisResults.objects.get(id=analysis_id)
    analysis.url = analysis.url
    analysis.article_text_md5 = article_text_md5
    analysis.sentence_results = bias_results
    analysis.status = 'completed'
    analysis.save()
