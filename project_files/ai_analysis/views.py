from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import PoliticalBiasAnalysis
from .serializer import PoliticalBiasAnalysisSerializer
import requests


@api_view(['GET'])
def getPoliticalBiasAnalysis(request):
    # Get all PoliticalBiasAnalysis objects
    biases = PoliticalBiasAnalysis.objects.all()
    # Apply the serializer to the entire array
    serializer = PoliticalBiasAnalysisSerializer(biases, many=True)
    # Return serialized data
    return Response(serializer.data)


@api_view(['POST'])
def postPoliticalBiasAnalysis(request):

    data = request.data

    url = data.get('url')

    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    bias = PoliticalBiasAnalysis().create(url)
    bias.save()

    return Response({"message": "Political bias analysis created successfully."}, status=status.HTTP_201_CREATED)


"""     # Serialize the request data
    serializer = PoliticalBiasAnalysisSerializer(data=request.data)

    # Check if the serialization was succesful:
    if serializer.is_valid():
        # Valid, so save the object
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Invalid, return HTTP 400 bad request
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) """


"""     article = "This is a sentence. This is another. Yet another sentence. The second last sentence. Finally, the last sentence."
    result = analyzePoliticalBias(article)

    print(result)
     """
