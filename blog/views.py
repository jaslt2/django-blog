import logging
from PIL import Image

from .models import Post, PostForm
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone

logger = logging.getLogger(__name__)

def index(request):
	context = {
         # 'posts': Post.objects.all()[:5]
        'posts': Post.objects.published()[:5],
        'drafts': Post.objects.myDrafts(request)
    }
	return render(request, 'blog/index.html', context)

def post_detail(request, pk):   
    context = {
        'post': get_object_or_404(Post, pk=pk)
    }
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('index')