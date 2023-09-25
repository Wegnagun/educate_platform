from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.forms.models import modelform_factory
from django.apps import apps

from .forms import ModuleFormSet
from .mixins import OwnerCourseEditMixin, OwnerCourseMixin
from .models import Course, Content, Module


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


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """ Контроллер добавление, изменения, удаления модулей курса. """
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """ Контроллер добавление, изменения модулей курса. """
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    @staticmethod
    def get_model(model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    @staticmethod
    def get_form(model, *args, **kwargs):
        form = modelform_factory(
            model,
            exclude=[
                'owner',
                'order',
                'created',
                'updated'
            ]
        )
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model,
                id=id,
                owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    """ Контроллер удаления модулей курса. """

    @staticmethod
    def post(request, id):
        content = get_object_or_404(
            Content,
            id=id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """ Контроллер тображения всех модулей курса и уроков. """
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )

        return self.render_to_response({'module': module})
