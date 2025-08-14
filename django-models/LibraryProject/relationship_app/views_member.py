from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render


def is_member(user) -> bool:
	return hasattr(user, "profile") and user.profile.role == "Member"


@login_required
@user_passes_test(is_member)
def member_view(request: HttpRequest) -> HttpResponse:
	return render(request, "relationship_app/member_view.html")

