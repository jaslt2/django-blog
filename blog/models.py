from django import forms
from django.db import models
from django.utils import timezone

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(live=True)

    def myDrafts(self, request):
        return self.filter(live=False, author=request.user)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    live = models.BooleanField()
    main_image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    category = models.ForeignKey('blog.Category');

    objects = PostQuerySet.as_manager()

    def save_draft(self, request):
        self.author=request.user
        self.live=False
        self.save()

    def publish(self, request):
        self.author=request.user
        self.live=True
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    post = models.ForeignKey(Post, default=None)

class Category(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=200, default=0)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'main_image')

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ('image' ,)