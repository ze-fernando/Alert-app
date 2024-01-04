from django.views.decorators.csrf import csrf_exempt
from .service import Authentication, SendMessage
from django.http import JsonResponse
from datetime import datetime
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
        user = Authentication.authenticate(data['name'], data['password'])
        if user is not None:
            token = JwtToken.generate(user.id, user.name)
            return JsonResponse({'token': f'{token}'}, status=200)
        else:
            return JsonResponse({'message': 'name or nassword invalid'}, status=401)
    else:
        return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)


@csrf_exempt
def create_task(req):
    if req.method == 'POST':
        try:
            token = req.headers.get('Authorization', '').split(' ')[1]
            if JwtToken.verify_jwt(token):
                data = json.loads(req.body)
                all_tasks = Task.objects.filter(user = data['user'])
                if len(all_tasks) >= 3:
                    return JsonResponse({'message': "you just have 3 task's in your profile"}, status=400)

                task = Task(
                    task = data['task'],
                    hourSend = data['hour'],
                    sendFor = data['sendTo'],
                    user = User.objects.get(id=data['user'])
                )
                task.save()
                return JsonResponse({'message': 'Task created!'})
            else:
                 return JsonResponse({'error': 'token invalid'}, status=401)
        except Exception as e:
            return JsonResponse({'error': e}, status=401)      
    else:
        return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)

        
@csrf_exempt
def del_task(req, id):
    if req.method == 'DELETE':
        try:
            token = req.headers.get('Authorization', '').split(' ')[1]
            if JwtToken.verify_jwt(token):
                task = Task.objects.get(id = id)
                task.delete()
                return JsonResponse({'message': 'Task deleted!'})
            else:
                 return JsonResponse({'error': 'token invalid'}, status=401)
        except Exception as e:
            return JsonResponse({'error': e}, status=401)      
    else:
        return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)


@csrf_exempt
def put_task(req, id):
    if req.method == 'PUT':
        try:
            token = req.headers.get('Authorization', '').split(' ')[1]
            if JwtToken.verify_jwt(token):
                data = json.loads(req.body)
                
                task = Task.objects.get(id = id)
                
                task.task = data['task']
                task.hourSend = data['hour']
                task.sendFor = data['sendTo']
                
                task.save()
                return JsonResponse({'message': 'Task updated!'})
            else:
                 return JsonResponse({'error': 'token invalid'}, status=401)
        except Exception as e:
            return JsonResponse({'error': e}, status=401)      
    else:
        return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)


def sendTask(task):
    hour_task = datetime.strptime(task.hourSend, '%H:%M').time().replace(second=0, microsecond=0)
    now = datetime.now().time().replace(second=0, microsecond=0)
    if hour_task == now:
        if task.sendFor == 'email':
            SendMessage.send_email(task)
        elif task.sendFor == 'phone':
            SendMessage.send_wpp(task)
