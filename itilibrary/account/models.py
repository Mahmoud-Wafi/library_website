from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    def __str__(self):
        return self.user.username
    
    
