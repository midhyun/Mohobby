from django.shortcuts import render, redirect
from .models import Community, Comment, Photo
from .forms import CommunityForm, CommentForm, ReCommentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

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
            post.user = request.user
            post.save()
            for image in request.FILES.getlist("images"):
                photo = Photo()
                photo.post = post
                photo.image = image
                photo.save()
            return redirect("community:index")
    else:
        post_form = CommunityForm()
    context = {
        "post_form": post_form,
    }
    return render(request, "community/create.html", context)


def update(request, community_pk):
    post = get_object_or_404(Community, pk=community_pk)
    # 커뮤니티의 해당 글의 사진이미지 전체 받아온다.
    photo_list = post.photo_set.all()
    if post.user == request.user:
        if request.method == "POST":
            post_form = CommunityForm(request.POST, request.FILES, instance=post)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.save()

                if request.FILES.getlist("images"):
                    for img in photo_list:
                        img.delete()
                    # 이미지 삭제(초기화)하고 난뒤 이미지 저장
                    for image in request.FILES.getlist("images"):
                        photo = Photo()
                        photo.post = post
                        photo.image = image
                        photo.save()
                    return redirect("community:detail", post.pk)
                else:
                    if request.POST.getlist("image-clear"):
                        for img in photo_list:
                            img.delete()
                    return redirect("community:detail", post.pk)
        else:
            post_form = CommunityForm(instance=post)
        context = {
            "post_form": post_form,
            "photo_list": photo_list,
        }
        return render(request, "community/update.html", context)
    else:
        return HttpResponseForbidden()
