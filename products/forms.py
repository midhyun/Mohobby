from django import forms
from .models import Product, Product_Comment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "price",
            "productType",
            "tradeType",
            "location",
            "image",
            "content",
        ]
        labels = {
            "title": "제목",
            "price": "판매 가격",
            "productType": "상품 상태",
            "tradeType": "배송 방법",
            "location": "거래 위치",
            "image": "이미지",
            "content": "",
        }


class Product_CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "댓글을 남겨보세요 💬",
            }
        ),
    )

    class Meta:
        model = Product_Comment
        fields = [
            "content",
        ]


class Product_ReplyForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "대댓글을 남겨보세요 💬",
            }
        ),
    )

    class Meta:
        model = Product_Comment
        fields = [
            "content",
        ]
