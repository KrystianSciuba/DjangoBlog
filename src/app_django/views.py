from django.shortcuts import render, redirect
from blog.models import BlogPost
from .forms import UserForm
from django.db import connection
from django.contrib.auth import authenticate, login, logout


def home_page(request):
	class Post(object):
		def __init__(self, title, slug, pub_date, content):
			self.title = title
			self.slug = slug
			self.pub_date = pub_date
			self.content = content

	with connection.cursor() as cursor:

		cursor.execute("SELECT title, slug, pub_date, content  FROM blog_blogpost ORDER BY pub_date DESC LIMIT 5")
		rows = cursor.fetchall()
		posts=[]
		for row in rows:
			posts.append(Post(row[0],row[1],row[2],row[3]))

	template="home.html"
	context = {'posts': posts}
	return render(request, template, context)

def about_page(request):
	template="about.html"
	return render(request, template)

def login_page(request):
	if request.user.is_authenticated:
		return redirect ('home_page')
	else:
		template="login.html"
		if request.method=='POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect ('login')
			else:
				message={"message": "invalid credentials"}
				return render(request, template, message)
		else:
			return render(request, template)

def register_page(request):
	template='register.html'
	new_user_form = UserForm(request.POST or None)

	if new_user_form.is_valid():
		new_user=new_user_form.save(commit=False)
		username=new_user_form.cleaned_data['username']
		password=new_user_form.cleaned_data['password']
		new_user.set_password(password)
		new_user.save()
		if new_user is not None:
			return redirect ('login')
	return render(request, template,{'new_user_form': new_user_form})


def logout_page(request):
	logout(request)
	return redirect ('login')

def contact_page(request):
	template='contact.html'
	return render(request, template)

def test_page(request):
	template='test.html'
	if request.user.is_authenticated:
		content={"my_list": [1, 2, 3, 4, 5]}
		return render(request, template, content)
	return render(request, template)

def newest_post_page(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT slug FROM blog_blogpost ORDER BY pub_date DESC LIMIT 1")
		last_post=cursor.fetchone()
		last_post_slug=last_post[0]
		return redirect('blog_post_detail_view', slug=last_post_slug)
