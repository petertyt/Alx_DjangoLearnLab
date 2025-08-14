from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render


def is_librarian(user) -> bool:
	return hasattr(user, "profile") and user.profile.role == "Librarian"


@login_required
@user_passes_test(is_librarian)
def librarian_view(request: HttpRequest) -> HttpResponse:
	return render(request, "relationship_app/librarian_view.html")

