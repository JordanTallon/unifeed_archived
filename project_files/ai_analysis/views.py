from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import ArticleAnalysisResults, BiasAnalysis
from .tasks import scrape
from .serializer import BiasAnalysisSerializer, ArticleAnalysisResultsSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render


@api_view(['GET'])
def check_analysis_status(request, analysis_id):
    analysis = BiasAnalysis.objects.get(id=analysis_id)
    print("current progress", analysis.status)
    if analysis.status == 'waiting':
        # Return a 'waiting' template to indicate that the results aren't ready
        return render(request, 'ai_analysis/waiting_results.html', {'analysis_id': analysis_id})

    # Return a template with the final analysis results
    return render(request, 'ai_analysis/final_analysis_results.html', {'analysis': analysis})


@api_view(['POST'])
def analyse_article_bias(request):

    data = request.data

    # Check if a 'url' param was even given in the request data
    url = data.get('url')

    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Verify that the 'url' param contained a genuine URL
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return Response({"error": "Invalid URL."}, status=status.HTTP_400_BAD_REQUEST)

    bias_analysis = BiasAnalysis.objects.create(url=url, status='processing')

    # Start the asynchronous process
    scrape.delay(url, bias_analysis.id)

    # Instantly return the BiasAnalysis so that client may track the status of the asynchronous tasks
    if request.content_type == 'application/json':
        return Response({'analysis_id': bias_analysis.id}, status=202)
    else:
        # if htmx posted the route, return html
        return render(request, 'ai_analysis/waiting_results.html', {'analysis_id': bias_analysis.id})

    # TODO:
"""     # TODO: a bunch of error handling

    # Asynchronous (scraping the website)
    article_text = scrape.delay(url)
    # Synchronous (just local logic to find the best sentences in the scraped content)
    sentences = extract_ideal_sentences(article_text)
    # Asynchronous (passing the ideal sentences to the external HuggingFace hosted AI and waiting for results)
    results = analyse_sentences.delay(sentences)

    # TODO: serialize the results, create a model entry in the database

    return results
 """

"""         analyze.delay(url)
        
        # Try scrape article content from the given url
        try:
            article_text = scrape_data(article_url)
        except ValueError as e:
            # No political bias analysis can be created from a broken url But it is not a 'critical failure'
            # if this happens, so returning a None object is safe here
            # Conditional logic can be applied, like if the creation of this model returns none, display a failure message to the user.
            return None

        article_text_md5 = text_to_md5_hash(article_text)

        biased_sentences = analyze_political_bias(article_text)

        return cls(article_url=article_url, article_text_md5=article_text_md5, biased_sentences=biased_sentences) """


""" 

    bias = PoliticalBiasAnalysis().create(url)

    # If the returned bias object is non, return a bad request.
    if not bias:
        return Response({"error": "Unable to create bias analysis for the given URL"}, status=status.HTTP_400_BAD_REQUEST)

    bias.save()

    # Serialize the bias object to return in the POST result
    serialized_bias = PoliticalBiasAnalysisSerializer(bias).data

    return Response({"message": "Political bias analysis created successfully.", "analysis_results": serialized_bias}, status=status.HTTP_201_CREATED)
 """
