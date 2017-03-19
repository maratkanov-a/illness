from django.conf.urls import url

from core.views import UserCreateView, NoteCreateView, HomeTemplateView, DiaryListView, UserDetailView, \
    SurveyListView, SurveyDetailView, DiaryDetailView

urlpatterns = [
    url(r'^$', HomeTemplateView.as_view(), name="index"),

    url(r'profile/$', UserDetailView.as_view(), name="profile"),

    url(r'survey/$', SurveyListView.as_view(), name="survey"),
    url(r'survey/(?P<pk>\d+)/detail/$', SurveyDetailView.as_view(), name="survey_detail"),

    url(r'diaries/$', DiaryListView.as_view(), name="diaries"),
    url(r'diaries/(?P<pk>\d+)/detail/$', DiaryDetailView.as_view(), name="diary_detail"),

    url(r'registration/$', UserCreateView.as_view(), name="registration"),
    url(r'note/create/$', NoteCreateView.as_view(), name="note_create"),
]
