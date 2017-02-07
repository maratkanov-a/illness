from django.views.generic import ListView

from core.models import Question


class QuestionsListView(ListView):
    model = Question
