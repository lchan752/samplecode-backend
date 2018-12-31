import factory
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.lazy_attribute(lambda o: f"{o.first_name}@example.com")
    first_name = factory.Sequence(lambda n: f"User{n}")
    last_name = "Sesame"

    class Meta:
        model = User

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "password"
        self.set_password(password)
