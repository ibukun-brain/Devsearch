from django.urls import path
from api.views import getProjects, getProject



urlpatterns = [
    path('projects/', getProjects),
    path('projects/<str:pk>/', getProject)
]
