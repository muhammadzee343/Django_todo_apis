from django.urls import path
from .views import TodoListApiView

urlpatterns = [
    path("api", TodoListApiView.as_view()),
    path("api/<int:todo_id>/", TodoListApiView.as_view())
]