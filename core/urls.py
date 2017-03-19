from django.conf.urls import url

from core.views import UserCreateView, NoteCreateView

urlpatterns = [
    url(r'registration/$', UserCreateView.as_view(), name="registration"),
    url(r'note/create/$', NoteCreateView.as_view(), name="note_create"),
]
