import json
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@require_POST
def signup(req):
    data = json.loads(req.body)
    try:
        user = User(
            name = data['name'],
            password = data['pass'],
            email = data['email'],
            tel = data['tel']
        )
        user.save()
        return JsonResponse({'message': f"User {data['name']} created!"})
    
    except Exception as e:
        return JsonResponse({'message': 'Internal server error', 'Error': f'{e}'})
        
        