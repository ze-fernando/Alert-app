import json
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def signup(req):
    data = json.loads(req.body)
    usr = User.objects.filter(name=data['name']).exists()
    if usr:
        return JsonResponse({'message': f'User {data['name']} aleredy exists'}, status=422)
    try:
        user = User(
            name = data['name'],
            password = data['password'],
            email = data['email'],
            tel = data['tel']
        )
        user.save()
        return JsonResponse({'message': f"User {data['name']} created!"}, status=201)
    
    except Exception as e:
        return JsonResponse({'message': 'Internal server error', 'Error': f'{e}'}, status=500)
        

@csrf_exempt
@require_POST
def signin(req):
    data = json.loads(req.body)
    usr = User.objects.get(name=data['name'])
    passw = check_password(data['password'], usr.password)
    if passw:
        return JsonResponse({'msg': 'true'}, status=200)
    else:
        return JsonResponse({'msg': 'false'}, status=401)
