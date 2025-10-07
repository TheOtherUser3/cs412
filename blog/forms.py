from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    """"Form for creating a new Article to the database"""
    class Meta:
        "Associate the form with the Article model and specify fields"
        model = Article
        fields = ['author', 'title', "text", 'image_file']


class CreateCommentForm(forms.ModelForm):
    """"Form for creating a new Comment to the database"""
    class Meta:
        "Associate the form with the Comment model and specify fields"
        model = Comment
        fields = ['author', 'text']

class UpdateArticleForm(forms.ModelForm):
    """"Form for updating an existing Article in the database"""
    class Meta:
        "Associate the form with the Article model and specify fields"
        model = Article
        fields = ['title', "text"]