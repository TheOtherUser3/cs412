# This file explains how to convert our Django data models
# for transmission over http

from rest_framework import serializers
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    """Specifies which fields are exposed to the API"""

    class Meta:
        model = Article
        fields = ['id','title','text','author', 'published', 'image_file']

    # We can add extra code to execute on create/read/update/delete operations

    def create(self, validated_data):

        # create article object, attach user foreign key
        article = Article.objects.create(user = User.objects.first(),
                                         **validated_data)
        #  save to database
        article.save()
        # return article
        return article

