# coding=utf-8
import json

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.list import BaseListView

from core.forms import UserCreateForm, NoteCreateForm, SurveyResultCreateForm, UserUpdateForm
from core.models import User, Note, Diary, Survey, SurveyResult, Answer


class FilterByUser(BaseListView):
    def get_queryset(self):
        qs = super(FilterByUser, self).get_queryset().filter(user__id=self.request.user.id)
        return qs


class HomeTemplateView(TemplateView):
    template_name = 'base.html'

# USER VIEWS ====================================


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('core:index')
    template_name_suffix = '_create'

    def form_valid(self, form):
        from django.contrib.gis.geoip import GeoIP
        g = GeoIP()
        ip = self.request.META.get('REMOTE_ADDR', None)

        city = 'Moscow'
        if ip and g.city(ip):
            city = g.city(ip)['city']

        form.instance.city = city

        if form.instance.height and form.instance.weight and form.instance.waist_circumference:
            form.instance.mass_index = 12  # ЗДЕСЬ ФОРМУЛА

        return super(UserCreateView, self).form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('core:index')

    def get_object(self, queryset=None):
        self.kwargs['pk'] = self.request.user.pk
        return super(UserUpdateView, self).get_object(queryset)
# ===============================================

# DIARY VIEWS ====================================


class DiaryListView(ListView, FilterByUser):
    model = Diary


class DiaryDetailView(DetailView):
    model = Diary

    def post(self, request, *args, **kwargs):
        view = NoteCreateView.as_view()
        return view(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiaryDetailView, self).get_context_data(**kwargs)
        context.update({
            "form": NoteCreateForm
        })
        return context

# ===============================================

# USER VIEWS ====================================


class SurveyListView(ListView, FilterByUser):
    model = Survey


class SurveyDetailView(DetailView):
    model = Survey

    def post(self, request, *args, **kwargs):
        view = SurveyResultCreateView.as_view()
        return view(request, *args, **kwargs)

# ===============================================


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteCreateForm
    success_url = reverse_lazy('core:index')
    template_name_suffix = '_create'

    def form_valid(self, form):
        result = super(NoteCreateView, self).form_valid(form)
        diary_id = self.request.POST.get('diary_id', None)
        if diary_id:
            diary = Diary.objects.filter(id=diary_id).first()
            diary.note.add(self.object)
        return result


class SurveyResultCreateView(CreateView):
    model = SurveyResult
    form_class = SurveyResultCreateForm
    success_url = reverse_lazy('core:index')
    template_name_suffix = '_create'

    def post(self, request, *args, **kwargs):
        survey_id = self.request.POST.get('survey_id', None)
        answers_ids = self.request.POST.get('answers_ids', [])

        if survey_id:
            result = SurveyResult(**{
                "user": User.objects.filter(id=self.request.user.id).first(),
                "survey": Survey.objects.filter(id=survey_id).first()
            })
            result.save()
            result.result.add(*Answer.objects.filter(id__in=json.loads(answers_ids)))

        return super(SurveyResultCreateView, self).post(request, *args, **kwargs)

