from django.shortcuts import render, redirect
from .models import Community, Comment
from .forms import CommunityForm, CommentForm, ReCommentForm

# Create your views here.
def index(request):
    posts = Community.objects.order_by("-pk")
    context = {"posts": posts}
    return render(request, "community/index.html", context)


def create(request):
    if request.method == "POST":
        post_form = CommunityForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            # post.user = request.user
            post.save()
            return redirect("community:index")
    else:
        post_form = CommunityForm()
    context = {
        "post_form": post_form,
    }
    return render(request, "community/create.html", context)
