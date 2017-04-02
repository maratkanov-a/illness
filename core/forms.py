from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import Textarea

from core.models import User, Note, SurveyResult


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'second_name', 'last_name', 'weight', 'height', 'birth_date', 'waist_circumference', 'city']


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['volume_pis', 'neolozh_poziv', 'podtek', 'volume_drink']
        widgets = {
            'volume_pis': Textarea(attrs={'class': 'materialize-textarea'}),
            'neolozh_poziv': Textarea(attrs={'class': 'materialize-textarea'}),
            'podtek': Textarea(attrs={'class': 'materialize-textarea'}),
            'volume_drink': Textarea(attrs={'class': 'materialize-textarea'}),
        }


class SurveyResultCreateForm(forms.ModelForm):
    class Meta:
        model = SurveyResult
        exclude = '__all__'
