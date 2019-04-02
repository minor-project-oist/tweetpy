from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from blog.models import Post

from django.views.generic import View,DetailView

from taggit.models import Tag



def home(request):
    context = {
        "posts" : Post.objects.all()
    }
    return render(request,'blog/post_list.html',context)



class BlogDetailView(DetailView):
    queryset = Post.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        return Post.objects.get(id=pk)



# def about(request):
#     return render(request,'blog/about.html')


class TagSearchView(View):

    def get(self,request,tag,*args,**kwargs):
       
        tags = get_object_or_404(Tag,slug = tag)

        obj = Post.objects.filter(tags__in=[tags])
        

        return render(request,'blog/post_list.html',{"posts":obj})

