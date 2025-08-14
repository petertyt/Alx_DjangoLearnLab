from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required


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


def register(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("list_books")
	else:
		form = UserCreationForm()

	return render(request, "relationship_app/register.html", {"form": form})


# Role checks
def _is_admin(user) -> bool:
	return hasattr(user, "profile") and user.profile.role == "Admin"


def _is_librarian(user) -> bool:
	return hasattr(user, "profile") and user.profile.role == "Librarian"


def _is_member(user) -> bool:
	return hasattr(user, "profile") and user.profile.role == "Member"


@login_required
@user_passes_test(_is_admin)
def admin_view(request: HttpRequest) -> HttpResponse:
	return render(request, "relationship_app/admin_view.html")


@login_required
@user_passes_test(_is_librarian)
def librarian_view(request: HttpRequest) -> HttpResponse:
	return render(request, "relationship_app/librarian_view.html")


@login_required
@user_passes_test(_is_member)
def member_view(request: HttpRequest) -> HttpResponse:
	return render(request, "relationship_app/member_view.html")


# Secured Book actions
@login_required
@permission_required("relationship_app.can_create", raise_exception=True)
def add_book(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		title = request.POST.get("title")
		author_id = request.POST.get("author_id")
		if title and author_id:
			Book.objects.create(title=title, author_id=author_id)
			return HttpResponse("Book created")
	return HttpResponse("Provide title and author_id via POST")


@login_required
@permission_required("relationship_app.can_edit", raise_exception=True)
def edit_book(request: HttpRequest, pk: int) -> HttpResponse:
	book = get_object_or_404(Book, pk=pk)
	if request.method == "POST":
		title = request.POST.get("title")
		if title:
			book.title = title
			book.save()
			return HttpResponse("Book updated")
	return HttpResponse("Provide title via POST")


@login_required
@permission_required("relationship_app.can_delete", raise_exception=True)
def delete_book(request: HttpRequest, pk: int) -> HttpResponse:
	book = get_object_or_404(Book, pk=pk)
	if request.method == "POST":
		book.delete()
		return HttpResponse("Book deleted")
	return HttpResponse("Send POST to delete book")
