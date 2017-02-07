from django.conf.urls import url

from core.views import QuestionsListView

urlpatterns = [
    url(r'show_question/$', QuestionsListView.as_view(), name="index"),
]
