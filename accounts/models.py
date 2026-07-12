from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('operator', 'Operator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operator')

    def __str__(self):
        return f"{self.username} ({self.role})"
