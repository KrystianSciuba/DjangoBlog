from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

def user_page_view(request, username):
	user = get_object_or_404(User, username=username)
	template_name = 'detail.html'
	context = {'user': user}
	return render(request, template_name, context)