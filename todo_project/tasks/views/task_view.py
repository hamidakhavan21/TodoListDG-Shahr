from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.serializers.task_serializer import TaskSerializer
from tasks.services.task_service import TaskService

class TaskListCreateView(APIView):
    def get(self, request):
        due_date = request.query_params.get('due_date')
        created_at = request.query_params.get('created_at')
        search_query = request.query_params.get('search')

        if due_date or created_at:
            tasks = TaskService.filter_tasks_by_date(due_date, created_at)
        elif search_query: 
            tasks = TaskService.search_tasks(search_query)
        else:
            tasks = TaskService.get_all_tasks()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = TaskService.create_task(serializer.validated_data)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class TaskDetailView(APIView):
    def get(self, request, pk):
        task = TaskService.get_task_by_id(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = TaskService.get_task_by_id(pk)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            updated_task = TaskService.update_task(task, serializer.validated_data)
            return Response(TaskSerializer(updated_task).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = TaskService.get_task_by_id(pk)
        TaskService.delete_task(task)
        return Response(status=status.HTTP_204_NO_CONTENT)
