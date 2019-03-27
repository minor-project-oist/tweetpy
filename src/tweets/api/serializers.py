from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer
from django.utils.timesince import timesince
from django.urls import reverse

class TweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only = True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    # tweetdetail = serializers.SerializerMethodField()


    def get_date_display(self,obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")
    def get_timesince(self,obj):
        return timesince(obj.timestamp)
    
    # def get_tweetdetail(self,obj):
    #     return reverse("tweet-api:list",kwargs={"id":obj.id})



    



    class Meta:
        model = Tweet
        fields = [
            'user',
            'content',
            'date_display',
            'timestamp',
            'timesince',
           
         
        ]
    
    