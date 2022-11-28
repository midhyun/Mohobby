from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_safe
from django.http import HttpResponseRedirect
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  
            auth_login(request, user)  # 로그인
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)

@require_safe
def login(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                auth_login(request, login_form.get_user())

                return redirect(request.GET.get("next") or "articles:main")

        else:
            login_form = AuthenticationForm()

        context = {
            "login_form": login_form,
        }
        return render(request, "accounts/login.html", context)
    else:
        return HttpResponseRedirect("/")