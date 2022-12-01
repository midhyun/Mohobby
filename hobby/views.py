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
