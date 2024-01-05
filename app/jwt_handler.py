from datetime import datetime, timedelta
from dotenv import load_dotenv
from .models import User
import jwt
import os

load_dotenv()

class JwtToken:
    SECRET_KEY = os.environ['JWT_KEY']
    
    def generate(id, username):
        payload = {
            'user_id': id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, JwtToken.SECRET_KEY, algorithm='HS256')
        return token
    
    def verify_jwt(token):
        try:
            payload = jwt.decode(token, JwtToken.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            return User.objects.get(id=user_id)
        except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
            return None