from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, SavedArticle
from .utils import *
from .forms import SaveArticleForm
import random


@login_required
def article_details(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    is_saved = SavedArticle.objects.filter(
        article=article, user=request.user)

    # This handles the user clicking on the "save article" button
    if request.method == "POST":
        form = SaveArticleForm(request.POST)
        if form.is_valid():
            # If the user already saved this article

            if is_saved:
                # 'Unsave' it (delete it)
                is_saved.delete()
            else:
                # Save it
                SavedArticle.objects.create(user=request.user, article=article)
                is_saved = True
    else:
        form = SaveArticleForm()

    # Get "related" articles to the current article being viewed
    # Just a random selection for now
    related_articles_queryset = Article.objects.filter(
        feed=article.feed).exclude(image_url="").distinct()
    # Up to 5 articles
    related_articles = random.sample(
        list(related_articles_queryset), min(len(related_articles_queryset), 5))

    return render(request, 'articles/article_details.html', {'article': article, 'related_articles': related_articles, 'form': form, 'is_saved': is_saved})


@login_required
def saved_articles(request, user_id):
    saved_articles = SavedArticle.objects.filter(user=user_id)
    articles = [saved_article.article for saved_article in saved_articles]

    return render(request, 'articles/saved_articles.html', {'articles': articles})
