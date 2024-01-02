from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128, default="", unique=True)
    tel = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
class Task(models.Model):
    task = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    hourSend = models.TimeField(null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
