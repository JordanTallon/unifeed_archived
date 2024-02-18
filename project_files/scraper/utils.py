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
    website = parsed_url.scheme + parsed_url.netloc
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


def scrape_data(url):

    # Try make a request to the url
    try:
        response = requests.get(url)

        # If the url did not reply 200 (ok) then raise an error
        if response.status_code != 200:
            raise ValueError("Failed to retrieve data from the given URL")

    except (ConnectionError, Timeout, RequestException):
        # If the url could not be reached, raise an error
        raise ValueError("Failed to establish a connection to the URL")

    soup = BeautifulSoup(response.text, 'html.parser')
    content = ' '.join([p.get_text() for p in soup.find_all('p')])
    return content
