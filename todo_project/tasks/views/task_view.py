from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from tasks.serializers.task_serializer import TaskSerializer
from tasks.services.task_service import TaskService
from tasks.models.task_model import Task
from rest_framework import status


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("due_date", OpenApiTypes.DATE, description="Filter tasks by due date"),
            OpenApiParameter("created_at", OpenApiTypes.DATE, description="Filter tasks by created date"),
            OpenApiParameter("search", OpenApiTypes.STR, description="Search tasks by title or description"),
        ]
    )
    def get_queryset(self):
        due_date = self.request.query_params.get('due_date')
        created_at = self.request.query_params.get('created_at')
        search_query = self.request.query_params.get('search')

        if due_date or created_at:
            return TaskService.filter_tasks_by_date(due_date, created_at)
        elif search_query:
            return TaskService.search_tasks(search_query)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            task = TaskService.create_task(serializer.validated_data)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self):
        task_id = self.kwargs['pk']
        return TaskService.get_task_by_id(task_id)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            updated_task = TaskService.update_task(task, serializer.validated_data)
            return Response(TaskSerializer(updated_task).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
