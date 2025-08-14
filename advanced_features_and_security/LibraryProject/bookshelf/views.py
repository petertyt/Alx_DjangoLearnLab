from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import permission_required
from .forms import BookForm, ExampleForm
from .models import Book

@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request: HttpRequest) -> HttpResponse:
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('relationship_app.can_create', raise_exception=True)
def book_form_example(request: HttpRequest) -> HttpResponse:
	if request.method == 'POST':
		form = BookForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse('Saved')
	else:
		form = BookForm()
	return render(request, 'bookshelf/form_example.html', {'form': form})
