from scraper.utils import scrape_data
from .utils import analyse_sentences_for_bias
from celery import shared_task


# Shared task is basically telling the function to be picked up by a celery worker
# This lets me hook onto the synchronous scraper function I implemented in scraper.utils
# with an asynchronous version that calls it but does not interfere with its functionality or unit tests
@shared_task
def scrape(url):
    scrape_data(url)


@shared_task
def analyse(url):
    analyse_sentences_for_bias(url)
