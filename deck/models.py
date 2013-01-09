from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Card(models.Model):
	name = models.CharField(max_length=50)
	cost = models.IntegerField()
	race = models.CharField(max_length=15)
	num = models.IntegerField()
	def __str__(self):
		return self.name
	
class Decks(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(User)	
	def __str__(self):
		return self.name

class Deck(models.Model):
	cardID = models.ForeignKey(Card)
	deckID = models.ForeignKey(Decks)	
	qty = models.IntegerField()
	def __str__(self):
		return "%s: %s: %d" % (self.deckID.name, self.cardID.name, self.qty)
