from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import Textarea

from core.models import User, Note, SurveyResult


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ['is_doctor', 'mass_index']


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'class': 'materialize-textarea'}),
        }


class SurveyResultCreateForm(forms.ModelForm):
    class Meta:
        model = SurveyResult
        exclude = '__all__'
