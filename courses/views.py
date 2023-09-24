from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .mixins import OwnerCourseEditMixin, OwnerCourseMixin
from .models import Course


class ManageCourseListView(ListView):
    """ Контролер списка пользователем созданных курсов. """
    model = Course
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """ Контроллер создания нового курса. """
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """ Контроллер редактирования курса. """
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """ Контроллер удаления курса. """
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'
