from django.views.generic import CreateView

from core.forms import UserCreateForm, NoteCreateForm
from core.models import User, Note


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name_suffix = '_create'


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteCreateForm
    template_name_suffix = '_create'
