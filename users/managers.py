from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not extra_fields.get('first_name'):
            raise ValueError('First Name is required')
        if not extra_fields.get('last_name'):
            raise ValueError('Last Name is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.update({'is_staff': False})
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.update({'is_superuser': True, 'is_staff': True})
        return self._create_user(email, password, **extra_fields)