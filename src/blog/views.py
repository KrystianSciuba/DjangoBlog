from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from slugify import slugify
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import User
from collections import namedtuple

import datetime

# Create your views here.
from .forms import BlogPostForm, BlogPostCommentForm
from .models import BlogPost, BlogPostComment

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def blog_post_list_view(request):

	now=datetime.datetime.now()
	today=datetime.date.today()
	yesterday=datetime.date.today()-datetime.timedelta(1)
	first_of_month=today.replace(day=1)
	if yesterday < first_of_month:
		other_date=yesterday
	else:
		other_date=first_of_month

	with connection.cursor() as cursor:

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN %(date1)s AND %(date2)s ORDER BY pub_date DESC", {'date1': today, 'date2': now})
		todayPosts = namedtuplefetchall(cursor)

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN %(date1)s AND %(date2)s ORDER BY pub_date DESC", {'date1': yesterday, 'date2': today})
		yesterdayPosts = namedtuplefetchall(cursor)

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN %(date1)s AND %(date2)s ORDER BY pub_date DESC",{'date1': first_of_month, 'date2': yesterday})
		monthPosts = namedtuplefetchall(cursor)

		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE pub_date BETWEEN 0 AND %(date)s ORDER BY pub_date DESC",{'date': other_date})
		otherPosts = namedtuplefetchall(cursor)

	template_name = 'blog/list.html'
	context = {'TodayList': todayPosts, 'YesterdayList': yesterdayPosts, 'MonthList': monthPosts, 'OtherList': otherPosts}
	return render(request, template_name, context)

def blog_post_create(request):
	form = BlogPostForm(request.POST or None)
	if form.is_valid():
		new_post=form.save(commit=False)
		new_post.pub_date = timezone.now()
		new_post.author=request.user
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
	author = get_object_or_404(User, id=post.author_id)

	with connection.cursor() as cursor:
		cursor.execute("SELECT author, content, pub_date FROM blog_blogpostcomment WHERE blogpost_id=%(id)s ORDER BY pub_date DESC", { 'id': post.id })
		results = cursor.fetchall()
		comments=[]
		for result in results:
			comments.append(Comment(author=result[0], content=result[1], pub_date=result[2]))

	form = BlogPostCommentForm(request.POST or None)
	if form.is_valid():
		new_comment=form.save(commit=False)
		new_comment.pub_date = timezone.now()		
		new_comment.blogpost=post
		new_comment.save()
		return redirect('blog_post_detail_view', slug=post.slug)

	template_name = 'blog/detail.html'
	context = {'post': post,'comments':comments, 'form': form, 'author':author}
	return render(request, template_name, context)



def blog_post_update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'blog/update.html'
	context = {'object': obj, 'form': None}
	return render(request, template_name, context)

def blog_post_delete_view(request, slug):
	post = get_object_or_404(BlogPost, slug=slug)
	if request.user.id==post.author_id:
		if request.method == 'POST':
			post.delete()
			return redirect ('userpage', username=request.user.username)
		template_name = 'blog/delete.html'
		context = {'object': post}
		return render(request, template_name, context)
	else:
		return redirect('blog_post_detail_view', slug=post.slug)