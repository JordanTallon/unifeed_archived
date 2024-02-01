from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException


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
