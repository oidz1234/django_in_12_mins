from django.shortcuts import render, get_object_or_404

from .models import Post

# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', context)

def post(request, post_id):
    post_to_display = get_object_or_404(Post, id=post_id)
    context = {
        'post': post_to_display,
    }
    return render(request, 'blog/post.html', context)

def my_view(request):
    # run intersting logic and code here
    # return some values to the user in the response
    # values = intersting
    return(request, values)
