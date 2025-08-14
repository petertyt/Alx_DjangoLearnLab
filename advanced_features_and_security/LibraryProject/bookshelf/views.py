from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request: HttpRequest) -> HttpResponse:
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})
