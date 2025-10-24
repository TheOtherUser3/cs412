from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    '''Encapsulate the data of a blog Article by an author'''


    # Define the data attribute of an Article
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        """Return the url to access a particular article instance."""
        return reverse('article', kwargs={'pk':self.pk})
    
    def get_all_comments(self):
        """Return all comments associated with this article instance."""
        return Comment.objects.filter(article=self)
    
class Comment(models.Model):
    '''Encapsulate the data of a blog Comment on an Article'''

    # Define the data attribute of a Comment
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"Comment by {self.author} on {self.article.title}"