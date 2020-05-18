"""post URL Configuration
maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from post import views
from django.conf.urls import url
urlpatterns = [
    #path('admin/', admin.site.urls),
	path('admin/', admin.site.urls),
	path('',views.login,name='login'),
	path('login/',views.login,name='login'),
	path('signup/',views.signup,name='signup'),
	path('home/',views.home.as_view(),name='home'),
	path('logout/',views.logout_usernow,name='logout'),
	path('post/',views.postshown.as_view(),name='post'),
	path('profile/',views.profile.as_view(),name='profile'),
	path('search/',views.search.as_view(),name='search'),
	path('like/',views.like,name='like'),
	path('dislike/',views.dislike,name='dislike'),
	path('delete/',views.delete,name='delete'),
	#url(r'^$',views.search.as_view(),name='search'),
]

