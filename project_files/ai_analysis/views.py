from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import ArticleAnalysisResults
from .tasks import async_scrape
from .serializer import ArticleAnalysisResultsSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render


@api_view(['GET'])
def check_analysis_status(request, analysis_id):
    bias_analysis = ArticleAnalysisResults.objects.get(id=analysis_id)
    bias_analysis_serialized = ArticleAnalysisResultsSerializer(
        bias_analysis).data

    if bias_analysis.status == 'processing':
        # Return a 'waiting' template to indicate that the results aren't ready
        return render(request, 'ai_analysis/waiting_results.html', {'analysis_id': bias_analysis.id})
    else:
        # Return a template with the final analysis results (success or fail, to be indicated in html)
        return render(request, 'ai_analysis/final_analysis_results.html', {'bias_analysis': bias_analysis_serialized})


@api_view(['POST'])
def analyse_article_bias(request):
    data = request.data
    url = data.get('url')

    # Check if a 'url' param was even given in the request data
    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Verify that the 'url' param contained a genuine URL
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return Response({"error": "Invalid URL."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new analysis entry in the database
    bias_analysis = ArticleAnalysisResults.objects.create(url=url)

    # Start the asynchronous scraping process
    async_scrape.delay(url, bias_analysis.id)

    # Instantly return the BiasAnalysis so that the client may track the status of the asynchronous tasks
    if request.content_type == 'application/json':
        return Response({'analysis_id': bias_analysis.id}, status=202)
    else:
        # if htmx posted the route, return html
        return render(request, 'ai_analysis/waiting_results.html', {'analysis_id': bias_analysis.id}, status=202)
