import email
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property

from django.urls import reverse

import auto_prefetch
from DevSearch.utils.uploads import profile_image_upload_path
from DevSearch.utils.models import TimeIDBasedModel
# Create your models here.
class Profile(TimeIDBasedModel):
    user = auto_prefetch.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, unique=True, null=True, blank=True, )
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=profile_image_upload_path, default='default/user-default.png', null=True, blank=True)
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    portfolio = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['-profile_project__vote_ratio','-profile_project__vote_total','-created']
        pass
    


class Skill(TimeIDBasedModel):
    owner = auto_prefetch.ForeignKey(
            Profile, on_delete=models.CASCADE, 
            null=True, blank=True, related_name='profile_skills',
            related_query_name='profile_skill'
        )
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("accounts:account_settings")
    


class Message(TimeIDBasedModel):
    sender = auto_prefetch.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = auto_prefetch.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipient_message')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.subject
    

    class Meta:
        ordering = ['is_read', '-created']

