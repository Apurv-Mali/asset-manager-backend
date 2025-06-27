from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('delete-user/<int:user_id>/', views.DeleteUserView.as_view(), name='delete_user'),
]