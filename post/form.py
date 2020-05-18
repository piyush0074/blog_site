from django import forms
from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from main.models import Post
from main.models import Comments



class NewUserForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields= ("username","email","password1","password2")
	def save(self,commit=True):
		user= super(NewUserForm,self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class PostForm(ModelForm):
	post = forms.CharField(required=True)
	class Meta:
		model = Post
		fields = ('post',)

class CommentForm(ModelForm):
	comment = forms.CharField(required=True)
	class Meta:
		model = Comments
		fields = ('comment',)
