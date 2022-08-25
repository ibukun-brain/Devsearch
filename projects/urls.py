from django.urls import path
from .views import ( ProjectListView, ProjectDetailView,
                     ProjectCreateView, ProjectUpdateView,
                     ProjectDeleteView )

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    # Add username to path also
    path('<str:owner>/project/<str:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('create-project/', ProjectCreateView.as_view(), name='project_create'),
    path('update-project/<str:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('delete-project/<str:pk>/', ProjectDeleteView.as_view(), name='project_delete'),

]
