from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.http import JsonResponse
from .jwt_handler import JwtToken
from datetime import datetime
from .service import Service
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
                email = data['email']
            )
            user.save()
            return JsonResponse({'message': f"User {data['name']} created!"}, status=201)
        
        except Exception as e:
            return JsonResponse({'message': 'Internal server error', 'Error': f'{e}'}, status=500)
        
    return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)


@csrf_exempt
def signin(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        user = Service.authenticate(data['name'], data['password'])
        if user is not None:
            token = JwtToken.generate(user.id, user.name)
            return JsonResponse({'token': f'{token}'}, status=200)
    
        return JsonResponse({'message': 'name or nassword invalid'}, status=401)
    
    return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)


@csrf_exempt
def tasks(req, id):
    if req.method == 'GET':
        try:
            token = req.headers.get('Authorization', '').split(' ')[1]
            if JwtToken.verify_jwt(token):
                user = User.objects.get(id=id)
                all_tasks = Task.objects.filter(user = user)
                tasks_list = []
                for task in all_tasks:
                    task_dict = {
                        'id': task.pk,
                        'task': str(task.task),
                        'created': task.created.isoformat(),
                        'hourSend': task.hourSend.strftime('%H:%M:%S'),
                        'user': task.user.name
                    }
                    tasks_list.append(task_dict)
                
                return JsonResponse(tasks_list, safe=False, status=200)
            
            return JsonResponse({'error': 'token invalid'}, status=401)
        
        except Exception as e:
            return JsonResponse({'error': e}, status=401)      
    
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
                    user = User.objects.get(id=data['user'])
                )
                
                task.save()
                return JsonResponse({'message': 'Task created!'})
            
            return JsonResponse({'error': 'token invalid'}, status=401)
        
        except Exception as e:
            return JsonResponse({'error': e}, status=401)      
    
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
    
            return JsonResponse({'error': 'token invalid'}, status=401)
        except Exception as e:
            return JsonResponse({'error': e}, status=401)      
    
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
                
                task.save()
                return JsonResponse({'message': 'Task updated!'})
    
            return JsonResponse({'error': 'token invalid'}, status=401)
        except Exception as e:
            return JsonResponse({'error': e}, status=401)      
    
    return JsonResponse({'error': f'Method {req.method} not allowed'}, status=405)


def sendTask(task):
    hour_task = datetime.strptime(task.hourSend, '%H:%M').time().replace(second=0, microsecond=0)
    now = datetime.now().time().replace(second=0, microsecond=0)
    if now == hour_task:
        Service.send_email(task)