from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils import timezone

import datetime

# Create your views here.
from .forms import BlogPostForm, BlogPostCommentForm
from .models import BlogPost, BlogPostComment

def blog_post_list_view(request):
	class Post(object):
		def __init__(self, title, slug):
			self.title = title
			self.slug = slug

	with connection.cursor() as cursor:

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE date(pub_date)=curdate() ORDER BY pub_date DESC")
		rows = cursor.fetchall()
		today=[]
		for row in rows:
			today.append(Post(row[0],row[1]))

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE date(pub_date)=subdate(curdate(), interval 1 day) ORDER BY pub_date DESC")
		rows = cursor.fetchall()
		yesterday=[]
		for row in rows:
			yesterday.append(Post(row[0],row[1]))

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN SUBDATE(curdate(), INTERVAL DAYOFMONTH(curdate())-1 DAY) AND SUBDATE(curdate(), INTERVAL 1 DAY) ORDER BY pub_date DESC")
		rows = cursor.fetchall()
		month=[]
		for row in rows:
			month.append(Post(row[0],row[1]))

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN 0 AND SUBDATE(curdate(), INTERVAL DAYOFMONTH(curdate())-1 DAY) ORDER BY pub_date DESC")
		rows = cursor.fetchall()
		other=[]
		for row in rows:
			other.append(Post(row[0],row[1]))			

	template_name = 'blog/list.html'
	context = {'TodayList': today, 'YesterdayList': yesterday, 'MonthList': month, 'OtherList': other}
	return render(request, template_name, context)

def blog_post_create(request):
	form = BlogPostForm(request.POST or None)
	if form.is_valid():
		new_post=form.save(commit=False)
		new_post.pub_date = timezone.now()
		new_post.save()
		return redirect('blog_post_detail_view', slug=new_post.slug)

	template_name = 'blog/create.html'
	context = {'form': form}
	return render(request, template_name, context)

def blog_post_detail_view(request, slug):
	class Comment(object):
		def __init__(self, author, content,pub_date):
			self.author = author
			self.content = content
			self.pub_date = pub_date

	post = get_object_or_404(BlogPost, slug=slug)

	with connection.cursor() as cursor:
		cursor.execute("SELECT author, content, pub_date FROM blog_blogpostcomment WHERE blogpost_id=%(id)s ORDER BY pub_date DESC", { 'id': post.id })
		rows = cursor.fetchall()
		comments=[]
		for row in rows:
			comments.append(Comment(author=row[0], content=row[1], pub_date=row[2]))

	form = BlogPostCommentForm(request.POST or None)
	if form.is_valid():
		new_comment=form.save(commit=False)
		new_comment.pub_date = timezone.now()		
		new_comment.blogpost=post
		new_comment.save()
		return redirect('blog_post_detail_view', slug=post.slug)

	template_name = 'blog/detail.html'
	context = {'post': post,'comments':comments, 'form': form}
	return render(request, template_name, context)



def blog_post_update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'blog/update.html'
	context = {'object': obj, 'form': None}
	return render(request, template_name, context)

def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'blog/delete.html'
	context = {'object': obj}
	return render(request, template_name, context)