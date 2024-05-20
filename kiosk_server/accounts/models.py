from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    IsDeleted = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Owners'
