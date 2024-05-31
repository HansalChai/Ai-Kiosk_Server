from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.category_name
