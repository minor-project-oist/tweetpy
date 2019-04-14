from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import DetailView
from django.views.generic import View
from django.contrib.auth import get_user_model
from .models import UserProfile

User  = get_user_model()

class UserTweetsDisplay(DetailView):
    model = User
    queryset = User.objects.all()
    template_name = 'accounts/user_detail.html'

    def get_object(self):
        return get_object_or_404(
                User,
                username__iexact = self.kwargs.get("username")
        )
    
    def get_context_data(self,*args,**kwargs):
        context = super(UserTweetsDisplay,self).get_context_data(*args,**kwargs)

        context["is_following"] = UserProfile.objects.is_following(self.request.user,self.get_object())
        return context

     

class UserFollowView(View):

    def get(self,request,username,*args,**kwargs):
        print(request.get_full_path())
        print("************************************************")
        toggle_user = get_object_or_404(User,username__iexact=username)
        
        if request.user.is_authenticated():
            following = UserProfile.objects.toggle_follow(request.user,toggle_user)
            
            # print("999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999")
        
        return redirect("/",username=username)




