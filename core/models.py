from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    text = models.TextField(max_length=50)
