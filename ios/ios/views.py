from django.http import HttpResponse, JsonResponse
from ios import models

def index(request):
	return JsonResponse({'user':'dave'})
