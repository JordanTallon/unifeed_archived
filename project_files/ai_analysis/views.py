from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import PoliticalBiasAnalysis
from .serializer import PoliticalBiasAnalysisSerializer


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
    print("Before serializer", request.data)
    serializer = PoliticalBiasAnalysisSerializer(data=request.data)
    # Check if the serialization was succesful:
    if serializer.is_valid():
        # Valid, so save the object
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    print(serializer.errors)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
