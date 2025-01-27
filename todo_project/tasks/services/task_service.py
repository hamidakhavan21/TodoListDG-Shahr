from tasks.models.task_model import Task
from rest_framework.exceptions import NotFound
from django.db.models import Q


class TaskService:
    @staticmethod
    def get_all_tasks():
        return Task.objects.all()

    @staticmethod
    def create_task(data):
        return Task.objects.create(**data)

    @staticmethod
    def get_task_by_id(task_id):
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound({"error": "Task not found"})

    @staticmethod
    def update_task(task, data):
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return task

    @staticmethod
    def delete_task(task):
        task.delete()

    @staticmethod
    def filter_tasks_by_date(due_date=None, created_at=None):
        query = Q()
        if due_date:
            query &= Q(due_date__date=due_date)
        if created_at:
            query &= Q(created_at__date=created_at)
        return Task.objects.filter(query)    
    
    @staticmethod
    def search_tasks(query):
        return Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
    )