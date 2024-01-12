from django.shortcuts import render
from rest_framework.response import Response
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
