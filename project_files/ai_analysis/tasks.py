from scraper.utils import scrape_data
from .utils import analyse_sentences_for_bias, extract_ideal_sentences
from celery import shared_task
from .models import BiasAnalysis


# Shared task is basically telling the function to be picked up by a celery worker
# This lets me hook onto the synchronous scraper function I implemented in scraper.utils
# with an asynchronous version that calls it but does not interfere with its functionality or unit tests
@shared_task
def scrape(url, analysis_id):
    print("starting scrape")
    article_text = scrape_data(url)
    sentences = extract_ideal_sentences(article_text)
    print("scrape results", sentences)
    analyse_sentences.delay(sentences, analysis_id)


@shared_task
def analyse_sentences(sentences, analysis_id):
    print("starting analysis")
    results = analyse_sentences_for_bias(sentences)

    print("analysis results", results)

    analysis = BiasAnalysis.objects.get(id=analysis_id)
    analysis.status = 'completed'
    analysis.save()
