from todo.serializers import TaskSchema
from datetime import datetime
from pytz import utc


def test_dump(three_tasks):
    task1, task2, task3 = three_tasks
    ser = TaskSchema()
    data = ser.dump(task1).data
    assert data['id'] == task1.id
    assert data['user']['id'] == task1.user.id
    assert data['description'] == task1.description
    assert data['due_date'] == task1.due_date


def test_load():
    description = 'test description'
    due_date = datetime(2018, 12, 13, tzinfo=utc)
    data = {
        'description': description,
        'due_date': due_date.isoformat()
    }
    ser = TaskSchema()
    results = ser.load(data)
    assert not results.errors
    assert results.data['description'] == description
    assert results.data['due_date'] == due_date


def test_description_is_required():
    ser = TaskSchema()
    results = ser.load({})
    assert 'description' in results.errors


def test_description_min_length():
    ser = TaskSchema()
    results = ser.load({'description': ''})
    assert 'description' in results.errors


def test_due_date_is_not_required():
    ser = TaskSchema()
    results = ser.load({'description': 'test description'})
    assert not results.errors
    results = ser.load({'description': 'test description', 'due_date': None})
    assert not results.errors
