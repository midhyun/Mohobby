from django.shortcuts import render, redirect
from .forms import HobbyForm
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

def index(request):
    return render(request, "hobby/index.html")

