from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, FormView)
from django.contrib import messages
from .mixins import ProjectMixin
from .models import Project, Review
from .forms import ProjectModelForm, ReviewForm
from DevSearch.utils.paginate_views import paginate
from DevSearch.utils.choices import Votes

# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    paginate_by = 6
    
    

    def get_queryset(self):

        queryset = super().get_queryset()
        queryset = Project.objects.all().prefetch_related('tags')
        search_query = self.request.GET.get('q')

        if search_query != '' and search_query is not None: 
            queryset = Project.objects.filter(
                        Q(title__icontains=search_query) |
                        Q(owner__name__icontains=search_query) |
                        Q(tags__name__iexact=search_query)
                        ).distinct().prefetch_related('tags')
        return queryset

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_no = 1
        num_pages = context['paginator'].num_pages

        paginate_template = paginate(page_no, num_pages)

        context.update({
            "custom_range" : paginate_template
        })
        return context
    

    

class ProjectDetailView(DetailView, FormView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'
    form_class =  ReviewForm

    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = Project.objects.prefetch_related('project_reviews').select_related('owner__user')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.select_related('owner__user', 'project').\
        values_list('owner__pk', flat=True).\
        filter(project__title=self.object.title)\
        
        context["reviews"] = reviews
        
        return context
    

    def form_valid(self, form):       
        user = self.request.user.profile
        project = Project.objects.get(slug=self.kwargs['slug'])
        review_form = form.save(commit=False)
        review_form.owner = user
        review_form.project = project
        review_form.save()

        project.get_vote_count

        messages.success(self.request, 'Your review was sucessfully submitted')
        return super().form_valid(form)

    def get_success_url(self):
        project = Project.objects.get(slug=self.kwargs['slug'])
        return reverse_lazy("projects:project_detail", kwargs={"slug": project.slug, 'owner':project.owner})

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class =  ProjectModelForm
    template_name = 'projects/project_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Create Project'
        return context

    def form_valid(self, form):
        user = self.request.user.profile
        instance = form.save(commit=False)
        instance.owner = user
        form.save()


        return super().form_valid(form)
        

    

class ProjectUpdateView(LoginRequiredMixin, ProjectMixin, UpdateView):
    model = Project
    form_class =  ProjectModelForm
    template_name = 'projects/project_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Update Project'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Project successfully updated')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, ProjectMixin,DeleteView):
    model = Project
    success_url = reverse_lazy('accounts:account_settings')


    def form_valid(self, form):
        messages.success(self.request, 'Project successfully deleted')
        return super().form_valid(form)

    
