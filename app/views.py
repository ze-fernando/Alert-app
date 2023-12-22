import json
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@require_POST
def signup(req):
    data = json.loads(req.body)
    user = User(
        name = data['name'],
        email = data['email'],
        tel = data['tel']
    )
    user.save()
    
    return JsonResponse({'message': f"User {data['name']} created!"}, status_code=201)