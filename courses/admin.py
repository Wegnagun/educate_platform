from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Course, Subject, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """ Отображение субъекта в админке. """

    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created']
    list_filter = ['created', 'owner']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


admin.site.unregister(Group)
