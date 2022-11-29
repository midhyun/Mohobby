from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Hobby

class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = [
            'title',
            'category',
            'meeting_day',
            'address',
            'X',
            'Y',
            'entry_fee',
            'content',
            'recruit_type',
            'limit',
            'image',
        ]