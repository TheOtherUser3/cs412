from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
import random
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
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

class CreateArticleView(CreateView):
    """Define a view class to create a new blog Article
    (1) display the HTML form to the USER GET
    (2) process the form submission POST and store new article object
    """
    
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

class CreateCommentView(CreateView):
    """Define a view class to create a new blog Comment
    (1) display the HTML form to the USER GET
    (2) process the form submission POST and store new comment object
    """
    
    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def get_success_url(self):
        """After creating a comment, return to the article page"""

        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk':pk})
    
    def get_context_data(self):
        # retrieve the article pk from the URL pattern
        pk = self.kwargs['pk']
        # attach this article to the comment
        article = Article.objects.get(pk=pk)
        # get the default context data from superclass
        context =  super().get_context_data()
        #add article into context dictionary
        context['article'] = article

        return context
    
    def form_valid(self, form):
        """Before saving the new comment, associate it with the correct article"""
        print(form.cleaned_data)
        # retrieve the article pk from the URL pattern
        pk = self.kwargs['pk']
        # attach this article to the comment
        article = Article.objects.get(pk=pk)
        form.instance.article = article #Set the Foreign key

        # delegate the work to the superclass form_valid
        return super().form_valid(form)