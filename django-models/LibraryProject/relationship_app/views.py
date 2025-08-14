from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test


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
