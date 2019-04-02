from django.db import models
from tweets.models import Tweet
# Create your models here.

class HashTag(models.Model):
    tag = models.CharField(max_length=120)


    def get_tweets(self):
        return Tweet.objects.filter(content__icontains=self.tag)