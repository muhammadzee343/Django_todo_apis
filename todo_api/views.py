from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

authentication_classes = [JWTAuthentication]
permission_classes = [IsAuthenticated, IsOwner]

# Create your views here.
class TodoListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)

        custom_data = {
            'count': todos.count(),
            'results': serializer.data,
            'message': "List of todo items retrieved successfully."
        }
        return Response(custom_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data={
            'task': request.data.get('task'),
            'complated': request.data.get('complated'),
            'user': request.user.id
        }

        serializer = TodoSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoDetailApiView(APIView):
    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            return None
        
    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        data={
            'task': request.data.get('task'),
            'complated': request.data.get('complated'),
            'user': request.user.id
        }
        serialize = TodoSerializer(instance=todo_instance, data=data, partial=True)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        todo_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)

