from scraper.utils import scrape_data
from .utils import analyse_sentences_for_bias, extract_ideal_sentences, text_to_md5_hash
from celery import shared_task
from .models import ArticleAnalysisResults
from traceback import format_exc
from collections import Counter


# Shared task is basically telling the function to be picked up by a celery worker
# This lets me hook onto the synchronous scraper function I implemented in scraper.utils
# with an asynchronous version that calls it but does not interfere with its functionality or unit tests
@shared_task
def scrape(url, analysis_id):
    try:
        # Scrape the article content
        article_text = scrape_data(url)
    except Exception as e:
        # Log an error message and mark the analysis as failed
        print(
            f"An error occurred when scraping from {url}: {e}\n{format_exc()}")
        analysis_failed(analysis_id)

    try:
        # Extract sentences for analysis
        sentences_df = extract_ideal_sentences(article_text)

        # Calculate the MD5 hash of the article text
        article_text_md5 = text_to_md5_hash(article_text)

        # Convert the sentence dataframe to json so Celery can serialize it
        sentences_df = sentences_df.to_json(orient='split')

        # Pass the MD5 hash along with other data to the analysis task
        analyse_sentences.delay(analysis_id, sentences_df, article_text_md5)
    except Exception as e:
        # Log an error message and mark the analysis as failed
        print(
            f"An error occurred when extracting ideal sentences: {e}\n{format_exc()}")
        analysis_failed(analysis_id)


# retry 3 times in 25 second intervals
@shared_task(bind=True, max_retries=3, default_retry_delay=25)
def analyse_sentences(self, analysis_id, sentences_df, article_text_md5):
    try:
        # Perform analysis on the sentences
        bias_results = analyse_sentences_for_bias(sentences_df)

        # Store the analysis results
        analysis_complete(analysis_id, bias_results,
                          article_text_md5)

    except ValueError as exc:
        # If an error occurs, retry the task up to 3 times
        if self.request.retries < self.max_retries:
            self.retry(exc=exc)
        else:
            # no more retries, mark the analysis as failed
            analysis_failed(analysis_id)


def make_final_conclusion(bias_results):
    """     
    Takes in bias results and makes a 'final' conclusion based on the sentence conclusions.
    For example if most sentences are left then the final conclusion is left 
    """
    # Extract all conclusions from the results
    conclusions = [result['conclusion'] for result in bias_results.values()]

    conclusion_counts = Counter(conclusions)

    most_common_conclusion = conclusion_counts.most_common(1)[0][0]

    # Calculate the percentage occurrence of the conclusion that was most common
    most_common_percentage = (
        conclusion_counts[most_common_conclusion] / len(conclusions)) * 100

    return most_common_conclusion, most_common_percentage


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
    analysis.bias_conclusion, analysis.bias_percent = make_final_conclusion(
        bias_results)
    analysis.status = 'completed'
    analysis.save()
