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
from feeds.models import UserFeed
from .utils import *
import random


@login_required
def article_details(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    # Get "related" articles to the current article being viewed
    # Just a random selection for now
    user_feeds = UserFeed.objects.filter(
        user=request.user).values_list('feed', flat=True)
    related_articles_queryset = Article.objects.filter(
        feeds__in=user_feeds
    ).exclude(
        image_url=""
    ).distinct()
    # Up to 10 articles
    related_articles = random.sample(
        list(related_articles_queryset), min(len(related_articles_queryset), 10))

    return render(request, 'articles/article_details.html', {'article': article, 'related_articles': related_articles, })