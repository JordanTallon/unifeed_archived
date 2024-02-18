from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


def parse_url(url):
    """     
    This function breaks up any given URL - primarily used to set up communication with a robots.txt file.
    For example: "https://example.com/test_path" - we can get 'example.com' and 'test_path' from this.
    For querying the site for any robots.txt and permission to scrape, we can add '/robots.txt' to get 'example.com/robots.txt'
    And we can query the robots.txt with '/test_path' to see if we are allowed to scrape that path.
    """
    parsed_url = urlparse(url)

    # Keep the scheme as part of the website if one was extracted
    if parsed_url.scheme:
        website = parsed_url.scheme + "://" + parsed_url.netloc
    else:
        website = parsed_url.netloc

    path = parsed_url.path
    return website, path


def check_robots(website, path):
    """ 
    Takes in a website 'https://example.com' and a path '/news_article', locates the website's 'robot.txt' file,
    reads the robots file and checks if 'UnifeedAgent' is explicitly denied permission to scrape the given path.
    Some websites  deny all agents under a wildcard * . If scraping is not allowed, we will follow ethical scraping 
    guidelines and cancel the scraping with a false return from this function.
    """
    rp = RobotFileParser()
    rp.set_url(website + "/robots.txt")
    target = website + path
    rp.read()
    user_agent = 'UnifeedAgent'

    # If the robots.txt of the website denies permission to scrape, this returns false.
    return (rp.can_fetch(user_agent, target))


def extract_article_text(scraped_article):
    """  
    Takes in the html content of a scraped website and tries different different strategies to target and extract the main
    articl content of the page. 
    Starts with high level of specificity (very likely to be article text) 
    To lower level of specificity (might not necessarily be article text)
    "On average, articles tend to have at least three to five paragraphs, but longer articles might have more"
    Not a very rigid source, but a starting point for what ultimately will need to be a manual observation and adjustment over time
    https://www.quora.com/How-many-paragraphs-should-an-article-have
    So the goal of this function is to find at least 3 paragraphs
    """
    soup = BeautifulSoup(scraped_article, 'html.parser')

    if not soup:
        raise ValueError("Failed to parse HTML from the given url")

    # First try get all paragraphs inside an <article> tag
    article = soup.find('article')

    if article:
        extracted_paragraphs = article.find_all('p')
        if len(extracted_paragraphs) >= 3:
            return extracted_paragraphs

    # Check for common article classes (this will be manually updated as more are discovered)
    common_article_classes = ['article-body',
                              'post-content', 'content', 'news-article']
    for common_class in common_article_classes:
        class_div = soup.find('div', class_=common_class)
        if class_div:
            extracted_paragraphs = class_div.find_all('p')
            if len(extracted_paragraphs) >= 3:
                return extracted_paragraphs

    # Check for div elements containing a number of paragraphs indiciative of an article
    divs = soup.find_all('div')
    if len(divs) > 0:
        for div in divs:
            extracted_paragraphs = div.find_all('p')
            if len(extracted_paragraphs) >= 3:
                return extracted_paragraphs

    # As a last resort, return all paragraphs on the website
    return soup.find_all('p')


def scrape_data(url):

    website, path = parse_url(url)

    if not check_robots(website, path):
        raise ValueError(
            f"{website}/robots.txt denied UnifeedAgent permission to scrape.")

    # Try make a request to the url
    try:
        response = requests.get(url)

        # If the url did not reply 200 (ok) then raise an error
        if response.status_code != 200:
            raise ValueError("Failed to retrieve data from the given URL")
        if 'text/html' not in response.headers.get('Content-Type', ''):
            raise ValueError("URL did not return HTML data")
    except (ConnectionError, Timeout, RequestException):
        # If the url could not be reached, raise an error
        raise ValueError("Failed to establish a connection to the URL")

    extracted_paragraphs = extract_article_text(response.text)

    if len(extracted_paragraphs) < 3:
        raise ValueError("Failed to extract article content")

    content = ' '.join([p.get_text() for p in extracted_paragraphs])

    return content
