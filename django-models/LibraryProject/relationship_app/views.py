from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library


def list_books(request: HttpRequest) -> HttpResponse:
	books = Book.objects.all()
	# If templates are preferred, render the HTML template; otherwise return plain text
	if request.GET.get("format") == "html":
		return render(request, "relationship_app/list_books.html", {"books": books})

	lines = [f"{book.title} by {book.author.name}" for book in books]
	return HttpResponse("\n".join(lines) or "No books available")


class LibraryDetailView(DetailView):
	model = Library
	template_name = "relationship_app/library_detail.html"
	context_object_name = "library"

	def get_object(self):
		return get_object_or_404(Library.objects.prefetch_related("books__author"), pk=self.kwargs["pk"])
