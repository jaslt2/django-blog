from django.contrib import admin
from .models import Post, Category, ImageModel

class PostAdmin(admin.ModelAdmin):
    exclude = ['created_date']

admin.site.register(Post, PostAdmin)
admin.site.register(Category);
admin.site.register(ImageModel)
