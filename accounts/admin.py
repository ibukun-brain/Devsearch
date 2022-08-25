from django.contrib import admin
from .models import Message, Profile, Skill


# Register your models here.
class SkillInline(admin.StackedInline):
    model = Skill
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    inlines = [SkillInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_select_related = True
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill)
