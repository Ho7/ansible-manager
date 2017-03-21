from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin

import core.forms.task_template
from core import consts

from core import models
from core.generic import mixins
from core.generic import views


class Search(mixins.PermissionRequiredMixin, mixins.FormMixin, views.ListView):
    template_name = 'core/task_template/search.html'
    form_class = core.forms.task_template.Search
    paginate_by = 20
    title = 'Search task templates'
    model = models.TaskTemplate
    permission_required = 'core.view_task_template'

    def get_breadcrumbs(self):
        return (
            ('Home', reverse('index')),
            (self.get_title(), '')
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.get_form()
        if form.is_valid():
            name = form.cleaned_data.get('name')
            hosts = form.cleaned_data.get('hosts')
            host_groups = form.cleaned_data.get('host_groups')

            if name:
                queryset = queryset.filter(name__icontains=name)

            if hosts:
                queryset = queryset.filter(hosts__in=hosts)

            if host_groups:
                queryset = queryset.filter(host_groups__in=host_groups)
        return queryset
search = Search.as_view()


class Edit(mixins.PermissionRequiredMixin, mixins.FormAndModelFormsetMixin, views.EditView):
    template_name = 'core/task_template/edit.html'
    form_class = core.forms.task_template.Edit
    model = models.TaskTemplate
    formset_model = models.Variable
    permission_required = 'core.add_task_template'
    success_url = reverse_lazy('task_template_search')
    title_create = 'Create Task Template'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_formset_initial(self):
        initial = self.formset_model.objects.none()
        obj = self.get_object()
        if obj:
            initial = self.formset_model.objects.filter(task_templates__in=[obj, ])
        return initial

    def get_breadcrumbs(self):
        return (
            ('Home', reverse('index')),
            ('Search task templates', reverse('task_template_search')),
            (self.get_title(), '')
        )

    def form_valid(self, form, formset):
        self.object = form.save()
        variables = formset.save()
        self.object.vars.add(*variables)
        return redirect(self.get_success_url())
edit = Edit.as_view()


class Delete(mixins.PermissionRequiredMixin, views.DeleteView):
    template_name = 'core/task_template/delete.html'
    model = models.TaskTemplate
    permission_required = 'core.delete_task_template'
    success_url = reverse_lazy('task_template_search')

    def get_title(self):
        obj = self.get_object()
        return "Delete %s" % obj

    def get_breadcrumbs(self):
        obj = self.get_object()
        return (
            ('Home', reverse('index')),
            ('Search task templates', reverse('task_template_search')),
            (str(obj), reverse('task_template_update', kwargs={'pk': obj.id})),
            ('Delete', '')
        )
delete = Delete.as_view()


class Run(mixins.PermissionRequiredMixin, SingleObjectMixin, views.View):
    permission_required = 'core.run_task'
    model = models.TaskTemplate

    def get(self, request, *args, **kwargs):
        task_template = self.get_object()
        task, in_progress = task_template.run_task(self.request.user)
        if in_progress:
            messages.info(self.request, 'The same task was not started. You have been redirected to a running task.')
        return redirect(reverse('task_log', kwargs={'pk': task.id}))
run = Run.as_view()
