from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from dotenv import load_dotenv
from .models import User
import os

load_dotenv()

class Service:
    REMETENTE = os.environ['EMAIL_USER']

    @staticmethod
    def authenticate(name, password):
        try:
            user = User.objects.get(name=name)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            pass
        return None
    

    @staticmethod
    def send_email(task):
        send_mail(
            'Your from app django',
            f"{task.user.name} your task {task.task} it's now!",
            Service.REMETENTE,
            [task.user.email],
            fail_silently=False
        )