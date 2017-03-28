# coding=utf-8
from __future__ import unicode_literals

import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models


class User(AbstractBaseUser):
    first_name = models.CharField(verbose_name=u'Имя', max_length=30, blank=True)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=30, blank=True)
    second_name = models.CharField(verbose_name=u'Отчество', max_length=200, default=u'')

    email = models.EmailField(verbose_name=u'Email', blank=True, unique=True)

    height = models.IntegerField(verbose_name=u'Рост', default=0)
    weight = models.IntegerField(verbose_name=u'Вес, кг', default=0)
    birth_date = models.DateField(default=datetime.datetime.now, verbose_name=u'Дата рождения')
    mass_index = models.FloatField(default=0.0, verbose_name=u'Рассчет индекса массы')
    waist_circumference = models.FloatField(verbose_name=u'Оркужность талии', default=0.0)
    is_doctor = models.BooleanField(verbose_name=u'Является врачом', default=False)
    city = models.CharField(verbose_name=u'Город', default='', max_length=100)

    USERNAME_FIELD = 'email'
    objects = UserManager()


class Answer(models.Model):
    text = models.CharField(max_length=200, verbose_name=u'Текст ответа')
    index = models.IntegerField(default=0, verbose_name=u'Величина')


class Question(models.Model):
    text = models.TextField(max_length=50, verbose_name=u'Текст вопроса')
    answer = models.ManyToManyField(to=Answer, verbose_name=u'Ответ')


class Survey(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Название опроса', default=u'')
    user = models.ForeignKey(to=User, verbose_name=u'Пользователь')
    questions = models.ManyToManyField(to=Question, verbose_name=u'Вопросы')


class SurveyResult(models.Model):
    user = models.ForeignKey(to=User, verbose_name=u'Пользователь')
    survey = models.ForeignKey(to=Survey, verbose_name=u'Опрос')
    result = models.ManyToManyField(to=Answer, verbose_name=u'Выбранные ответы')


class Note(models.Model):
    text = models.TextField(max_length=500, verbose_name=u'', default='Текст записи')
    date_created = models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания')


class Card(models.Model):
    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    note = models.ManyToManyField(to=Note, verbose_name=u'Запись в карте')


class Diary(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Название дневника', default=u'')
    user = models.ForeignKey(to=User, verbose_name=u'Пользователь')
    note = models.ManyToManyField(to=Note, verbose_name=u'Запись в дневнике')
