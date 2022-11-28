from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User
class DateInput(forms.DateInput):
    input_type = "Date"

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "profile_pic",
            "birth",
            "address",
            "address_detail",
            "gender",
        ]
        widgets = {
            "birth": DateInput(),
        }