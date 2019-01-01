import pytest
from django.urls import reverse
from rest_framework import status
from users.tests.factories import UserFactory
from todo.tests.factories import TaskFactory


@pytest.fixture()
def test_data(db):
    admin = UserFactory(is_staff=True)
    user1 = UserFactory()
    user2 = UserFactory()
    user1_task1 = TaskFactory(user=user1)
    user1_task2 = TaskFactory(user=user1)
    user2_task1 = TaskFactory(user=user2)
    user2_task2 = TaskFactory(user=user2)

    return {
        'admin': admin,
        'user1': user1,
        'user2': user2,
        'user1_task1': user1_task1,
        'user1_task2': user1_task2,
        'user2_task1': user2_task1,
        'user2_task2': user2_task2,
    }


def test_list_tasks(test_data, client):
    admin = test_data['admin']
    user1 = test_data['user1']
    user2 = test_data['user2']
    user1_task1 = test_data['user1_task1']
    user1_task2 = test_data['user1_task2']
    user2_task1 = test_data['user2_task1']
    user2_task2 = test_data['user2_task2']

    client.login(username=admin.email, password='password')
    resp = client.get(reverse('task_list'))
    assert resp.status_code == status.HTTP_200_OK
    task_ids = [item['id'] for item in resp.json()]
    assert user1_task1.id in task_ids
    assert user1_task2.id in task_ids
    assert user2_task1.id in task_ids
    assert user2_task2.id in task_ids

    client.login(username=user1.email, password='password')
    resp = client.get(reverse('task_list'))
    assert resp.status_code == status.HTTP_200_OK
    task_ids = [item['id'] for item in resp.json()]
    assert user1_task1.id in task_ids
    assert user1_task2.id in task_ids
    assert user2_task1.id not in task_ids
    assert user2_task2.id not in task_ids

    client.login(username=user2.email, password='password')
    resp = client.get(reverse('task_list'))
    assert resp.status_code == status.HTTP_200_OK
    task_ids = [item['id'] for item in resp.json()]
    assert user1_task1.id not in task_ids
    assert user1_task2.id not in task_ids
    assert user2_task1.id in task_ids
    assert user2_task2.id in task_ids

    client.logout()
    resp = client.get(reverse('task_list'))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_task(test_data, client):
    admin = test_data['admin']
    user1 = test_data['user1']
    user2 = test_data['user2']
    user1_task = test_data['user1_task1']
    user2_task = test_data['user2_task1']

    client.login(username=admin.email, password='password')
    resp = client.get(reverse('task_detail', kwargs={'task_id': user1_task.id}))
    assert resp.status_code == status.HTTP_200_OK
    resp = client.get(reverse('task_detail', kwargs={'task_id': user2_task.id}))
    assert resp.status_code == status.HTTP_200_OK

    client.login(username=user1.email, password='password')
    resp = client.get(reverse('task_detail', kwargs={'task_id': user1_task.id}))
    assert resp.status_code == status.HTTP_200_OK
    resp = client.get(reverse('task_detail', kwargs={'task_id': user2_task.id}))
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    client.login(username=user2.email, password='password')
    resp = client.get(reverse('task_detail', kwargs={'task_id': user1_task.id}))
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    resp = client.get(reverse('task_detail', kwargs={'task_id': user2_task.id}))
    assert resp.status_code == status.HTTP_200_OK

    client.logout()
    resp = client.get(reverse('task_detail', kwargs={'task_id': user1_task.id}))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    resp = client.get(reverse('task_detail', kwargs={'task_id': user2_task.id}))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_task(test_data, client):
    user1 = test_data['user1']
    user2 = test_data['user2']

    client.login(username=user1.email, password='password')
    resp = client.post(reverse('task_list'), data={'description': 'test description'})
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()['user']['id'] == user1.id

    client.login(username=user2.email, password='password')
    resp = client.post(reverse('task_list'), data={'description': 'test description'})
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()['user']['id'] == user2.id

    client.logout()
    resp = client.post(reverse('task_list'), data={'description': 'test description'})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_edit_task_by_admin(test_data, client):
    admin = test_data['admin']
    user1_task = test_data['user1_task1']
    user2_task = test_data['user2_task1']

    client.login(username=admin.email, password='password')
    resp = client.post(reverse('task_detail', kwargs={'task_id': user1_task.id}), data={'description': 'updated'})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['description'] == 'updated'
    resp = client.post(reverse('task_detail', kwargs={'task_id': user2_task.id}), data={'description': 'updated'})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['description'] == 'updated'


def test_edit_task_by_user1(test_data, client):
    user1 = test_data['user1']
    user2 = test_data['user2']
    user1_task = test_data['user1_task1']
    user2_task = test_data['user2_task1']

    client.login(username=user1.email, password='password')
    resp = client.post(reverse('task_detail', kwargs={'task_id': user1_task.id}), data={'description': 'updated'})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['description'] == 'updated'
    resp = client.post(reverse('task_detail', kwargs={'task_id': user2_task.id}), data={'description': 'updated'})
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    client.login(username=user2.email, password='password')
    resp = client.post(reverse('task_detail', kwargs={'task_id': user1_task.id}), data={'description': 'updated'})
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    resp = client.post(reverse('task_detail', kwargs={'task_id': user2_task.id}), data={'description': 'updated'})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['description'] == 'updated'


def test_edit_task_unauthorized(test_data, client):
    user1_task = test_data['user1_task1']
    user2_task = test_data['user2_task1']

    resp = client.post(reverse('task_detail', kwargs={'task_id': user1_task.id}), data={'description': 'updated4'})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    resp = client.post(reverse('task_detail', kwargs={'task_id': user2_task.id}), data={'description': 'updated4'})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_task_by_admin(test_data, client):
    admin = test_data['admin']
    user1_task = test_data['user1_task1']
    user2_task = test_data['user2_task1']

    client.login(username=admin.email, password='password')
    resp = client.delete(reverse('task_detail', kwargs={'task_id': user1_task.id}))
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    client.login(username=admin.email, password='password')
    resp = client.delete(reverse('task_detail', kwargs={'task_id': user2_task.id}))
    assert resp.status_code == status.HTTP_204_NO_CONTENT


def test_delete_task_by_user(test_data, client):
    user1 = test_data['user1']
    user1_task = test_data['user1_task1']
    user2_task = test_data['user2_task1']

    client.login(username=user1.email, password='password')
    resp = client.delete(reverse('task_detail', kwargs={'task_id': user1_task.id}))
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    client.login(username=user1.email, password='password')
    resp = client.delete(reverse('task_detail', kwargs={'task_id': user2_task.id}))
    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_delete_task_unauthorized(test_data, client):
    user1_task = test_data['user1_task1']
    user2_task = test_data['user2_task1']

    resp = client.delete(reverse('task_detail', kwargs={'task_id': user1_task.id}))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    resp = client.delete(reverse('task_detail', kwargs={'task_id': user2_task.id}))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
