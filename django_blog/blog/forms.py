from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=False, max_length=150)
	last_name = forms.CharField(required=False, max_length=150)

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def save(self, commit: bool = True) -> User:
		user: User = super().save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data.get("first_name", "")
		user.last_name = self.cleaned_data.get("last_name", "")
		if commit:
			user.save()
		return user


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ["title", "content"]


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["content"]

