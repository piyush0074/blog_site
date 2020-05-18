from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as save_login
from django.contrib.auth.forms import AuthenticationForm as AF
from django import forms 
from .form import *
from main.models import *
from django.contrib.auth.models import User 
from post.form import Post
from post.form import Comments
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string

import redis
#import rcache
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

#CACHE_TTL = getattr(settings, 'CACHE_TTL',DEFAULT_TIMEOUT)
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT, db=0)

# Create your views here.

def login(request):
	if request.method=="POST":
		form = AF(request,data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username,password=password)	
			if user is not None:
				save_login(request,user)
				messages.success(request, "Logged in")
				return redirect('/home/')
	form = AF()
	return render(request=request,template_name="login.html",context={"form":form})


def signup(request):
	form = NewUserForm(request.POST or None)
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			save_login(request,user)
			return redirect('/')
	form = NewUserForm
	return render(request=request,template_name="signup.html",context={"form":form})

def logout_usernow(request):
	logout(request)
	messages.success(request, "Logged Out!!!")
	return redirect('/login/')

class home(TemplateView):
	template_name = 'home.html'
	def get( self, request):
		#if 'postt' in redis_instance.keys("*"):
			#posts = cache.get('postt')
		#	posts[key.decode("utf-8")] = redis_instance.get(key)
		#	args = {'form':form, 'posts':posts}
		#	return render(request,self.template_name,args)
		#else:
		#if not redisintance :
		form = PostForm()
		posts = Post.objects.all()#[:5]
		#value = readytoset(posts)
		args = {'form':form,'posts':posts}
		return render(request,self.template_name,args)
	def post(self,request):
		form = PostForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				form = form.save(commit=False)
				form.user = request.user
				form.save()
				form = PostForm()	
		args = {'form': form}
		return  redirect('/home/')
	
class profile(TemplateView):
	template_name = 'profile.html'
	def get(self,request):
		posts = Post.objects.filter(user = request.user)
		args = {'posts':posts}
		print(posts)
		return render(request,self.template_name,args)

class search(TemplateView):
	template_name = 'search.html'
	def get(self,request):
		if request.method == 'GET':
			query = request.GET.get('q')
			submitbutton = request.GET.get('submit')
			if query is not None:
				lookups = Q(username=query)
				results = User.objects.filter(username=query)
				context = {'results':results,'submitbutton':submitbutton}
			return render(request,self.template_name,context)
		#else:
		return render(request,self.template_name)
	#else:
	#return render(request,self.template_name)
class postshown(TemplateView):
	template_name = 'post.html'
	def get( self, request):
		form = CommentForm()
		button = False
		idd = int(request.GET.get('postid'))
		posts = Post.objects.get(post_id=idd)
		cmt = Comments.objects.filter(post_id=idd)
		comment = Comments.objects.filter(post_id=idd).count()
		like_count = LikeDislike.objects.filter(post_id=idd).filter(value='1').count()
		print(like_count)
		dislike_count = LikeDislike.objects.filter(post_id=idd).filter(value='2').count()
		if request.user == posts.user:
			button = True
		args = {'form':form, 'posts':posts,'cmt':cmt,'comment':comment,'like_count':like_count,'dislike_count':dislike_count,'button':button}
		return render(request,self.template_name,args)
	def post(self,request):
		form = CommentForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				form =form.save(commit=False)
				form.user = request.user
				idd = int(request.GET.get('postid'))
				form.post_id = idd
				print(form.comment)
				form.save()
				form = CommentForm()
		args = {'form':form}
		return render(request,self.template_name,args)
def like(request):
	postid = int(request.POST.get('postid'))
	is_liked = False
	if LikeDislike.objects.filter(post_id=postid,user=request.user):
		if LikeDislike.objects.filter(post_id=postid,user=request.user,value='1'):
			obj = LikeDislike.objects.filter(post_id=postid).filter(user=request.user).filter(value='1')
			obj.delete()
		else:
			obj = LikeDislike.objects.filter(post_id=postid).filter(user=request.user).update(value='1')
			obj.save()
	else:
		obj = LikeDislike(user=request.user,post_id=postid,value='1')
		obj.save()
		is_liked = True
	like_count = LikeDislike.objects.filter(post_id=postid).filter(user=request.user).filter(value='1').count()
	args = {'is_liked':is_liked,'like_count':like_count}
	if request.is_ajax():
		html = render_to_string('like_section.html',args,request=request)
		return JsonResponse({'form':html})

def dislike(request):
	postid = int(request.POST.get('postid'))
	is_liked = False
	if LikeDislike.objects.filter(post_id=postid,user=request.user):
		if LikeDislike.objects.filter(post_id=postid,user=request.user,value='2'):
			obj = LikeDislike.objects.filter(post_id=postid).filter(user=request.user).filter(value='2')
			obj.delete()
		else:
			obj = LikeDislike.objects.filter(post_id=postid).filter(user=request.user).update(value='2')
			obj.save()
	else:
		obj = LikeDislike(user=request.user,post_id=postid,value='2')
		obj.save()
		is_liked = True
	dislike_count = LikeDislike.objects.filter(post_id=postid).filter(user=request.user).filter(value='2').count()
	args = {'is_liked':is_liked,'dislike_count':dislike_count}
	if request.is_ajax():
		html = render_to_string('like_section.html',args,request=request)
		return JsonResponse({'form':html})


def delete(request):
	postid = int(request.GET.get('postid'))
	uid = request.user.id
	like = LikeDislike.objects.filter(post_id=postid)
	like.delete()
	comment = Comments.objects.filter(post_id=postid)
	comment.delete()
	post = Post.objects.get(post_id=postid)
	post.delete()
	return redirect('/home/')





