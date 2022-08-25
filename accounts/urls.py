from profile import Profile
from django.urls import path
from .views import (AddSkillView, CreateMessageView, EditAccountView, InboxView, 
                    ProfilesListView, ProfileDetailView, CustomLoginView, 
                    CustomSignupView, UpdateSkillView, UserAccountView,
                    DeleteSkillView, MessageView,
                    )
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('', ProfilesListView.as_view(), name='profiles'),
    path('<str:user>/<uuid:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('accounts/signup/', CustomSignupView.as_view(), name='signup'),
    path('accounts/login/', CustomLoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    path('accounts/account-settings/', UserAccountView.as_view(), name='account_settings'),
    path('accounts/edit-account/', EditAccountView.as_view(), name='edit_account'),
    path('accounts/add-skill/', AddSkillView.as_view(), name='add_skill'),
    path('accounts/update-skill/<uuid:pk>/', UpdateSkillView.as_view(), name='update_skill'),
    path('accounts/delete-skill/<uuid:pk>/', DeleteSkillView.as_view(), name='delete_skill'),
    path('accounts/inbox/', InboxView.as_view(), name="inbox"),
    path('accounts/message/<uuid:pk>/', MessageView.as_view(), name="message"),
    path('accounts/create-message/<uuid:pk>/', CreateMessageView.as_view(), name="message_create"),
]