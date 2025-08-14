from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render


def is_admin(user) -> bool:
	return hasattr(user, "profile") and user.profile.role == "Admin"


@login_required
@user_passes_test(is_admin)
def admin_view(request: HttpRequest) -> HttpResponse:
	return render(request, "relationship_app/admin_view.html")

