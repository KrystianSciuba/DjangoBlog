from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from slugify import slugify
from django.utils import timezone
from django.db import IntegrityError

import datetime

# Create your views here.
from .forms import BlogPostForm, BlogPostCommentForm
from .models import BlogPost, BlogPostComment

def blog_post_list_view(request):
	class Post(object):
		def __init__(self, title, slug):
			self.title = title
			self.slug = slug

	now=datetime.datetime.now()
	today=datetime.date.today()
	yesterday=datetime.date.today()-datetime.timedelta(1)
	first_of_month=datetime.date.today().replace(day=1)
	if yesterday < first_of_month:
		other_date=yesterday
	else:
		other_date=first_of_month

	with connection.cursor() as cursor:

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN %(date1)s AND %(date2)s ORDER BY pub_date DESC", {'date1': today, 'date2': now})
		rows = cursor.fetchall()
		todayPosts=[]
		for row in rows:
			todayPosts.append(Post(row[0],row[1]))

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN %(date1)s AND %(date2)s ORDER BY pub_date DESC", {'date1': yesterday, 'date2': today})
		rows = cursor.fetchall()
		yesterdayPosts=[]
		for row in rows:
			yesterdayPosts.append(Post(row[0],row[1]))

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN %(date1)s AND %(date2)s ORDER BY pub_date DESC",{'date1': first_of_month, 'date2': yesterday})
		rows = cursor.fetchall()
		monthPosts=[]
		for row in rows:
			monthPosts.append(Post(row[0],row[1]))

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN 0 AND %(date)s ORDER BY pub_date DESC",{'date': other_date})
		rows = cursor.fetchall()
		otherPosts=[]
		for row in rows:
			otherPosts.append(Post(row[0],row[1]))			

	template_name = 'blog/list.html'
	context = {'TodayList': todayPosts, 'YesterdayList': yesterdayPosts, 'MonthList': monthPosts, 'OtherList': otherPosts}
	return render(request, template_name, context)

def blog_post_create(request):
	form = BlogPostForm(request.POST or None)
	if form.is_valid():
		new_post=form.save(commit=False)
		new_post.pub_date = timezone.now()
		query_slug=slugify(new_post.title)+"%"
		with connection.cursor() as cursor:
			cursor.execute("SELECT COUNT(*) FROM blog_blogpost WHERE slug LIKE %(pattern)s", {'pattern': query_slug})
			result=cursor.fetchone()
			number=result[0]+1
		new_slug=slugify(new_post.title)+"-"+str(number)
		new_post.slug=new_slug
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