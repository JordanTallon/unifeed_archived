# scraper/views.py

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
