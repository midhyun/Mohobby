from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from .models import User
class DateInput(forms.DateInput):
    input_type = "Date"
   

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password1",
            "password2",
            "birth",
            "image",
            "address",
            "address_detail",
            "gender",
            "sports",
            "travel",
            "art",
            "food",
            "develop",
        ]
        widgets = {
            "birth": DateInput(),
        }
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = [
            "sports",
            "travel",
            "art",
            "food",
            "develop",
        ]
        widgets = {
            "birth": DateInput(),
        }