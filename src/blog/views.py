from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from blog.models import Post

from django.views.generic import View,DetailView

from taggit.models import Tag
from taggit.managers import TaggableManager




def home(request):
    context = {
        "posts" : Post.objects.all(),
        "tags" : Tag.objects.all().distinct(),
    }
    return render(request,'blog/post_list.html',context)



class BlogDetailView(DetailView):
    queryset = Post.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        return Post.objects.get(id=pk)




class TagSearchView(View):

    def get(self,request,tag,*args,**kwargs):
       
        tags = get_object_or_404(Tag,slug = tag)

        obj = Post.objects.filter(tags__in=[tags])
        

        return render(request,'blog/post_list.html',{"posts":obj})

class BlogCreateView(View):

    def get(self,request):
        return render(request,'blog/writearticle.html')
    
    def post(self,request):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(request.POST['editor1'])

        title = request.POST['title']
        content = request.POST['editor1']
        tags = request.POST['tag']

        post = Post.objects.create(author=request.user , title=title,content=content)
        for t in tags.split(","):

            tag = Tag.objects.create(name=t)
            post.tags.add(tag)
        post.save()
     

        return redirect('/blog')
    
        
        



