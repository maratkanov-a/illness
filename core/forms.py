from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.models import User, Note


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ['is_doctor', 'mass_index']


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['user']
