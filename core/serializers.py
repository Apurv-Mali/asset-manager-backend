# core/serializers.py
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from pnm.models import Manager, Mechanic
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    salary = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'role', 'phone', 'salary']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False, 'allow_null': True},
        }

    def validate_phone(self, value):
        """
        Ensure the phone number is unique.
        """
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already associated with another user.")
        return value

    def create(self, validated_data):
        # Extract specific fields
        role = validated_data.pop('role')
        phone = validated_data.get('phone')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        salary = validated_data.get('salary')

        # Create the user
        user = User.objects.create_user(**validated_data)
        user.role = role
        user.phone = phone
        user.first_name = first_name
        user.last_name = last_name
        user.salary = salary
        user.save()

        # Create Manager or Mechanic based on role
        full_name = f"{first_name} {last_name}"
        if role == 'manager':
            Manager.objects.create(user=user, name=full_name, phone=phone, salary=salary)
        elif role == 'mechanic':
            Mechanic.objects.create(user=user, name=full_name, phone=phone, salary=salary)

        return user


class UserSerializer(BaseUserSerializer):
    is_manager = serializers.SerializerMethodField()  # Field to check if the user is a manager
    is_mechanic = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User  # Ensure to use your custom User model
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_manager', 'is_mechanic']  # Include is_manager in fields

    def get_is_manager(self, obj):
        return hasattr(obj, 'manager')  # Check if the user has an associated Manager instance

    def get_is_mechanic(self, obj):
        return hasattr(obj, 'mechanic')  # Check if the user has an associated Manager instance
