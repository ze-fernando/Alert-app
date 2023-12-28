from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os


load_dotenv()

class JwtToken:
    SECRET_KEY = os.environ['JWT_KEY']
    
    def generate(id, username):
        payload = {
            'user_id': id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JwtToken.SECRET_KEY, algorithm='HS256')
        return token