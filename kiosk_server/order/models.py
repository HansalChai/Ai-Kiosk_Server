from django.db import models
from accounts.models import Membership, CustomUser
from django.utils import timezone

# 아래는 카테고리, 옵션, 옵션 선택지 모델
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Category'

class Options(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    option_name = models.CharField(max_length=30, null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Options'
    

class OptionChoice(models.Model):
    id = models.AutoField(primary_key=True)
    option_id = models.ForeignKey(Options, related_name='choices', on_delete=models.CASCADE)
    choice_name = models.CharField(max_length=100)
    extra_cost = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Option_choice'

class Menu(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False)
    image = models.ImageField(upload_to='menu/', null=True)
    price = models.IntegerField(null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Menu'
    
class Order(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    membership_id = models.ForeignKey(Membership, on_delete=models.CASCADE, null=True)
    total_price = models.IntegerField(null=False)
    order_num = models.IntegerField(null=False)
    order_age = models.CharField(max_length=10)
    package = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Order'

class Order_amount(models.Model):
    order_amount_id = models.AutoField(primary_key=True, null=False)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    teenager = models.IntegerField(default=0) # 0-2, 4-6, 8-12
    adult = models.IntegerField(default=0) # 15-20, 25-32
    elder = models.IntegerField(default=0) # 38-43, 48-53
    aged = models.IntegerField(default=0) # 60-100
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Order_amount'
    
class Order_menu(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    count = models.IntegerField(null=False)
    
    class Meta:
        db_table = 'Order_menu'

class Order_choice_order_menu(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    order_menu_id = models.ForeignKey(Order_menu, on_delete=models.CASCADE)
    option_choice_id = models.ForeignKey(OptionChoice, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Order_choice_order_menu'