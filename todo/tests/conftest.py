from pytest import fixture
from todo.tests.factories import TaskFactory


@fixture(scope='function')
def three_tasks(db):
    tasks = TaskFactory.create_batch(size=3)
    return tasks
