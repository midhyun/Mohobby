from django.shortcuts import render, redirect
from .forms import HobbyForm
from .models import Hobby
from django.contrib.auth.decorators import login_required

# Create your views here.


def create(request):
    if request.method == "POST":
        form = HobbyForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.host = request.user
            temp.tags = tag
            temp.save()
            return redirect("main")
    else:
        form = HobbyForm()
    context = {
        "form": form,
    }
    return render(request, "hobby/form.html", context)


def index(request, category_name):
    # category_posts = Hobby.objects.filter(category=category_name)
    context = {
        "category_name": category_name,
    }
    return render(request, "hobby/index.html", context)


def tag(request, category_name, tag_name):
    return render(request)
