from django.shortcuts import render
from articles.models import blog
# Create your views here.
def articles(request):
    blogs = blog.objects.all()
    context = {
        'blogs': blogs,
    }
    return render(request, 'articles/articles.html', context)

def article_details(request,blog_title):
    try:
        single_blog = blog.objects.all().filter(blog_title = blog_title)
    except Exception as e:
        raise e
    context = {
        'single_blog': single_blog,
    }
    return render(request,'articles/article_details.html',context)