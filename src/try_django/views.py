from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from blog.models import BlogPost
from django.db import connection


def home_page(request):
	my_title="Hello there!!!"
	return render(request, "home.html", {"title": my_title})

def about_page(request):
	return render(request, "about.html",{"title":"About Us"})

def login_page(request):
	return render(request, "login.html",{"title":"log in"})

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
		cursor.execute("SELECT * FROM blog_blogpost ORDER BY pub_date DESC LIMIT 2")
		rows = cursor.fetchone()
		columns = [col[0] for col in cursor.description]
		obj=dict(zip(columns, rows))
	template_name = 'blog/detail.html'
	context = {'object': obj}
	return render(request, template_name, context)

