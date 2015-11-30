from django.db import models

class Profile(models.Model):
	username = models.CharField(max_length=250, unique = True)
	password = models.CharField(max_length=256)
	email = models.EmailField()
	games_played = models.IntegerField()
	lifetime_score = models.IntegerField()
	high_score = models.IntegerField()
	perfect_boards = models.IntegerField()
	best_questions = models.IntegerField()
	best_fast = models.IntegerField()

class Question(models.Model):
	text = models.CharField(max_length=250)
	is_fast = models.BooleanField(default=False)
	
class Answers(models.Model):
	question = models.ForeignKey(Question)
	text = models.CharField(max_length=250)
	points = models.IntegerField()
