# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from deck.forms import *
from deck.models import *
from chat.models import *
from game.models import *
from django import forms

def main_page(request):
	u = User.objects.get(id=1)
	r = Room.objects.get_or_create(u)
	return render_to_response(
		'news.html',
		RequestContext(request, { "chat_id":r.pk }),
	)

def games_page(request):
	games = Game.objects.filter(player1=request.user)
	games2 = Game.objects.filter(player2=request.user)
	incomingProposals = Proposal.objects.filter(recipient=request.user)
	outgoingProposals = Proposal.objects.filter(proposer=request.user)
	u = User.objects.get(id=1)
	r = Room.objects.get_or_create(u)
	userDrop = AllUserDropdownForm()
	decks = Decks.objects.filter(owner=request.user)
	return render_to_response('games.html',
		RequestContext(request, { "chat_id":r.pk, "games":games, 'games2':games2, 'incomingProposals':incomingProposals, 'outgoingProposals':outgoingProposals, 'userDrop':userDrop, 'decks':decks }),
	)

def accept_proposal(request, proposalID, deckID):
	deck = Decks.objects.get(id=deckID)
	proposal = Proposal.objects.get(id=proposalID)
	game = Game(
		player1 = proposal.proposer,
		player2 = proposal.recipient,
		p1Deck = proposal.proposerDeck,
		p2Deck = deck,
		lastAdd = 0)
	game.save()
	setup(game)
	proposal.delete()	
	return HttpResponseRedirect("/game/%d" % game.id)

def setup(game):
	for card in Deck.objects.filter(deckID=game.p1Deck):
		GameCard(
			game = game,
			owner = game.player1,
			location = 'd',
			card = card.cardID,
			xLoc = 0,
			yLoc = 0, 
			zLoc = 1
		).save()
	for card in Deck.objects.filter(deckID=game.p2Deck):
		GameCard(
			game = game,
			owner = game.player2,
			location = 'd',
			card = card.cardID,
			xLoc = 0,
			yLoc = 0, 
			zLoc = 1
		).save()


def decline_proposal(request, proposalID):
	Proposal.objects.get(id=proposalID).delete()
	return HttpResponseRedirect('/games/')

@login_required
@csrf_exempt
def propose(request):
	p = request.POST
	proposer = request.user
	deck = Decks.objects.get(id=int(p['deck']))
	message = p['message']
	recipient = User.objects.get(id=int(p['recipient']))
	proposal = Proposal(
		proposer = proposer,
		proposerDeck = deck,
		message = message,
		recipient = recipient	
	)
	proposal.save()
	return HttpResponseRedirect('/games/')

def add_to_deck(request, deckID, cardID):
#first arg will be deckID, second arg will be cardiid
	owner = Decks.objects.get(id=deckID).owner
	if request.user != owner:
		return HttpResponseRedirect('/deck_builder/')
	deck = Decks.objects.get(id=deckID)
	card = Card.objects.get(id=cardID)	
	deckCard = Deck.objects.filter(deckID=deck, cardID=card)
	if len(deckCard) == 1:
		deckCard[0].qty += 1
		deckCard[0].save()
	else:
		Deck.objects.get_or_create(deckID=deck, cardID=card, qty=1)
	return HttpResponseRedirect('/deck_builder/%s/' % deckID)

def delete_from_deck(request, deckID, cardID):
#first arg will be deckID, second arg will be cardiid
	owner = Decks.objects.get(id=deckID).owner
	if request.user != owner:
		return HttpResponseRedirect('/deck_builder/')
	deck = Decks.objects.get(id=deckID)
	card = Card.objects.get(id=cardID)	
	deckCard = Deck.objects.filter(deckID=deck, cardID=card)
	if len(deckCard) == 1:
		if deckCard[0].qty == 1:
			deckCard[0].delete()
		else:
			deckCard[0].qty -= 1
			deckCard[0].save()
	return HttpResponseRedirect('/deck_builder/%s/' % deckID)

def deck_builder(request, deckID):
	try:
		deck = Decks.objects.get(id=deckID)
	except:
		raise Http404('Deck not found, try making it first.')
	deckCards = Deck.objects.filter(deckID=deck)
	cards = Card.objects.all()
	return render_to_response(
		'deck_builder.html',
		RequestContext(request, { 'cards': cards, 'deck': deck, 'deckCards': deckCards })
	)

def deck_select(request):
	if request.method == 'POST':
		form = NewDeckForm(request.POST)
		if form.is_valid():
			#add deck
			deckName = form.cleaned_data['deckName']
			if len(deckName) < 50 and len(deckName) > 0:
				deck, made = Decks.objects.get_or_create(
					owner = request.user,
					name = deckName
				)
				return HttpResponseRedirect('/deck_builder/%s/' % deck.id)
			else:
				return HttpResponseRedirect('/deck_builder/')
		return HttpResponseRedirect('/deck_builder/')
	else:
		form = NewDeckForm()
		decks = Decks.objects.filter(owner=request.user)
		return render_to_response(
			'deck_select.html',
			RequestContext(request, { 'form': form, 'decks': decks })
		)
					
def user_page(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404('U Dumb')
	books = user.bookmark_set.all()
	template = get_template('user_page.html')
	variables = RequestContext(request, {
		'username': username,
		'bookmarks': books
	})
	return render_to_response('user_page.html', variables)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email']
			)
			return HttpResponseRedirect('/')
	else:
		form = RegistrationForm()
	variables = RequestContext(request, {
		'form': form
	})
	return render_to_response(
		'registration/register.html',
		variables
	)

