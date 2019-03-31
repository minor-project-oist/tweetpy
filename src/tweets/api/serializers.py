from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer
from django.utils.timesince import timesince
from django.urls import reverse

class TweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only = True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    # tweetdetail = serializers.SerializerMethodField()

    def get_likes(self,obj):
        return obj.likes.all().count()

    def get_did_like(self,obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                return True
        return False
    
    def get_date_display(self,obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")
    def get_timesince(self,obj):
        return timesince(obj.timestamp)
  

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'date_display',
            'timestamp',
            'timesince',
            'did_like',
            'likes'
            
           
         
        ]
    
    