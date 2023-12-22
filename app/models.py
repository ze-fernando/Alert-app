from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=128, default="")
    tel = models.IntegerField()


class Task(models.Model):
    task = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    hourSend = models.TimeField(null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
