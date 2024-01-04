from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from twilio.rest import Client
from dotenv import load_dotenv
from .models import User
import os

load_dotenv()

class Authentication:
    @staticmethod
    def authenticate(name, password):
        try:
            user = User.objects.get(name=name)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            pass
        return None
    

class SendMessage:
    REMETENTE = os.environ['EMAIL_USER']
    NUMBER = os.environ['NUMBER']
    @staticmethod
    def send_email(task):
        send_mail(
            'Your from app django',
            f"{task.user.name} your task {task.task} it's now!",
            SendMessage.REMETENTE,
            [task.user.email],
            fail_silently=False
        )
    
    @staticmethod
    def send_wpp(task):
        account_sid = os.environ['SID']
        auth_token = os.environ['AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_ = SendMessage.NUMBER,
            body = f"your task {task.task} is now",
            to = task.tel
        )

        print(message.sid)