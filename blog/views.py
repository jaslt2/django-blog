import logging

from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render,get_object_or_404,redirect

from .models import Post, PostForm, ImageModel, ImageForm

logger = logging.getLogger(__name__)

def index(request):
	context = {
        'posts': Post.objects.published(),
        'drafts': Post.objects.myDrafts(request)
    }
	return render(request, 'blog/index.html', context)

def post_detail(request, pk):   
    context = {
        'post': get_object_or_404(Post, pk=pk)
    }
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    ImageFormSet = modelformset_factory(ImageModel, form=ImageForm, extra=1)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.save_draft(request)
            for image_form in formset.cleaned_data:
                if image_form:
                    image = image_form['image']
                    photo = ImageModel(post=post, image=image)
                    photo.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        formset = ImageFormSet(queryset=ImageModel.objects.none())
    return render(request, 'blog/post_edit.html', {'form': form, 'formset': formset})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ImageFormSet = inlineformset_factory(Post, ImageModel, form=ImageForm, max_num=3)
    logging.warn(post.imagemodel_set.all())
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        formset = ImageFormSet(request.POST, request.FILES, instance=post)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.save_draft(request)
            formset.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        formset = ImageFormSet(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'formset': formset})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish(request)
    return redirect('index', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('index')