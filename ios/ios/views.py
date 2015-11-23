from django.http import HttpResponse, JsonResponse
from ios import models
from django.core import serializers
import json
from django.contrib.auth.hashers import make_password, check_password

def model_to_json(model):
	data = serializers.serialize('json',[model,])
	struct = json.loads(data)
	data = json.dumps(struct[0])
	return data

def index(request):
	return JsonResponse({'user':'dave'})

def add_user(request):
	if request.method != 'POST':
		return JsonResponse({'ok': False, 'error': 'Wrong request type, should be post'})
	try:
		new_user = models.Profile()
		new_user.username = request.POST['username']
		new_user.password = make_password(request.POST['password'])
		new_user.games_played = 0
		new_user.lifetime_score = 0
		new_user.high_score = 0
		new_user.best_game = 0
		new_user.best_questions = 0
		new_user.best_fast = 0
		new_user.save()
		return JsonResponse({'ok': True, 'user': 'Created new user ' + new_user.username})

	except Exception as e:
		this_user = models.Profile.objects.get(username=request.POST['username'])
		if check_password(request.POST['password'], this_user.password):
			return JsonResponse({'ok': True, 'user': 'User ' + request.POST['username']})
		else:
			return JsonResponse({'ok':False, 'user': 'Invalid password ' + request.POST['password']})

def add_question(request):
	#Because Nick wants me to write good code
	if request.method != 'POST':
		return JsonResponse({'ok': False, 'error': 'Wrong request type, should be post'})
	incoming_json = json.loads(request.body.decode('utf8'))
	new_question = models.Question()
	if 'question' in incoming_json:
		new_question.text = incoming_json['question']
	new_question.is_fast = False
	new_question.save()
	ans_list = incoming_json['answers']
	for ans in ans_list:
		answer = models.Answers()
		answer.question = new_question
		answer.text = ans['answer']
		answer.points = ans['score']
		answer.save()
	return JsonResponse({'ok':True, 'log': 'Made question'})

def add_fast(request):
	#Because Nick wants me to write good code
	if request.method != 'POST':
		return JsonResponse({'ok': False, 'error': 'Wrong request type, should be post'})
	incoming_json = json.loads(request.body.decode('utf8'))
	new_question = models.Question()
	if 'question' in incoming_json:
		new_question.text = incoming_json['question']
	new_question.is_fast = True
	new_question.save()
	ans_list = incoming_json['answers']
	for ans in ans_list:
		answer = models.Answers()
		answer.question = new_question
		answer.text = ans['answer']
		answer.points = ans['score']
		answer.save()
	return JsonResponse({'ok':True, 'log': 'Made question'})


