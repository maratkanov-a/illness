from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from core.forms import UserCreateForm, NoteCreateForm
from core.models import User, Note, Diary, Survey


class HomeTemplateView(TemplateView):
    template_name = 'base.html'

# USER VIEWS ====================================


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('core:index')
    template_name_suffix = '_create'


class UserDetailView(DetailView):
    model = User
    template_name_suffix = '_detail'

    def get_object(self, queryset=None):
        self.kwargs['pk'] = self.request.user.pk
        return super(UserDetailView, self).get_object(queryset)

# ===============================================

# DIARY VIEWS ====================================


class DiaryListView(ListView):
    model = Diary


class DiaryView(View):
    def get(self, request, *args, **kwargs):
        view = DiaryDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = NoteCreateView.as_view()
        return view(request, *args, **kwargs)


class DiaryDetailView(DetailView):
    model = Diary

# ===============================================

# USER VIEWS ====================================


class SurveyListView(ListView):
    model = Survey


class SurveyDetailView(DetailView):
    model = Survey

# ===============================================


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteCreateForm
    success_url = reverse_lazy('core:index')
    template_name_suffix = '_create'
