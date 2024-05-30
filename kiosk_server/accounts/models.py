from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    IsDeleted = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Owners'
        
class Membership(models.Model):
    ID = models.AutoField(primary_key=True, null=False)
    phone_number = models.CharField(max_length=15, null=False, unique=True)
    total_point = models.IntegerField(null=False, default=0)
    IsDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Membership'

class Order(models.Model):
    ID = models.AutoField(primary_key=True, null=False)
    Membership_ID = models.ForeignKey(Membership, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=False)
    order_num = models.IntegerField(null=False)
    order_age = models.IntegerField(null=False)
    package = models.BooleanField()
    IsDeleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Order'
