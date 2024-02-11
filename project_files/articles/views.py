from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Article
from .utils import *


@login_required
def article_details(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    return render(request, 'articles/article_details.html', {'article': article})
