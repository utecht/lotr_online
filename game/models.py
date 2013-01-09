from django.db import models
from django.contrib.auth.models import User
from deck.models import *

class Game(models.Model):
	player1 = models.ForeignKey(User, related_name='player1')
	player2 = models.ForeignKey(User, related_name='player2')
	p1Deck = models.ForeignKey(Decks, related_name='p1Deck')
	p2Deck = models.ForeignKey(Decks, related_name='p2Deck')
	lastAdd = models.PositiveIntegerField()
	def __str__(self):
		return self.player1.username + " v " + self.player2.username

class Proposal(models.Model):
	proposer = models.ForeignKey(User, related_name='proposer')
	recipient = models.ForeignKey(User, related_name='recipient')
	proposerDeck = models.ForeignKey(Decks)
	message = models.CharField(max_length=255, blank=True, null=True)
	time = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.proposer.username + ' v ' + self.recipient.username

CARD_LOCATIONS = (
	('d', 'deck'),
	('h', 'hand'),
	('t', 'table'),
	('s', 'discard')
)

class GameCard(models.Model):
	''' A card in a game '''
	game = models.ForeignKey(Game)
	owner = models.ForeignKey(User)
	location = models.CharField(max_length=1, choices=CARD_LOCATIONS)
	card = models.ForeignKey(Card)
	xLoc = models.PositiveSmallIntegerField()
	yLoc = models.PositiveSmallIntegerField()
	zLoc = models.PositiveSmallIntegerField()
	def __str__(self):
		return "%s %s:%d,%d,%d" % (self.owner.username, self.card.name, self.xLoc, self.yLoc, self.zLoc)

TOKEN_COLOR = (
	('r', 'red'),
	('b', 'black')
)

class Token(models.Model):
	game = models.ForeignKey(Game)
	color = models.CharField(max_length=1, choices=TOKEN_COLOR)
	xLoc = models.PositiveSmallIntegerField()
	yLoc = models.PositiveSmallIntegerField()
	qty = models.PositiveSmallIntegerField()
	def __str__(self):
		return "%s %s" % (self.game, self.color)
