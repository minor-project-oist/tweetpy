from .serializers import TweetModelSerializer

from rest_framework import generics

from tweets.models import Tweet

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .paginations import StandardResultsPagination



class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class  = TweetModelSerializer
    permission_classes = (IsAuthenticated,)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    


class TweetListAPIView(generics.ListAPIView):

    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self,*args,**kwargs):
        qs = Tweet.objects.all()
        query = self.request.GET.get("q",None)
        
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )

        return qs
    