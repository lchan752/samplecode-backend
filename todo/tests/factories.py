import factory
from factory.fuzzy import FuzzyText
from todo.models import Task
from users.tests.factories import UserFactory


class TaskFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    description = FuzzyText()

    class Meta:
        model = Task
