from rest_framework import serializers
from tasks.models.task_model import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'created_at' ,'completed']
