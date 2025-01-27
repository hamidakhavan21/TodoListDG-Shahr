from django.urls import path
from tasks.views.task_view import TaskListCreateView, TaskDetailView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
