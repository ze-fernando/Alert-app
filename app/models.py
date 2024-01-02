from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128, default="", unique=True)
    tel = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
class Task(models.Model):
    SEND_CHOICES = (
        ('email', 'email'),
        ('phone', 'phone')
    )    
    task = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.now())
    hourSend = models.TimeField(null=True)
    sendFor = models.CharField(choices=SEND_CHOICES, max_length = 5, default='email')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
