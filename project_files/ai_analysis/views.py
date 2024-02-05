from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import PoliticalBiasAnalysis
from .serializer import PoliticalBiasAnalysisSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


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

    bias = PoliticalBiasAnalysis().create(url)

    # If the returned bias object is non, return a bad request.
    if not bias:
        return Response({"error": "Unable to create bias analysis for the given URL"}, status=status.HTTP_400_BAD_REQUEST)

    bias.save()

    # Serialize the bias object to return in the POST result
    serialized_bias = PoliticalBiasAnalysisSerializer(bias).data

    return Response({"message": "Political bias analysis created successfully.", "analysis_results": serialized_bias}, status=status.HTTP_201_CREATED)
