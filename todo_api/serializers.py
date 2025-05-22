from rest_framework import serializers
from .models import Todo
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Todo 
        fields= ["task", "timestamp", "completed", "updated", "user"]

class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']
        fields = ['id', 'email', 'username', 'password']