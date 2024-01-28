from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import PoliticalBiasAnalysis
from .serializer import PoliticalBiasAnalysisSerializer
import requests


@api_view(['GET'])
def getData(request):
    # Get all PoliticalBiasAnalysis objects
    biases = PoliticalBiasAnalysis.objects.all()
    # Apply the serializer to the entire array
    serializer = PoliticalBiasAnalysisSerializer(biases, many=True)
    # Return serialized data
    return Response(serializer.data)


@api_view(['POST'])
def postPoliticalBiasAnalysis(request):
    # Serialize the request data
    serializer = PoliticalBiasAnalysisSerializer(data=request.data)

    # Check if the serialization was succesful:
    if serializer.is_valid():
        # Valid, so save the object
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Invalid, return HTTP 400 bad request
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


"""     article = "This is a sentence. This is another. Yet another sentence. The second last sentence. Finally, the last sentence."
    result = analyzePoliticalBias(article)

    print(result)
     """


def analyzePoliticalBias(article):

    # TODO: I will find 'ideal' sentences from an article
    sentences = article.split('.')

    # Restrict to 5 sentences per article (5 is arbitrary for testing, i'm not sure what a good limit is yet)
    if (len(sentences) >= 5):
        sentences = sentences[:5]

    def query(payload):
        response = requests.post(settings.HUGGINGFACE_API_URL,
                                 headers=settings.HUGGINGFACE_API_HEADERS, json=payload)
        return response.json()

    # Query for all sentences and gather the results in a 'results' array
    results = []
    for sentence in sentences:
        output = query({"inputs": sentence})
        results.append(output)

    # Associate each result with the sentence text. For displaying to the user later on.
    result_dict = {}
    for i in range(5):
        result_dict[sentences[i]] = results[i]

    return result_dict
