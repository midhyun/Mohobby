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
        if comment.user.image:
            image = comment.user.image.url
        else: image = 'https://dummyimage.com/80x80/000/fff'
        comments_data.append({
            "pk": comment.pk,
            "user": comment.user.nickname,
            "content": comment.content,
            "created_at": created_at,
            "is_like": is_like,
            "image": image,
            'likeCount': comment.like_user.count(),
        })
    context = {
        "comments_data": comments_data,
    }
    return JsonResponse(context)

def comment_delete(request, comment_pk):
    comment = get_object_or_404(HobbyComment, pk=comment_pk)
    hobby_pk = comment.hobby.pk
    if comment.user == request.user:
        comment.delete()
    else:
        print('권한이 없습니다.')
    comments = HobbyComment.objects.filter(hobby_id=hobby_pk).order_by('-pk')
    comments_data = []
    for comment in comments:
        if request.user in comment.like_user.all():
            is_like = True
        else: is_like = False
        created_at = comment.created_at.strftime('%Y-%m-%d %H:%M')
        if comment.user.image:
            image = comment.user.image.url
        else: image = 'https://dummyimage.com/80x80/000/fff'
        comments_data.append({
            "pk": comment.pk,
            "user": comment.user.nickname,
            "user_pk": comment.user.pk,
            "content": comment.content,
            "created_at": created_at,
            "is_like": is_like,
            "image": image,
            'likeCount': comment.like_user.count(),
        })
    context = {
        "comments_data": comments_data,
    }
    return JsonResponse(context)

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


# 카테고리별 태그 저장
def save(request):
    lsit_1 = [
        "야구",
        "클라이밍",
        "등산",
        "테니스",
        "트래킹",
        "볼링",
        "러닝",
        "스키",
        "보드",
        "헬스",
        "산책",
        "플로깅",
        "자전거",
        "서핑",
        "배드민턴",
        "탁구",
        "골프",
        "스포츠경기",
    ]
    list_2 = [
        "복합문화공간",
        "테마파크",
        "피크닉",
        "드라이브",
        "캠핑",
        "국내여행",
        "해외여행",
    ]
    list_3 = [
        "전시",
        "영화",
        "뮤지컬",
        "공연",
        "디자인",
        "박물관",
        "연극",
        "콘서트",
        "연주회",
        "페스티벌",
    ]

    list_4 = [
        "맛집투어",
        "카페",
        "와인",
        "커피",
        "디저트",
        "맥주",
        "티룸",
        "비건",
        "파인다이닝",
        "요리",
        "페어링",
        "칵테일",
        "위스키",
        "전통주",
    ]
    list_5 = [
        "습관만들기",
        "챌린지",
        "독서",
        "스터디",
        "외국어",
        "재테크",
        "브랜딩",
        "커리어",
        "사이드프로젝트",
    ]
    for i in range(len(lsit_1)):
        tag = Tag()
        tag.tag = lsit_1[i]
        tag.category = "sports"
        tag.save()

    for i in range(len(list_2)):
        tag = Tag()
        tag.tag = list_2[i]
        tag.category = "travel"
        tag.save()
    for i in range(len(list_3)):
        tag = Tag()
        tag.tag = list_3[i]
        tag.category = "art"
        tag.save()
    for i in range(len(list_4)):
        tag = Tag()
        tag.tag = list_4[i]
        tag.category = "food"
        tag.save()
    for i in range(len(list_5)):
        tag = Tag()
        tag.tag = list_5[i]
        tag.category = "develop"
        tag.save()

    return redirect("main")
    
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

