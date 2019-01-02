from unittest.mock import patch, create_autospec
from rest_framework import status
from marshmallow import UnmarshalResult
from todo.serializers import TaskSchema
from todo.views import (
    TaskListCreate,
    TaskRetrieveUpdateDestroy,
)
from todo.tests.factories import TaskFactory


def test_task_retrieve(db, rf):
    task = TaskFactory()
    serializer_instance = create_autospec(TaskSchema)
    serializer_instance.dump.return_value.data = {"id": task.id}
    patch_get_task = patch('todo.views.get_task', return_value=task, autospec=True)
    patch_task_schema = patch('todo.views.TaskSchema', return_value=serializer_instance, autospec=True)
    request = rf.get("/some/path")
    request.user = task.user

    with patch_get_task as mock_get_task, patch_task_schema:
        view = TaskRetrieveUpdateDestroy.as_view()
        resp = view(request, task_id=task.id)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['id'] == task.id
        mock_get_task.assert_called_once_with(task_id=task.id)
        serializer_instance.dump.assert_called_once_with(task)


def test_task_update(db, rf):
    task = TaskFactory()
    post_data = {'description': 'updated description'}
    request = rf.post("/some/path", post_data)
    request.user = task.user
    request._dont_enforce_csrf_checks = True

    serializer_instance = create_autospec(TaskSchema)
    serializer_instance.dump.return_value.data = {"id": task.id}
    serializer_unmarshal = create_autospec(UnmarshalResult)
    serializer_unmarshal.data = post_data
    serializer_unmarshal.errors = {}
    serializer_instance.load.return_value = serializer_unmarshal
    patch_edit_task = patch('todo.views.edit_task', return_value=task, autospec=True)
    patch_task_schema = patch('todo.views.TaskSchema', return_value=serializer_instance, autospec=True)

    with patch_edit_task as mock_edit_task, patch_task_schema:
        view = TaskRetrieveUpdateDestroy.as_view()
        resp = view(request, task_id=task.id)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['id'] == task.id
        mock_edit_task.assert_called_once_with(task_id=task.id, **post_data)
        serializer_instance.load.assert_called_once()
        assert serializer_instance.load.call_args[0][0].dict() == post_data
        serializer_instance.dump.assert_called_once_with(task)


def test_task_delete(db, rf):
    task = TaskFactory()
    request = rf.delete("/some/path")
    request.user = task.user
    request._dont_enforce_csrf_checks = True
    patch_delete_task = patch('todo.views.delete_task', autospec=True)

    with patch_delete_task as mock_delete_task:
        view = TaskRetrieveUpdateDestroy.as_view()
        resp = view(request, task_id=task.id)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        mock_delete_task.assert_called_once_with(task_id=task.id)


def test_task_list(db, rf):
    task = TaskFactory()
    serializer_instance = create_autospec(TaskSchema)
    serializer_instance.dump.return_value.data = [{"id": task.id}]
    patch_list_tasks = patch('todo.views.list_tasks', return_value=[task], autospec=True)
    patch_task_schema = patch('todo.views.TaskSchema', return_value=serializer_instance, autospec=True)
    request = rf.get("/some/path", {'q': 'querystring'})
    request.user = task.user

    with patch_list_tasks as mock_list_tasks, patch_task_schema:
        view = TaskListCreate.as_view()
        resp = view(request)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == [{"id": task.id}]
        mock_list_tasks.assert_called_once_with(search_term='querystring', user=task.user)
        serializer_instance.dump.assert_called_once_with([task], many=True)


def test_task_create(db, rf):
    task = TaskFactory()
    post_data = {'description': 'task description'}
    serializer_instance = create_autospec(TaskSchema)
    serializer_instance.dump.return_value.data = {"id": task.id}
    serializer_unmarshal = create_autospec(UnmarshalResult)
    serializer_unmarshal.data = post_data
    serializer_unmarshal.errors = {}
    serializer_instance.load.return_value = serializer_unmarshal
    patch_add_task = patch('todo.views.add_task', return_value=task, autospec=True)
    patch_task_schema = patch('todo.views.TaskSchema', return_value=serializer_instance, autospec=True)
    request = rf.post("/some/path", post_data)
    request.user = task.user
    request._dont_enforce_csrf_checks = True

    with patch_add_task as mock_add_task, patch_task_schema:
        view = TaskListCreate.as_view()
        resp = view(request)
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data == {"id": task.id}
        mock_add_task.assert_called_once_with(user=task.user, **post_data)
        serializer_instance.load.assert_called_once()
        assert serializer_instance.load.call_args[0][0].dict() == post_data
        serializer_instance.dump.assert_called_once_with(task)