from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
import random
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.
    
class ShowAllView(ListView):
    """Define a view class to show all blog Articles"""
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to add debugging"""
        if request.user.is_authenticated:
            print(f"ShowAllView.dispatch(): request.user={request.user}")
        return super().dispatch(request, *args, **kwargs)

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

class CreateArticleView(LoginRequiredMixin, CreateView):
    """Define a view class to create a new blog Article
    (1) display the HTML form to the USER GET
    (2) process the form submission POST and store new article object
    """
    
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self):
        """Return the login URL to redirect to for login"""
        return reverse('login')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #print out form data
        print("Create Article form Data:", form.cleaned_data)
        #associate the article with the logged-in user
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

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
    
class UpdateArticleView(UpdateView):
    """Define a view class to update an existing blog Article
    (1) display the HTML form to the USER GET
    (2) process the form submission POST and store updated article object
    """
    model = Article
    form_class = UpdateArticleForm
    template_name = 'blog/update_article_form.html'

class DeleteCommentView(DeleteView):
    """Define a view class to delete an existing blog Comment"""

    model = Comment
    template_name = 'blog/delete_comment_form.html'

    def get_success_url(self):
        """Return the URL to direct to after a successful delete"""
        # find PK for this Comment
        pk = self.kwargs['pk']
        #find comment
        comment = Comment.objects.get(pk=pk)
        article = comment.article
        return reverse('article', kwargs={'pk':article.pk})
    
class UserRegistrationView(CreateView):
    """Define a view class to register a new user account"""

    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        """Return the URL to direct to after successful registration"""
        return reverse('login')