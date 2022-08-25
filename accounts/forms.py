from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        
        labels = {
            'first_name':'Name'
        }

    
    def __init__(self, *args, **kwargs):

        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'email','username','location','short_intro', 
        'bio','profile_image','social_github', 'social_linkedin',
        'social_twitter','social_youtube','portfolio'
        ]

    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})


class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ['name', 'description']


    def __init__(self, *args, **kwargs):

        super(SkillForm, self).__init__(*args, **kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['name','email', 'subject','body']

        
    def __init__(self, *args, **kwargs):

        super(MessageForm, self).__init__(*args, **kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})