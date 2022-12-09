from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe, require_http_methods
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from datetime import date, datetime, timedelta, timezone
from .models import Product, Product_Comment
from .forms import ProductForm, Product_CommentForm, Product_ReplyForm
from django.core.paginator import Paginator
from django.utils.html import strip_tags

# Create your views here.
@require_safe
def index(request):
    products = Product.objects.select_related("user").order_by("-pk")
    page = request.GET.get("page", "1")  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(products, 4)  # Paginator(분할될 객체, 페이지 당 담길 객체 수)
    page_list = paginator.get_page(page)  # 페이지 번호를 받아 해당 페이지를 리턴
    context = {
        "page_list": page_list,
    }
    return render(request, "products/index.html", context)


@require_safe
def search(request):
    products = None
    query = None

    if "q" in request.GET:
        query = request.GET.get("q").split("&")[0]
        products = Product.objects.order_by("-pk").filter(
            Q(title__contains=query)
            | Q(productType__contains=query)
            | Q(tradeType__contains=query)
            | Q(location__contains=query)
            | Q(contentStripTag__contains=query)
        )
    page = request.GET.get("page", "1")  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(products, 8)  # Paginator(분할될 객체, 페이지 당 담길 객체 수)
    page_list = paginator.get_page(page)  # 페이지 번호를 받아 해당 페이지를 리턴
    context = {
        "query": query,
        "page_list": page_list,
    }
    return render(request, "products/search.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            if product.location == "":
                product.location = "전국"
            product.contentStripTag = strip_tags(product.content)
            product.save()
            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm()
    context = {
        "form": form,
    }
    return render(request, "products/form.html", context)


@require_safe
def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    cookie_value = request.COOKIES.get("hits", "_")

    if f"_{product_pk}_" not in cookie_value:  # 쿠키에 없으면
        product.hits += 1  # 조회수 증가
        product.save()

    context = {
        "product": product,
        "comments": Product_Comment.objects.select_related("user").filter(product=product, parent=None).order_by("pk"),
        "comment_form": Product_CommentForm(),
        "reply_form": Product_ReplyForm(),
    }
    response = render(request, "products/detail.html", context)

    # https://arotein.tistory.com/40 쿠키를 이용하여 조회수 기능 만들기
    if f"_{product_pk}_" not in cookie_value:
        cookie_value += f"_{product_pk}_"
        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()
        response.set_cookie("hits", value=cookie_value, max_age=max_age, httponly=True)

    return response


@login_required
@require_http_methods(["GET", "POST"])
def product_update(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if product.user != request.user:
        return redirect("products:product_detail", product_pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.is_updated = True
            product.contentStripTag = strip_tags(product.content)
            product.save()
            return redirect("products:product_detail", product_pk)
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
    }
    return render(request, "products/form.html", context)


@require_POST
def product_delete(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if product.user != request.user:
        return redirect("products:product_detail", product_pk)

    product.delete()
    return redirect("products:index")


@require_POST
def product_like(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if product.like_users.filter(pk=request.user.pk).exists():
        product.like_users.remove(request.user)
    else:
        product.like_users.add(request.user)
    # context = {
    #     "like_count": product.like_users.count(),
    # }
    # return JsonResponse(context)
    return redirect("products:product_detail", product.pk)


@require_POST
def comment_create(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    form = Product_CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.product = product
        comment.save()
    return redirect("products:product_detail", product_pk)


@require_POST
def comment_update(request, product_pk, comment_pk):
    comment = get_object_or_404(Product_Comment, pk=comment_pk)

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.user != comment.user:
        return redirect("products:product_detail", product_pk)

    form = Product_CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
    return redirect("products:product_detail", product_pk)


@require_POST
def comment_delete(request, product_pk, comment_pk):
    comment = get_object_or_404(Product_Comment, pk=comment_pk)

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.user != comment.user:
        return redirect("products:product_detail", product_pk)

    comment.delete()
    return redirect("products:product_detail", product_pk)


@require_POST
def reply_create(request, product_pk, comment_pk):
    product = get_object_or_404(Product, pk=product_pk)
    parent_comment = get_object_or_404(Product_Comment, pk=comment_pk)

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    form = Product_ReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.product = product
        reply.parent = parent_comment
        reply.save()
    return redirect("products:product_detail", product_pk)
