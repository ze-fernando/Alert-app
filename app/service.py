from django.contrib.auth.hashers import check_password
from .models import User

class AuthenticationService:
    @staticmethod
    def authenticate(name, password):
        try:
            user = User.objects.get(name=name)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            pass
        return None
