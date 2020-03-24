from django.db import models
from django.contrib.auth.models import User



# Create your models here.
# python manage.py makemigrations
# python manage.py migrate


class BlogPost(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.TextField()
	slug = models.SlugField(unique=True)
	content = models.TextField(null=True, blank=True)
	pub_date = models.DateTimeField()

class BlogPostComment(models.Model):
	id = models.AutoField(primary_key=True)
	author= models.TextField(max_length=30)
	content = models.TextField()
	pub_date = models.DateTimeField()
	blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


