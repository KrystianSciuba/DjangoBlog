from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from blog.models import BlogPost
from .forms import UserForm
from django.db import connection
from django.contrib.auth import authenticate, login, logout


def home_page(request):
	my_title="Hello there!!!"
	return render(request, "home.html", {"title": my_title})

def about_page(request):
	return render(request, "about.html",{"title":"About Us"})

def login_page(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect ('home_page')
		else:
			return render(request, "login.html", {"message": "invalid credentials"})
	else:
		return render(request, "login.html", {"title": "LOG IN"})

def register_page(request):
	new_user_form = UserForm(request.POST or None)

	if new_user_form.is_valid():
		new_user=new_user_form.save(commit=False)
		username=new_user_form.cleaned_data['username']
		password=new_user_form.cleaned_data['password']
		new_user.set_password(password)
		new_user.save()

		user=authenticate(username=username, password=password)
		if user is not None:
			if user.is_authenticated:
				login(request, user)
				return redirect ('home_page')
	template='register.html'
	return render(request, template, {'new_user_form': new_user_form})


def logout_page(request):
	logout(request)
	return redirect ('home_page')

def contact_page(request):
	return render(request, "contact.html",{"title":"Contact Us"})


def example_page(request):
	context			= {"title": "Example"}
	template_name	= "hello_world.html"
	template_obj 	= get_template (template_name)
	return HttpResponse(template_obj.render(context))

def test_page(request):
	my_title="TEST!!!"
	context={"title":my_title}
	if request.user.is_authenticated:
		context={"title":my_title, "my_list": [1, 2, 3, 4, 5]}
	return render(request, "test.html", context)

def newest_post_page(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT slug FROM blog_blogpost ORDER BY pub_date DESC LIMIT 1")
		last_post=cursor.fetchone()
		last_post_slug=last_post[0]

		return redirect('blog_post_detail_view', slug=last_post_slug)
