from django.db import models

import auto_prefetch
from django.urls import reverse
from django.utils.text import slugify

from DevSearch.utils.models import TimeIDBasedModel
from DevSearch.utils.choices import Votes
from DevSearch.utils.uploads import project_image_upload_path
from accounts.models import Profile




# Create your models here.
class Project(TimeIDBasedModel):
    owner = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_query_name="profile_project")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True,null=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(upload_to=project_image_upload_path, null=True, blank=True, default='default/image-default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link =  models.CharField(max_length=2000, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']


class Review(TimeIDBasedModel):
    owner = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE, null=True)  
    project = auto_prefetch.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_reviews', related_query_name='project_review',)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=Votes.choices, default=Votes.UP)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
    

    # @property
    # def reviewers(self):
    #     reviewers = Review.objects.values_list('owner__id', flat=True)

    #     return reviewers


class Tag(TimeIDBasedModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    