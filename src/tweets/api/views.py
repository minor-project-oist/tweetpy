from .serializers import TweetModelSerializer

from rest_framework import generics

from tweets.models import Tweet

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .paginations import StandardResultsPagination
from rest_framework.response import Response


class LikeToggleAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    

    def get(self,request,pk,format=None):
        tweet_qs = Tweet.objects.filter(pk = pk)
        if request.user.is_authenticated():
            is_liked = Tweet.objects.tweet_toggle(request.user,tweet_qs.first())
            count_likes = Tweet.objects.get_likes(request.user,tweet_qs.first())
            return Response({'liked':is_liked,"count_likes":count_likes})
        return Response({'message':"invalid operation"})




class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class  = TweetModelSerializer
    permission_classes = (IsAuthenticated,)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    


class TweetListAPIView(generics.ListAPIView):

    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self,*args,**kwargs):
        context = super(TweetListAPIView,self).get_serializer_context(*args,**kwargs)
        context['request'] = self.request 
        return context

    def get_queryset(self,*args,**kwargs):
        qs = Tweet.objects.all()
        im_following = self.request.user.profile.get_following()

        qs1 = qs.filter(user__in=im_following)
        qs2 = Tweet.objects.filter(user=self.request.user)
        qs = (qs1|qs2).distinct().order_by("-timestamp")
        query = self.request.GET.get("q",None)
        
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )

        return qs
    