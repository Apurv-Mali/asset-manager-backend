from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('delete-user/<int:user_id>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('create-superuser/', views.CreateSuperuserView.as_view()),
    path('check-db/', views.check_db_view),
    path('apply-migrations/', views.ApplyMigrationsView.as_view()),
]