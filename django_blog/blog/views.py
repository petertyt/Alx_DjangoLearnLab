from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from .forms import RegistrationForm


def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("profile")
	else:
		form = RegistrationForm()
	return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
	if request.method == "POST":
		# Simple profile update: email, first_name, last_name
		email = request.POST.get("email", "")
		first_name = request.POST.get("first_name", "")
		last_name = request.POST.get("last_name", "")
		user: User = request.user
		user.email = email
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		return redirect("profile")
	return render(request, "blog/profile.html")

# Create your views here.
