# scraper/views.py

from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
import json


def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = ' '.join([p.get_text() for p in soup.find_all('p')])
    return content


def scrape(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            if url:
                content = scrape_data(url)
                return JsonResponse({'url': url, 'content': content})
        except:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    else:
        # No get route for scrape, instead display an error (might require get route later?)
        return JsonResponse({'error': 'Method not allowed'}, status=405)
