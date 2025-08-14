from django import forms
from .models import Book


class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ["title", "author", "publication_year"]

	def clean_title(self):
		title = self.cleaned_data.get("title", "").strip()
		return title


class ExampleForm(forms.Form):
	title = forms.CharField(max_length=255)

