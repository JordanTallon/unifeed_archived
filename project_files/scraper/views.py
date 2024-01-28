# scraper/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import URLForm
from .models import ScrapedData
from bs4 import BeautifulSoup
import requests


def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = ' '.join([p.get_text() for p in soup.find_all('p')])
    return content


def scrape(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            content = scrape_data(url)
            scraped_data = ScrapedData.objects.create(url=url, content=content)
            return render(request, 'scraper/scrape_result.html', {'scraped_data': scraped_data})
    else:
        # No get route for scrape, instead display an error (might require get route later?)
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    return render(request, 'scraper/scrape_form.html', {'form': form})
