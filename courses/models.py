from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .fields import OrderField


class Subject(models.Model):
    """ Модель субъектов обучения. """

    title = models.CharField(
        max_length=200,
        verbose_name='Наименование предмета'
    )
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

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
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

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
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """ Модель контента. """
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': (
                'text',
                'video',
                'image',
                'file'
            )
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields='module')

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    """ Абстрактная модель типа содержимого контента. """

    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    """ Модель типа содержимого контента - текст. """
    content = models.TextField()


class File(ItemBase):
    """ Модель типа содержимого контента - файл. """
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """ Модель типа содержимого контента - изображение. """
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """ Модель типа содержимого контента - видео. """
    url = models.URLField()
