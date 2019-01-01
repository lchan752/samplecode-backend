from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from todo.permissions import IsStaffOrTaskOwner
from todo.helpers import (
    add_task,
    edit_task,
    delete_task,
    get_task,
    list_tasks,
)
from todo.serializers import TaskSchema


class TaskListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search_term = self.request.query_params.get('q', None)
        tasks = list_tasks(search_term=search_term, user=self.request.user)
        ser = TaskSchema()
        return Response(ser.dump(tasks, many=True).data)

    def post(self, request, *args, **kwargs):
        ser = TaskSchema()
        results = ser.load(request.data)
        if results.errors:
            return Response(results.errors, status=status.HTTP_400_BAD_REQUEST)
        task = add_task(user=self.request.user, **results.data)
        return Response(ser.dump(task).data, status=status.HTTP_201_CREATED)


class TaskRetrieveUpdateDestroy(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrTaskOwner]

    def get_task_id(self):
        return self.kwargs['task_id']

    def get(self, request, *args, **kwargs):
        task = get_task(task_id=self.get_task_id())
        ser = TaskSchema()
        return Response(ser.dump(task).data)

    def post(self, request, *args, **kwargs):
        ser = TaskSchema(partial=True)
        results = ser.load(request.data)
        if results.errors:
            return Response(results.errors, status=status.HTTP_400_BAD_REQUEST)
        task = edit_task(task_id=self.get_task_id(), **results.data)
        return Response(ser.dump(task).data)

    def delete(self, request, *args, **kwargs):
        task_id = self.get_task_id()
        delete_task(task_id=task_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
