from django.shortcuts import render
from .models import Community, Comment

# Create your views here.
def index(request):
    posts = Community.objects.order_by("-pk")
    context = {"posts": posts}
    return render(request, "community/index.html", context)
