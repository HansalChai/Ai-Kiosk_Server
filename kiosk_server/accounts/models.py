from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Owners'
        
class Membership(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    phone_number = models.CharField(max_length=15, null=False, unique=True)
    total_point = models.IntegerField(null=False, default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Membership'


