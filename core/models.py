# coding=utf-8
from __future__ import unicode_literals

import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

CHOICES_DEFAULT = [
    (0, 'Нет'),
    (1, 'Да')
]


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

    diary_required = models.BooleanField(editable=False, default=False)
    sex_survey_required = models.BooleanField(editable=False, default=False)

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
    volume_pis = models.IntegerField(blank=True, null=True, verbose_name='Объем выделенной мочи, мл')
    neolozh_poziv = models.BooleanField(blank=True, default=False, verbose_name='Неотложный позыв')
    podtek = models.BooleanField(blank=True, default=False, verbose_name='Подтекание')
    volume_drink = models.IntegerField(blank=True, null=True, verbose_name='Объем выпитой жидкости, мл')
    date_created = models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания')


class Card(models.Model):
    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    note = models.ManyToManyField(to=Note, verbose_name=u'Запись в карте')


class Diary(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Название дневника', default=u'')
    user = models.ForeignKey(to=User, verbose_name=u'Пользователь')
    note = models.ManyToManyField(to=Note, verbose_name=u'Запись в дневнике')


class Claim(models.Model):
    user = models.OneToOneField(User, related_name='claim')
    zatrud_moch = models.BooleanField(verbose_name='Затрудненное мочеиспускание', choices=CHOICES_DEFAULT)
    uchash_moch = models.BooleanField(verbose_name='Учащенное мочеиспускание', choices=CHOICES_DEFAULT)
    night_moch = models.BooleanField(verbose_name='Ночное мочеиспускание', choices=CHOICES_DEFAULT)
    rez_moch = models.BooleanField(verbose_name='Резь при мочеиспускании', choices=CHOICES_DEFAULT)
    low_stomach_pain = models.BooleanField(verbose_name='Боль внизу живота', choices=CHOICES_DEFAULT)
    nederzh_moch = models.BooleanField(verbose_name='Недержание мочи', choices=CHOICES_DEFAULT)
    sex_weak = models.BooleanField(verbose_name='Сексуальная дисфункция', choices=CHOICES_DEFAULT)
    mocha_blood_mixin = models.BooleanField(verbose_name='Примесь крови в моче', choices=CHOICES_DEFAULT)

    def __str__(self):
        return self.user.last_name



class Anamnez(models.Model):
    user = models.OneToOneField(User, related_name='anamnez')
    how_long = models.IntegerField(verbose_name='Сколько месяцев считаете себя больным ?')
    narost = models.BooleanField(verbose_name='Отмечаете ли Вы нарастание симптомов '
                                              'нарушения мочеиспускания в течение последних двух лет ?',
                                 choices=CHOICES_DEFAULT)
    diabet = models.BooleanField(verbose_name='Страдаете ли вы сахарным диабетом ?', choices=CHOICES_DEFAULT)
    hron_prost = models.BooleanField(verbose_name='Ставился ли Вам диагноз хронического простатита ?',
                                     choices=CHOICES_DEFAULT)
    strict_uret = models.BooleanField(verbose_name='Ставился ли Вам диагноз стриктуры уретры ?')
    pozv_taz_travm = models.BooleanField(verbose_name='Была ли у Вас травма позвоночика, органов таза ?',
                                         choices=CHOICES_DEFAULT)
    radiculit = models.BooleanField(verbose_name='Бывают ли у Вас приступы радикулита ?', choices=CHOICES_DEFAULT)
    insult = models.BooleanField(verbose_name='Был ли у Вас инсульт ?', choices=CHOICES_DEFAULT)
    bliz_rak = models.BooleanField(verbose_name='Был ли выявлен рак предстательной железы '
                                                'у Ваших близких родственников?', choices=CHOICES_DEFAULT)

    def __str__(self):
        return self.user.last_name


@receiver(pre_save, sender=Claim, dispatch_uid="check_claim")
def сheck_claim(sender, instance, update_fields, **kwargs):
    """Этот гандон хотел аналитики, мы ему дадим ее. Погнали, пидор."""
    if instance.uchash_moch or instance.night_moch or instance.nederzh_moch:
        instance.user.diary_required = True
        instance.user.save()
    if instance.sex_weak:
        instance.user.sex_survey_required = True
        instance.user.save()


class SexSurvey(models.Model):
    CHOICES_FIRST = ((1, 'Очень низкая'),
                     (2, 'Низкая'),
                     (3, 'Средняя'),
                     (4, 'Высокая'),
                     (5, 'Очень высокая'),)
    CHOICES_SECOND = ((0, 'Сексуальной активности не было'),
                      (1, 'Почти никогда или никогда'),
                      (2, 'Изредка (меньше половины случаев)'),
                      (3, 'Иногда (половина случаев)'),
                      (4, 'Часто (чаще, чем в половине случаев)'),
                      (5, 'Почти всегда или всегда'),)
    CHOICES_THIRD = ((0, 'Не пытался совершить половой акт'),
                     (1, 'Почти никогда или никогда'),
                     (2, 'Изредка (меньше половины случаев)'),
                     (3, 'Иногда (половина случаев)'),
                     (4, 'Часто (чаще, чем в половине случаев)'),
                     (5, 'Почти всегда или всегда'),)
    CHOICES_FOURTH = ((0, 'Не пытался совершить половой акт'),
                      (1, 'Чрезвычайно трудно'),
                      (2, 'Очень трудно'),
                      (3, 'Трудно'),
                      (4, 'Немного трудновато'),
                      (5, 'Нетрудно'),)

    user = models.OneToOneField(User, related_name='sex_survey')
    self_confidence = models.IntegerField(choices=CHOICES_FIRST,
                                          verbose_name='Как Вы оцениваете степень Вашей уверенности в том, '
                                                       'что Вы можете достичь и удержать эрекцию?')
    stoyak_do = models.IntegerField(choices=CHOICES_SECOND,
                                    verbose_name='Как часто Ваша эрекция достаточна для введения члена во влагалище?')
    stoyak_vo_vremya = models.IntegerField(choices=CHOICES_THIRD,
                                           verbose_name='Как часто Вам удается сохранить '
                                                        'эрекцию после введения члена во влагалище?')
    stoyak_nevalyashka = models.IntegerField(choices=CHOICES_FOURTH,
                                             verbose_name='Было ли Вам трудно сохранять '
                                                          'эрекцию до завершения полового акта?')
    orgazm = models.IntegerField(choices=CHOICES_SECOND, verbose_name='При попытках совершить '
                                                                      'половой акт часто ли Вы были удовлетворены ?')

    def __str__(self):
        return self.user.last_name
