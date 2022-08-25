from django.shortcuts import redirect
from .models import Project


class ProjectMixin:

    def dispatch(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        if request.user.profile != project.owner:
            return redirect('projects:project_list')

        return super(ProjectMixin, self).dispatch(request, *args, **kwargs)