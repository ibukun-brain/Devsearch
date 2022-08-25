from django.views.generic import (FormView, ListView,DetailView,
                                TemplateView,View,UpdateView,
                                DeleteView)
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .mixins import SkillMixin
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm
from DevSearch.utils.paginate_views import paginate


# Create your views here.
class CustomSignupView(FormView):
    template_name = 'accounts/login_signup.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users_emails = User.objects.filter(email=email)
        
        if users_emails.exists():
            messages.error(self.request, 'This email has already been used')
            return redirect('accounts:signup')

        else:
            user = form.save()
            if user is not None:
                login(self.request, user)
                return reverse_lazy('accounts:edit_account')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:edit_account')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "signup_page" 
        return context

class CustomLoginView(LoginView):
    template_name = 'accounts/login_signup.html'
    

    def form_invalid(self, form):
        messages.error(self.request, 'invalid username or password')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:account_settings')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "login_page" 
        return context
    

class ProfilesListView(ListView):
    template_name = 'accounts/profiles.html'
    model = Profile
    context_object_name = 'profiles'
    paginate_by =  6

    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = Profile.objects.exclude(profile_skill=None, bio=None, short_intro='').prefetch_related('profile_skills')
        search_query = self.request.GET.get('q')

        if search_query != '' and search_query is not None: 
            queryset = Profile.objects.filter(
                        Q(name__icontains=search_query) |
                        Q(short_intro__icontains=search_query) |
                        Q(profile_skill__name__iexact=search_query)
                        ).distinct().prefetch_related('profile_skills')

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

    
class ProfileDetailView(DetailView):
    template_name = 'accounts/user_profile.html'
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.select_related('user').get(pk=self.object.pk)
        top_skills = profile.profile_skills.exclude(description__exact="")
        other_skills = profile.profile_skills.filter(description__exact="")
        projects = profile.project_set.all().prefetch_related('tags')

        context.update({
        'profile':profile,
        'top_skills':top_skills,
        'other_skills':other_skills,
        'projects':projects,
       })
        return context

class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # profile = self.request.user.profile OR
        profile = Profile.objects.select_related('user').get(user=self.request.user)
        skills = profile.profile_skills.all()
        context["profile"] = profile
        context.update({
            'profile':profile,
            'skills':skills,
        })
        return context
    
    
class EditAccountView(LoginRequiredMixin, View):

    def get(self,request, *args, **kwargs):

        profile = self.request.user.profile
        form = ProfileForm(instance=profile)

        context = {
            'form':form
        }

        return render(request, 'accounts/profile_form.html', context)
    
    def post(self, *args, **kwargs):
        profile = self.request.user.profile
        form = ProfileForm(self.request.POST, self.request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(self.request, 'Profile succesfully updated!')
            return redirect('accounts:account_settings')

    
class AddSkillView(LoginRequiredMixin,TemplateView, FormView):
    form_class = SkillForm
    template_name = 'accounts/skills_form.html'
    success_url = reverse_lazy('accounts:account_settings')

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["page_title"] = 'Add Skill'
            return context

    def form_valid(self, form):

        user = self.request.user.profile
        skill = form.save(commit=False)
        skill.owner = user
        form.save()

        messages.success(self.request, 'Skill successfully added')
        return super(AddSkillView, self).form_valid(form)

        
class UpdateSkillView(LoginRequiredMixin,SkillMixin,UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'accounts/skills_form.html'

    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = Skill.objects.select_related('owner',)

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title':'Update Skill'
        })
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill successfully updated')
        return super().form_valid(form)
        
class DeleteSkillView(LoginRequiredMixin, SkillMixin,DeleteView):
    model = Skill
    success_url = reverse_lazy('accounts:account_settings')


    def form_valid(self, form):
        messages.success(self.request, 'Skill successfully deleted')
        return super().form_valid(form)


class InboxView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/inbox.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        message_requests = profile.recipient_message.all()
        unread_messages = message_requests.filter(is_read=False).count()
        context.update({
            'message_requests':message_requests,
            'unread_messages':unread_messages,
        })
        return context
    
class MessageView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'accounts/message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        message = profile.recipient_message.get(pk=self.object.pk)
        if message.is_read == False:
            message.is_read = True
            message.save()
        context["message"] =  message
        return context
    


class CreateMessageView(DetailView, FormView):
    template_name = 'accounts/message_form.html'
    model = Profile
    form_class = MessageForm


    def form_valid(self, form):
        try:
            sender = self.request.user.profile
        except:
            sender = None

        recipient = Profile.objects.get(pk=self.kwargs['pk'])
        message = form.save(commit=False)
        message.sender = sender
        message.recipient= recipient

        if sender:
            message.name = sender.name
            message.email = sender.email
        message.save()
        messages.success(self.request, 'Your message was sent successfully')
        return super().form_valid(form)

    def get_success_url(self):
        recipient = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy("accounts:profile_detail", kwargs={'user':recipient.user, 'pk':recipient.pk})
    