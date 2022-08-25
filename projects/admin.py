from django.contrib import admin

from .models import Project, Review, Tag

# # Register your models here.
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ['title','full_name', 'vote_total','vote_ratio_percent']
#     search_fields = ['title']
#     list_select_related = ('owner',)

#     def vote_ratio_percent(self, obj):
#         return "{}%".format(obj.vote_ratio if obj.vote_ratio else "0")
        
#     @admin.display(ordering='-created')
#     def full_name(self, obj):
#         return obj.owner.name

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_select_related = ('owner', 'project')
    search_fields =  ['project',]
    list_filter = ['value', 'project']
    list_display = ['full_name','project', 'value']

    def full_name(self, obj):
        return obj.owner.name

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    # list_select_related = ['owner__profile']

# admin.site.register(Review, ReviewAdmin)
admin.site.register(Tag)
