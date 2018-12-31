from django.db import transaction
from todo.models import Task


def add_task(user=None, **kwargs):
    with transaction.atomic():
        task = Task.objects.create(user=user, **kwargs)
    # send websocket message
    return task


def edit_task(task_id, **kwargs):
    with transaction.atomic():
        Task.objects.filter(id=task_id).update(**kwargs)
    # send websocket message
    task = get_task(task_id)
    return task


def delete_task(task_id):
    with transaction.atomic():
        Task.objects.filter(id=task_id).delete()
    # send websocket message


def get_task(task_id):
    qry = list_tasks()
    return qry.filter(id=task_id).first()


def list_tasks(search_term=None, user=None):
    qry = Task.objects.select_related('user')
    if user and not user.is_staff:
        qry = qry.filter(user=user)
    if search_term:
        qry = qry.filter(description__icontains=search_term)
    return qry
