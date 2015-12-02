from django.http import HttpResponse, JsonResponse
from ios import models
from django.core import serializers
import json
from django.contrib.auth.hashers import make_password, check_password
from random import randint
import random
from django.core.mail import send_mail

def model_to_json(model):
	data = serializers.serialize('json',[model,])
	struct = json.loads(data)
	data = json.dumps(struct[0])
	return data

def index(request):
	return JsonResponse({'user':'dave'})

def register_user(request):
	if request.method != 'POST':
		return JsonResponse({'ok': False, 'error': 'Wrong request type, should be post'})
	try:
		new_user = models.Profile()
		new_user.username = request.POST['username']
		new_user.password = make_password(request.POST['password'])
		new_user.email = request.POST['email']
		new_user.games_played = 0
		new_user.lifetime_score = 0
		new_user.high_score = 0
		new_user.perfect_boards = 0
		new_user.best_questions = 0
		new_user.best_fast = 0
		new_user.save()
		return JsonResponse({'ok': True, 'user': 'Created new user ' + new_user.username})

	except Exception as e:
		return JsonResponse({'ok': False, 'error': 'Registration Failed'})



def login(request):
	try:
		this_user = models.Profile.objects.get(username=request.POST['username'])
		if check_password(request.POST['password'], this_user.password):
			return JsonResponse({'ok': True, 'user': 'User ' + request.POST['username']})
		else:
			return JsonResponse({'ok':False, 'error': 'Invalid username/password'})
	except:
			return JsonResponse({'ok':False, 'error': 'Login failed'})	

def add_user(request):
	if request.method != 'POST':
		return JsonResponse({'ok': False, 'error': 'Wrong request type, should be post'})
	try:
		new_user = models.Profile()
		new_user.username = request.POST['username']
		new_user.password = make_password(request.POST['password'])
		new_user.email = request.POST['email']
		new_user.games_played = 0
		new_user.lifetime_score = 0
		new_user.high_score = 0
		new_user.perfect_boards = 0
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

def get_question(request):
	count = models.Question.objects.filter(is_fast=False).count()
	index = randint(0,count-1)
	rand_question = models.Question.objects.filter(is_fast=False)[index]
	answers = models.Answers.objects.filter(question=rand_question)
	ret_list = [{'answer': a.text, 'score': str(a.points)} for a in answers]
	return JsonResponse({'ok':True,'question':rand_question.text, 'answers':ret_list})

def get_fast(request):
	count = models.Question.objects.filter(is_fast=True).count()
	index = randint(0,count-1)
	rand_question = models.Question.objects.filter(is_fast=True)[index]
	answers = models.Answers.objects.filter(question=rand_question)
	ret_list = [{'answer': a.text, 'score': str(a.points)} for a in answers]
	return JsonResponse({'ok':True,'question':rand_question.text, 'answers':ret_list})

def add_score(request):
	if request.method != 'POST':
		return JsonResponse({'ok': False, 'error':'Must use POST'})
	#just take a score, and a user, check if it's higher
	try:
		user = models.Profile.objects.get(username=request.POST['username'])
	except:
		return JsonResponse({'ok':False, 'error': 'User not found'})
	score = int(request.POST['questions']) + int(request.POST['fast'])
	user.games_played += 1
	user.lifetime_score += score
	if score > user.high_score:
		user.high_score = score
	if int(request.POST['questions']) > user.best_questions:
		user.best_questions = int(request.POST['questions'])
	if int(request.POST['fast']) > user.best_fast:
		user.best_fast = int(request.POST['fast'])
	if 'perfect_boards' in request.POST:
		user.perfect_boards += int(request.POST['perfect_boards'])
	user.save()
	return JsonResponse({'ok': True,'log': 'Scores Updated'})

def get_user_data(request):
	if request.method != 'POST':
		return JsonResponse({'ok': False, 'error':'Must use POST'})
	try:
		user = models.Profile.objects.get(username=request.POST['username'])
		return JsonResponse({'ok': True, 'played': user.games_played, 'high': user.high_score, 'best_questions': user.best_questions, 'best_fast': user.best_fast, 'lifetime': user.lifetime_score, 'perfect_boards':user.perfect_boards})
	except:
		return JsonResponse({'ok': False, 'error': 'User not found'})

def get_high_scores(request):
	profiles = models.Profile.objects.all()
	score_list = [{'score':p.lifetime_score, 'name': p.username} for p in profiles]
	return JsonResponse({'ok': True, 'scores':score_list})

def change_pass(request):
	try:
		this_user = models.Profile.objects.get(username=request.POST['username'])
		if check_password(request.POST['old'], this_user.password):
			this_user.password = make_password(request.POST['new'])
			this_user.save()
			return JsonResponse({'ok': True, 'log': 'password changed'})
		else:
			return JsonResponse({'ok':False, 'error': 'Invalid password'})
	except:
			return JsonResponse({'ok':False, 'error': 'Failed to find user'})	

def send_email(request):
	try:
		this_user = models.Profile.objects.get(username=request.POST['username'])
		if this_user.email == request.POST['email']:
			temp_pass = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
			this_user.password = make_password(temp_pass)
			this_user.save()
			send_mail("Here's Your Temporary Password", "Your temporary password: " + temp_pass,"webandmobilefamilyfeud@gmail.com",[this_user.email], fail_silently=False)
			return JsonResponse({'ok': True, 'log': 'email sent'})
		else:
			return JsonResponse({'ok':False, 'error': 'Email Invalid'})
	except:
			return JsonResponse({'ok':False, 'error': 'Failed to find user'})	

