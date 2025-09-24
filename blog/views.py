from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random
# Create your views here.

class ShowAllView(ListView):
    """Define a view class to show all blog Articles"""
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class ArticleView(DetailView):
    """Define a view class to show a single blog Article"""
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

class RandomArticleView(DetailView):
    """Define a view class to show a random blog Article"""
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        articles = Article.objects.all()
        return random.choice(articles)