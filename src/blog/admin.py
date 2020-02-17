from django.contrib import admin

# Register your models here.
from .models import BlogPost, BlogPostComment

admin.site.register(BlogPost)
admin.site.register(BlogPostComment)
