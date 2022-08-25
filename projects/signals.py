from operator import imod
from django.utils.text import slugify
from .models import Project, Review
from django.db.models.signals import pre_save, post_save, post_delete,pre_delete
from DevSearch.utils.choices import Votes
from django.dispatch import receiver
import random

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Project.objects.filter(slug=slug).order_by('pk')
    exists = qs.exists()
    if exists:
        random_number = random.randrange(1, 1000000)
        new_slug = "%s-%s" %(slug, random)
        return create_slug(instance, new_slug=new_slug)

    return slug

@receiver(pre_save, sender=Project)
def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


# Using Review Model
@receiver(post_save, sender=Review)
def count_vote_count(instance, created, *args, **kwargs):

    if created:
        reviews = Review.objects.select_related('project','owner').filter(project__title=instance.project.title)
        review_upvotes = reviews.filter(value=Votes.UP).count()
        total_review_vote = reviews.count()
        vote_ratio_percent = (review_upvotes / total_review_vote) * 100
        
        project = Project.objects.get(pk=instance.project.pk)
        project.vote_total = total_review_vote
        project.vote_ratio = vote_ratio_percent
        project.save()
      


@receiver(post_save, sender=Review)
def update_vote_count(instance, created, *args, **kwargs):
    if created == False:
        reviews = Review.objects.select_related('project','owner').filter(project__title=instance.project.title)
        review_upvotes = reviews.filter(value=Votes.UP).count()
        total_review_vote = reviews.count()
        vote_ratio_percent = (review_upvotes / total_review_vote) * 100
        
        project = Project.objects.get(pk=instance.project.pk)
        project.vote_total = total_review_vote
        project.vote_ratio = vote_ratio_percent
        project.save()
       


@receiver(post_delete, sender=Review)
def delete_review(sender,instance,**kwargs):
    print('hello')
    print(sender)
    print(instance)
    print(kwargs)
    # review.delete()
    reviews = Review.objects.select_related('project','owner').filter(project__title=instance.project.title)
    review_upvotes = reviews.filter(value=Votes.UP).count()
    print(review_upvotes)
    total_review_vote = reviews.count()
    if total_review_vote <= 0:
        vote_ratio_percent = 0
    else:
        vote_ratio_percent = (review_upvotes / total_review_vote) * 100
    
    project = Project.objects.get(pk=instance.project.pk)
    project.vote_total = total_review_vote
    project.vote_ratio = vote_ratio_percent
    project.save()



# # Using Project Model
# @receiver(post_save, sender=Project)
# def update_vote_count(sender, instance, *args, **kwargs):
    
#     def get_vote_total(self):
#         projects = Project.objects.prefetch_related('project_reviews')

#         for project in projects:
#             total_vote_count = project.project_reviews.select_related('project', 'owner').count()

#         total_vote_count = self.project_reviews.all().count()
#         # self.vote_total = total_vote_count
#         # self.save()
#         return total_vote_count

  
#     def get_vote_ratio(self):
#         reviews = self.project_reviews.all()

#         upVote = reviews.filter(value=Votes.UP).count()
#         vote_total = reviews.count()
#         vote_ratio_percent = 0
#         if upVote != 0:
#             vote_ratio_percent = (upVote / vote_total) * 100  

        # self.vote_ratio = vote_ratio_percent
        # self.save()

        # return vote_ratio_percent     