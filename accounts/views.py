from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_safe, require_http_methods
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # 로그인
            return redirect("main")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)

def id_check(request):
    accounts = [i.username for i in get_user_model().objects.all()]
    data = {
        'accounts' : accounts
    }
    return JsonResponse(data)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("main")
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
    return redirect("main")


@login_required
def update(request, pk):
    user_info = get_user_model().objects.get(pk=pk)
    # 요청한 유저가 로그인한 해당 유저인 경우
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        # 유저폼 유효성 확인
        if user_form.is_valid():
            user_form.save()
            return redirect("accounts:detail", user_info.pk)
    else:
        user_form = CustomUserChangeForm(instance=request.user)
    context = {
        "user_form": user_form,
        "user_info": user_info,
    }
    return render(request, "accounts/update.html", context)

def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 변경하였습니다.")
            return redirect('main')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        "form" : form
    }



    return render(request, 'accounts/password.html', context)
