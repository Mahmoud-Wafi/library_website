from django.db import models
from datetime import datetime
from account.models import Students
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biographie'),
        ('history', 'History'),
        ]
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    photo = models.ImageField(upload_to='photos/')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)
    
    
    def __str__(self):
        return self.name
    


class Borrow(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.student.user.username + " borrow " + self.book.name
    

    