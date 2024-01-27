# scraper/views.py

from django.shortcuts import render
from .forms import URLForm
from .models import ScrapedData
from bs4 import BeautifulSoup
import requests

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text() if soup.find('h1') else ''
    content = ' '.join([p.get_text() for p in soup.find_all('p')])
    return title, content

def scrape(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            title, content = scrape_data(url)
            scraped_data = ScrapedData.objects.create(url=url, title=title, content=content)
            return render(request, 'scraper/scrape_result.html', {'scraped_data': scraped_data})
    else:
        form = URLForm()

    return render(request, 'scraper/scrape_form.html', {'form': form})
