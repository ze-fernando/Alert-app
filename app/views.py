from django.views.decorators.csrf import csrf_exempt
from .service import AuthenticationService as auth
from django.http import JsonResponse
from .jwt_handler import JwtToken
from .models import *
import json

@csrf_exempt
def signup(req):
    if req.method == 'POST':
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
    else:
        return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)



@csrf_exempt
def signin(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        user = auth.authenticate(data['name'], data['password'])
        if user is not None:
            token = JwtToken.generate(user.id, user.name)
            return JsonResponse({'token': f'{token}'}, status=200)
        else:
            return JsonResponse({'message': 'name or nassword invalid'}, status=401)
    else:
        return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)


@csrf_exempt
def task(req):
    if req.method == 'POST':
        try:
            token = req.headers.get('Authorization', '').split(' ')[1]
            if JwtToken.verify_jwt(token):
                data = json.loads(req.body)
                task = Task(
                task = data['task'],
                hourSend = data['hour'],
                sendFor = data['sendTo'],
                user = User.objects.get(id=data['user'])
                )
                print(task.created)
                task.save()
                return JsonResponse({'message': 'Task created!'})

        except Exception:
            return JsonResponse({'error': 'token invalid'}, status=401)
    else:
        return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)