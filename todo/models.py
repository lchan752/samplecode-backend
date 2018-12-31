from django.db import models
from users.models import User


class Task(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    due_date = models.DateTimeField(blank=True, null=True)
