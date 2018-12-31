from rest_framework.permissions import BasePermission
from todo.models import Task


class IsStaffOrTaskOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        task_id = view.get_task_id()
        is_task_owner = Task.objects.filter(id=task_id, user=request.user).exists()
        return is_task_owner
