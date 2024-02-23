
from django.shortcuts import render


def help_page(request):
    return render(request, 'unifeed/help.html')


def ai_transparency(request):
    return render(request, 'unifeed/ai_transparency.html')
