from django.shortcuts import render, redirect
from .forms import HobbyForm
from .models import Hobby, Tag
from django.contrib.auth.decorators import login_required

# Create your views here.


def create(request):
    if request.method == "POST":
        form = HobbyForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.host = request.user
            temp.save()
            return redirect("main")
        else:
            pass
    else:
        form = HobbyForm()
    context = {
        "form": form,
    }
    return render(request, "hobby/form.html", context)


def test(request):
    return render(request, "hobby/test.html")


# 카테고리별 인기글 , 최신글, 전체 글
def index(request, category_name):
    category_posts = Hobby.objects.filter(category=category_name)
    category_posts_hit = category_posts.order_by("-hits")[:3]
    category_posts_new = category_posts.order_by("-pk")[:3]
    tags = Tag.objects.filter(category=category_name)
    context = {
        "category_name": category_name,
        "category_posts": category_posts,
        "category_posts_hit": category_posts_hit,
        "category_posts_new": category_posts_new,
        "tags": tags,
    }
    return render(request, "hobby/index.html", context)


# 전체 인기글, 최신글, 태그글 모음
def tag(request, tag_name):
    if tag_name == "hits":
        tag_posts = Hobby.objects.all().order_by("-hits")
    if tag_name == "news":
        tag_posts = Hobby.objects.all().order_by("-pk")
    else:
        tag_posts = Hobby.objects.filter(tags=tag_name)
    context = {
        "tag_posts": tag_posts,
        "tag_name": tag_name,
    }

    return render(request, "hobby/tag.html", context)
