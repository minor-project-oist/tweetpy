from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from .validators import validate_content



class TweetManager(models.Manager):

    def tweet_toggle(self,user,tweet_obj):
        if user in tweet_obj.likes.all():
            isliked = False
            tweet_obj.likes.remove(user)

        else:
            isliked  = True
            tweet_obj.likes.add(user)
        
        return isliked
    
    def get_likes(self,user,obj):
        return obj.likes.all().count()
    
   
    def retweet(self,user,parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj
        
        obj = self.model(
            parent = og_parent,
            user = user,
            content = parent_obj.content,
        )
        obj.save()
        return obj


# Create your models here.
class Tweet(models.Model):
    parent = models.ForeignKey("self",blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content =  models.CharField(max_length=140,validators=[validate_content])
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liked',blank=True)
    updated = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = TweetManager()

    def get_absolute_url(self):
        return reverse("tweet:detail",kwargs={"pk":self.pk})
    
    
    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ["-timestamp"]


    