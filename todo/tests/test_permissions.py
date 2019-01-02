from unittest.mock import create_autospec
from rest_framework.permissions import IsAuthenticated
from todo.views import (
    TaskRetrieveUpdateDestroy,
    TaskListCreate,
)
from todo.permissions import IsStaffOrTaskOwner
from users.tests.factories import UserFactory
from todo.tests.factories import TaskFactory


def mock_view(task_id):
    view = create_autospec(spec=TaskRetrieveUpdateDestroy)
    view.get_task_id.return_value = task_id
    return view


def test_is_staff_or_task_owner_permission_for_staff(db, rf):
    admin = UserFactory(is_staff=True)
    user1_task = TaskFactory()
    user2_task = TaskFactory()
    request = rf.get('/some/path')
    request.user = admin
    perm = IsStaffOrTaskOwner()
    assert perm.has_permission(request, mock_view(user1_task.id))
    assert perm.has_permission(request, mock_view(user2_task.id))


def test_is_staff_or_task_owner_permission_for_task_owner(db, rf):
    user1_task = TaskFactory()
    user2_task = TaskFactory()
    request = rf.get('/some/path')
    request.user = user1_task.user
    perm = IsStaffOrTaskOwner()
    assert perm.has_permission(request, mock_view(user1_task.id))
    assert not perm.has_permission(request, mock_view(user2_task.id))


def test_is_staff_or_task_owner_permission_for_non_task_owner(db, rf):
    user1_task = TaskFactory()
    user2_task = TaskFactory()
    request = rf.get('/some/path')
    request.user = UserFactory()
    perm = IsStaffOrTaskOwner()
    assert not perm.has_permission(request, mock_view(user1_task.id))
    assert not perm.has_permission(request, mock_view(user2_task.id))


def test_view_permissions():
    assert IsStaffOrTaskOwner in TaskRetrieveUpdateDestroy.permission_classes
    assert IsAuthenticated in TaskRetrieveUpdateDestroy.permission_classes
    assert IsAuthenticated in TaskListCreate.permission_classes
