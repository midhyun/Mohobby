
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
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
import requests, os




# Create your views here.


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")  # 로그인
            return redirect("main")
        else:
            messages.warning(request, '필수 정보를 입력해주세요.')
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def id_check(request):
    accounts = [i.username for i in get_user_model().objects.all()]
    data = {"accounts": accounts}
    return JsonResponse(data)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("main")
        else:
            messages.warning(request, '비밀번호나 아이디가 틀립니다.')
    else:
        form = AuthenticationForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    messages.warning(request, '로그아웃 하였습니다.')
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


def password_change(request, pk):
    user_info = get_user_model().objects.get(pk=pk)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("accounts:detail", user_info.pk)
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        "form" : form
    }
    return render(request, 'accounts/password.html', context)


def kakao_login(request):
    app_key = os.getenv("KAKAO_REST_API_KEY")
    redirect_uri = 'http://localhost:8000/accounts/login/kakao/callback'
    kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'

    return redirect(
        # 서버의 정보를 카카오 로그인 페이지에 전송하게된다.
        f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}'
    )



def KakaoCallBack(request):
    auth_code = request.GET.get('code')
    kakao_token_api = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv("KAKAO_REST_API_KEY"),
        'redirection_uri': 'http://localhost:8000/accounts/login/kakao/callback',
        'code': auth_code,
    }
    token_response = requests.post(kakao_token_api, data=data)
    
    # 발급받은 토큰
    access_token = token_response.json().get('access_token')
    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})

    # json 파일로 카카오 계정 정보 받아오기
    kakao_user_data = user_info_response.json()

    # 일단 닉네임만. 받을 수 있는 개인정보는 설정으로 바꿀수있음.
    kakao_user_nickname = kakao_user_data['properties']['nickname']
    

    # 1.
    
    # filter 활용 username(id)에 카카오 user_nickname 존재하는지 확인 (problem.1 : 카카오 닉네임이 같은 경우는?)
    if get_user_model().objects.filter(username=kakao_user_nickname).exists():
        # 존재하는 경우 유저의 오브젝트를 가져오고 로그인 후 메인페이지로 리다이렉트
        kakao_user = get_user_model().objects.get(username=kakao_user_nickname)
        auth_login(request, kakao_user)
        return redirect(request.GET.get("next") or "main")
    # 서버 DB에 존재하지 않는 경우
    else:
        # username을 DB에 젖아하고 로그인 후 소셜 로그인 전용 회원가입 페이지로 넘겨줌.
        kakao_login_user = get_user_model()()
        kakao_login_user.username = kakao_user_nickname
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(username=kakao_user_nickname)
    
        auth_login(request, kakao_user)
        return redirect("accounts:social_signup", kakao_user.pk)

    # 2. 위와 같은 방법을 카카오의 고유 ID로 바꾼 로직

    # if get_user_model().objects.filter(kakao_id=kakao_user_id).exists():
    #     kakao_user = get_user_model().objects.get(kakao_id=kakao_user_id)
    #     auth_login(request, kakao_user)
    #     return redirect(request.GET.get("next") or "main")
    # else:
    #     kakao_login_user = get_user_model()()
    #     kakao_login_user.username = kakao_user_nickname
    #     kakao_login_user.kakao_id = kakao_user_id
    #     kakao_login_user.save()
    #     kakao_user = get_user_model().objects.get(kakao_id=kakao_user_id)
    
    #     auth_login(request, kakao_user)
    #     return redirect("accounts:social_signup", kakao_user.pk)

@login_required
def social_signup(request, pk):
    user_info = get_user_model().objects.get(pk=pk)
    # 로그인한 유저가 찾는 유저가 맞는지 확인
    if request.user == user_info:
        if request.method == "POST":
            # 소셜 회원가입이지만 커스텀폼 재활용. 따로 만들어도 문제없음
            form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("main")
            else:
                # 필수 정보를 입력하지 않았을 때 출력하는 에러메시지 
                messages.warning(request, '필수 정보를 입력해주세요.')
        else:
            form = CustomUserChangeForm(instance=request.user)
    

    context = {
        "form": form,
        "user_info": user_info,
    }

    return render(request, 'accounts/social_signup.html', context)

