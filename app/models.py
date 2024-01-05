from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128, default="", unique=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
class Task(models.Model):
    task = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.now())
    hourSend = models.TimeField(null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
