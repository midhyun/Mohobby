from django.shortcuts import render, redirect, get_object_or_404
from .forms import HobbyForm, AcceptedForm, CommentForm
from .models import Hobby, Accepted, Tag, HobbyComment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Avg, Count, Max, Case, When, IntegerField, Q
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
    comments = HobbyComment.objects.filter(hobby=hobby).order_by('-pk')
    accepted = Accepted.objects.filter(hobby=hobby, joined=True)
    waiting = Accepted.objects.filter(hobby=hobby, joined=False)
    context = {
        'hobby':hobby,
        'accepted': accepted,
        'waiting': waiting,
        'comments':comments,        
    }
    return render(request, "hobby/detail.html", context)


# 카테고리별 인기글 , 최신글, 전체 글
def index(request, category_name):
    category_posts = Hobby.objects.filter(category=category_name).annotate(joinmembers = Count('accepted', filter=Q(accepted__joined=True)))
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
        tag_posts = (
            Hobby.objects.all().order_by("-pk").annotate(joinmembers=Count("accepted", filter=Q(accepted__joined=True)))
        )
    else:
        tag_posts = Hobby.objects.filter(tags=tag_name)

    context = {
        "tag_posts": tag_posts,
        "tag_name": tag_name,
    }

    return render(request, "hobby/tag.html", context)


def call(request, hobby_pk):
    hobby = get_object_or_404(Hobby, pk=hobby_pk)
    accepted = Accepted.objects.filter(hobby=hobby, user=request.user)
    if not accepted.exists():
        aform = AcceptedForm()
        temp = aform.save(commit=False)
        temp.hobby = hobby
        temp.user = request.user
        temp.save()
        print('호스트의 승인을 기다려주세요.')
    else:
        print("이미 신청한 소셜링입니다.")
    return redirect("hobby:detail", hobby_pk)


def approve(request, hobby_pk, user_pk):
    hobby = get_object_or_404(Hobby, pk=hobby_pk)
    if request.user == hobby.host:
        accepted = get_object_or_404(Accepted, hobby=hobby, user_id=user_pk)
        accepted.joined = True
        accepted.save()
        print(f'{request.user}님의 가입을 승인했습니다.')
    else:
        print("권한이 없습니다.")
    return redirect("hobby:detail", hobby_pk)


def reject(request, hobby_pk, user_pk):
    hobby = get_object_or_404(Hobby, pk=hobby_pk)
    if request.user == hobby.host and user_pk != hobby.host.pk:
        accepted = get_object_or_404(Accepted, hobby=hobby, user_id=user_pk)
        accepted.delete()
    else:
        print('권한이 없습니다.')
    return redirect('hobby:detail', hobby_pk)

def comment_create(request, hobby_pk):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            temp = comment_form.save(commit=False)
            temp.user = request.user
            temp.hobby_id = hobby_pk
            temp.save()
    comments = HobbyComment.objects.filter(hobby_id=hobby_pk).order_by('-pk')
    comments_data = []
    for comment in comments:
        if request.user in comment.like_user.all():
            is_like = True
        else: is_like = False
        created_at = comment.created_at.strftime('%Y-%m-%d %H:%M')
        comments_data.append({
            "pk": comment.pk,
            "user": comment.user.username,
            "content": comment.content,
            "created_at": created_at,
            "is_like": is_like,
            'likeCount': comment.like_user.count(),
        })
    context = {
        "comments_data": comments_data,
    }
    return JsonResponse(context)

def comment_delete(request, comment_pk):
    comment = get_object_or_404(HobbyComment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    else:
        print('권한이 없습니다.')
    return JsonResponse({})

def comment_like(request, comment_pk):
    comment = get_object_or_404(HobbyComment, pk=comment_pk)
    if request.user not in comment.like_user.all():
        comment.like_user.add(request.user)
        is_like = True
    else:
        comment.like_user.remove(request.user)
        is_like = False
    data = {
        'is_like': is_like,
        'likeCount': comment.like_user.count(),
    }
    return JsonResponse(data)

def like_hobby(request, hobby_pk):
    hobby = get_object_or_404(Hobby, pk=hobby_pk)
    if request.user not in hobby.like_user.all():
        hobby.like_user.add(request.user)
        is_like = True
    else:
        hobby.like_user.remove(request.user)
        is_like = False
    data = {
        'is_like': is_like,
        'likeCount': hobby.like_user.count()
    }
    return JsonResponse(data)

def like_comment(request, comment_pk):
    comment = get_object_or_404(HobbyComment, pk=comment_pk)
    if request.user not in comment.like_user.all():
        comment.like_user.add(request.user)
        is_like = True
    else:
        comment.like_user.remove(request.user)
        is_like = False
    data = {
        'is_like': is_like,
        'likeCount': comment.like_user.count()
    }
    return JsonResponse(data)