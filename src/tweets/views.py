from django.shortcuts import render

from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin,UserOwnerMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q





class TweetCreateView(LoginRequiredMixin,FormUserNeededMixin,CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    
    # success_url = '/tweet/'

    login_url = '/admin/'

  

class TweetUpdateView(UserOwnerMixin,UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    # success_url = '/tweet/'


class TweetDeleteView(LoginRequiredMixin,DeleteView):
    model = Tweet
    template_name = 'tweets/delete_view.html'
    login_url = '/admin/'
    success_url = reverse_lazy('tweet:list')


class TweetListView(ListView):
    # queryset = Tweet.objects.all()
   # template_name = 'tweets/list.html' for custom tempaltes
    
    def get_queryset(self,*args,**kwargs):
        qs = Tweet.objects.all()
        query = self.request.GET.get("q",None)
        print(query)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )

        return qs
    

    def get_context_data(self,*args,**kwargs):
        context = super(TweetListView,self).get_context_data(*args,**kwargs)
        
        context["createform"] = TweetModelForm()
        context["create_url"] = reverse_lazy("tweet:create")
        print(context)
        return context
    






 

class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        return Tweet.objects.get(id=pk)

