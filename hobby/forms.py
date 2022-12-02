from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Hobby, Accepted

class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = [
            'title',
            'category',
            'tags',
            'meeting_day',
            'address_type',
            'address',
            'X',
            'Y',
            'entry_fee',
            'content',
            'recruit_type',
            'limit',
            'image',
        ]

class AcceptedForm(forms.ModelForm):
    class Meta:
        model = Accepted
        fields = []