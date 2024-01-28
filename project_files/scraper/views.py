# scraper/views.py

from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def scrape(request):
    data = json.loads(request.body)
    url = data.get('url')
    if url:
        content = scrape_data(url)
        return Response({'url': url, 'content': content})


def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = ' '.join([p.get_text() for p in soup.find_all('p')])
    return content
