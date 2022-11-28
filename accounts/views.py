from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_safe
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  
            auth_login(request, user)  # 로그인
            return redirect("articles:login")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)

@require_safe
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:detail")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)
    
@login_required
def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)

def follow(request, pk):
    accounts = get_user_model().objects.get(pk=pk)
    if request.user == accounts:
        return redirect("accounts:detail", pk)
    if request.user in accounts.followers.all():
        accounts.followers.remove(request.user)
        accounts.save()
    else:
        accounts.followers.add(request.user)
        accounts.save()
    # 상세 페이지로 redirect
    return redirect("accounts:detail", pk)

@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("articles:index")