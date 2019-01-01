import pytest
from django.db import DatabaseError
from todo.tests.factories import TaskFactory
from users.tests.factories import UserFactory
from datetime import datetime
from todo.helpers import (
    add_task,
    edit_task,
    delete_task,
    get_task,
    list_tasks,
)
from todo.models import Task
from pytz import utc


def test_add_task_success(three_tasks):
    user = UserFactory()
    new_description = 'test description'
    new_due_date = datetime(2018, 12, 12, tzinfo=utc)
    task4 = add_task(user=user, description=new_description, due_date=new_due_date)
    assert task4.description == new_description
    assert task4.due_date == new_due_date
    assert Task.objects.count() == 4
    for task in three_tasks:
        assert task.description != new_description
        assert task.due_date != new_due_date


def test_add_task_failed(three_tasks):
    new_description = 'test description'
    with pytest.raises(DatabaseError):
        add_task(user=None, description=new_description)
    assert Task.objects.count() == 3
    for task in three_tasks:
        assert task.description != new_description


def test_edit_task_success(three_tasks):
    task1, task2, task3 = three_tasks
    new_description = 'updated description'
    new_due_date = datetime(2018, 12, 12, tzinfo=utc)
    task3 = edit_task(task3.id, description=new_description, due_date=new_due_date)
    assert Task.objects.count() == 3
    assert task3.description == new_description
    assert task3.due_date == new_due_date
    for task in [task1, task2]:
        assert task.description != new_description
        assert task.due_date != new_due_date


def test_edit_task_failed(three_tasks):
    task1, task2, task3 = three_tasks
    new_description = 'updated description'
    with pytest.raises(DatabaseError):
        edit_task(task3.id, user=None, description=new_description)
    assert Task.objects.count() == 3
    for task in [task1, task2, task3]:
        assert task.description != new_description


def test_delete_task(three_tasks):
    task1, task2, task3 = three_tasks
    delete_task(task3.id)
    assert Task.objects.count() == 2
    assert Task.objects.filter(id=task1.id).exists()
    assert Task.objects.filter(id=task2.id).exists()
    assert not Task.objects.filter(id=task3.id).exists()


def test_staff_can_list_all_tasks(three_tasks, django_assert_num_queries):
    admin = UserFactory(is_staff=True)
    with django_assert_num_queries(1):
        tasks = list_tasks(user=admin)
        # access task.user shouldn't trigger another query because select_related('user')
        [task.user for task in tasks]
        assert len(tasks) == 3


def test_user_can_list_own_tasks(db, django_assert_num_queries):
    user1, user2 = UserFactory.create_batch(size=2)
    TaskFactory.create_batch(size=2, user=user1)
    TaskFactory.create_batch(size=3, user=user2)
    with django_assert_num_queries(1):
        tasks = list_tasks(user=user1)
        # access task.user shouldn't trigger another query because select_related('user')
        [task.user for task in tasks]
        assert len(tasks) == 2
    with django_assert_num_queries(1):
        tasks = list_tasks(user=user2)
        # access task.user shouldn't trigger another query because select_related('user')
        [task.user for task in tasks]
        assert len(tasks) == 3


def test_search_task_by_description(db, django_assert_num_queries):
    TaskFactory(description='apple1')
    TaskFactory(description='apple2')
    TaskFactory(description='pie')
    TaskFactory(description='cookie')
    with django_assert_num_queries(1):
        tasks = list_tasks(search_term='apple')
        # access task.user shouldn't trigger another query because select_related('user')
        [task.user for task in tasks]
        assert len(tasks) == 2


def test_get_task(three_tasks, django_assert_num_queries):
    task1, task2, task3 = three_tasks
    with django_assert_num_queries(1):
        task = get_task(task3.id)
        # access task.user shouldn't trigger another query because select_related('user')
        task.user


def test_get_task_no_found(three_tasks, django_assert_num_queries):
    with django_assert_num_queries(1):
        task = get_task(99)
        assert task is None
