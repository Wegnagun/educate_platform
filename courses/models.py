from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    """ Модель субъектов обучения. """

    title = models.CharField(max_length=200, verbose_name='Тип субъекта')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    """ Модель курсов. """

    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE,
        verbose_name='Создатель курса'
    )
    title = models.CharField(max_length=200, verbose_name='Наименование курса')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField(verbose_name='Описание курса')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    """ Модель модулей. """

    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE,
        verbose_name='Ссылка на курс'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование модуля'
    )
    description = models.TextField(blank=True, verbose_name='Описание модуля')

    def __str__(self):
        return self.title
