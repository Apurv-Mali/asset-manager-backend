from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from pnm.pagination import DefaultPagination
from core.serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User 
from .serializers import UserSerializer
from .filters import UserFilter
from django.http import HttpResponse

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            # Check if the user role is 'manager' or 'mechanic'
            if user.role in ['manager', 'mechanic']:
                user.delete()
                return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"detail": "You can only delete users with the roles 'manager' or 'mechanic'."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)  

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filterset_class = UserFilter

from django.http import JsonResponse

def create_superuser_view(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
        return JsonResponse({"status": "Superuser created"})
    else:
        return JsonResponse({"status": "Superuser already exists"})