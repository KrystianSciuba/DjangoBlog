"""try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from .views import (
	home_page,
	about_page,
	contact_page,
	test_page,
    login_page,
    newest_post_page,
    logout_page,
    register_page
)

from blog.views import (
    blog_post_create
)

from users.views import (
    settings_page
)
urlpatterns = [

	path('', home_page, name="home_page"),
	re_path(r'pages?/$', about_page),

    path('blog-new/', blog_post_create),
    path('blog/', include('blog.urls')),
    path('user/', include('users.urls')),

    path('settings', settings_page),
    path('newest-post/', newest_post_page),    
	path('about/', about_page),
	path('contact/', contact_page),
    path('admin/', admin.site.urls),
    path('test/', test_page),
    path('login/', login_page, name= "login"),
    path('logout/', logout_page),
    path('register/', register_page)

]
