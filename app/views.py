import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@require_POST
def signup(req):
    data = json.loads(req.body)
    return JsonResponse(data, safe=False)