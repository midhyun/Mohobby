from django.shortcuts import render, redirect, get_object_or_404
from .forms import HobbyForm, AcceptedForm
from .models import Hobby, Accepted, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

# Create your views here.


def create(request):
    print(request.method)
    if request.method == "POST":
        form = HobbyForm(request.POST, request.FILES)
        accepted = AcceptedForm()
        print(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.host = request.user
            temp.save()
            atemp = accepted.save(commit=False)
            atemp.joined = True
            atemp.hobby = temp
            atemp.user = request.user
            atemp.save()
            return redirect("main")
    else:
        form = HobbyForm()
    context = {
        "form": form,
    }
    return render(request, "hobby/form.html", context)


def test(request):
    return render(request, "hobby/test.html")

def detail(request, hobby_pk):
    hobby = Hobby.objects.get(pk=hobby_pk)
    context = {
        'hobby':hobby,
    }
    return render(request, "hobby/detail.html", context)

def index(request, category_name):
    category_posts = Hobby.objects.filter(category=category_name)
    category_posts_hit = category_posts.order_by("-hits")[:3]
    category_posts_new = category_posts.order_by("-created_at")[:3]
    tags = Tag.objects.filter(category=category_name)
    context = {
        "category_name": category_name,
        "category_posts": category_posts,
        "category_posts_hit": category_posts_hit,
        "category_posts_new": category_posts_new,
        "tags": tags,
    }
    return render(request, "hobby/index.html", context)


def tag(request, tag_name):
    return render(request)

def call(request, hobby_pk):
    hobby = get_object_or_404(Hobby, pk=hobby_pk)
    accepted = Accepted.objects.filter(hobby=hobby).values_list('user_id')
    if request.user.pk not in accepted[0]:
        aform = AcceptedForm()
        temp = aform.save(commit=False)
        temp.hobby = hobby
        temp.user = request.user
        temp.save()
    else:
        print('이미 신청한 소셜링입니다.')
    return redirect('hobby:detail', hobby_pk)

def approve(request, hobby_pk, user_pk):
    hobby = get_object_or_404(Hobby, pk=hobby_pk)
    if request.user == hobby.host:
        accepted = get_object_or_404(Accepted, hobby=hobby, user_id=user_pk)
        accepted.joined = True
        accepted.save()
    else:
        print('권한이 없습니다.')
    return redirect('hobby:detail', hobby_pk)

def reject(request, hobby_pk, user_pk):
    hobby = get_object_or_404(Hobby, pk=hobby_pk)
    if request.user == hobby.host and user_pk != hobby.host.pk:
        accepted = get_object_or_404(Accepted, hobby=hobby, user_id=user_pk)
        accepted.delete()
    else:
        print('권한이 없습니다.')
    return redirect('hobby:detail', hobby_pk)