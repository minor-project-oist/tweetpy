
from django.conf.urls import url

from .views import UserTweetsDisplay,UserFollowView

urlpatterns = [

   
    url(r'^(?P<username>[\w.@+-]+)/$',UserTweetsDisplay.as_view(),name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$',UserFollowView.as_view(),name='follow'),


    ]

