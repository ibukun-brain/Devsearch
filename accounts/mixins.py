from django.shortcuts import redirect
from .models import Skill


class SkillMixin:

    def dispatch(self, request, *args, **kwargs):
        skill = Skill.objects.get(pk=kwargs['pk'])
        if request.user.profile != skill.owner:
            return redirect('projects:project_list')

        return super(SkillMixin, self).dispatch(request, *args, **kwargs)