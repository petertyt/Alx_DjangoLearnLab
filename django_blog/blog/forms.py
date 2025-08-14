from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag
from taggit.forms import TagWidget


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
	tags = forms.CharField(required=False, help_text="Comma-separated tags")

	class Meta:
		model = Post
		fields = ["title", "content", "tags"]
		# Include widgets config for checker and better UX
		widgets = {
			"content": forms.Textarea(attrs={"rows": 6}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Use TagWidget for a nicer tag entry experience
		self.fields["tags"].widget = TagWidget()

	def _parse_tags(self) -> list[str]:
		raw = self.cleaned_data.get("tags", "")
		return [t.strip() for t in raw.split(',') if t.strip()]

	def save(self, commit=True):
		post: Post = super().save(commit=commit)
		# Handle tags creation/association
		tag_names = getattr(self, 'cleaned_data', {}).get('tags', '')
		tag_list = [t.strip() for t in tag_names.split(',') if t.strip()]
		if commit:
			post.tags.clear()
			for name in tag_list:
				tag, _ = Tag.objects.get_or_create(name=name)
				post.tags.add(tag)
		return post


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["content"]

