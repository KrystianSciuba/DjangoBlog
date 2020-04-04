from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import connection

def user_page_view(request, username):
	class Post(object):
		def __init__(self, title, slug):
			self.title = title
			self.slug = slug
			
	user = get_object_or_404(User, username=username)
	with connection.cursor() as cursor:
		cursor.execute("SELECT title, slug FROM blog_blogpost WHERE author_id=%(author)s ORDER BY pub_date DESC", {'author': user.id})
		rows = cursor.fetchall()
		userPosts=[]
		for row in rows:
			userPosts.append(Post(row[0],row[1]))

	context = {'user': user, 'user_post_list': userPosts}
	template_name = 'userpage.html'

	return render(request, template_name, context)





def settings_page(request):
	if request.user.is_authenticated:
		template_name = 'settings.html'
		context = {'user': request.user}
		return render(request, template_name, context)
	else:
		return redirect("login")
