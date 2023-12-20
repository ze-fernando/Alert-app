from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    tel = models.IntegerField()


class Task(models.Model):
    task = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    send = models.TimeField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
