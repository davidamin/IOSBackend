from django.db import models

class Profile(models.Model):
	username = models.CharField(max_length=250)
	password = models.CharField(max_length=256)
	games_played = models.IntegerField()
	lifetime_score = models.IntegerField()
	high_score = models.IntegerField()
	best_game = models.IntegerField()
	best_questions = models.IntegerField()
	best_fast = models.IntegerField()

class Question(models.Model):
	text = models.CharField(max_length=250)
	is_fast = models.BooleanField(default=False)
	
class Answers(models.Model):
	text = models.CharField(max_length=250)
	points = models.IntegerField()
