from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import django.utils.simplejson as json
import time, random
from deck.models import *
from game.models import *
from chat.models import *

def game_page(request, id):
	try:
		game = Game.objects.get(id=id)
		r = Room.objects.get_or_create(game)
		playArea = GameCard.objects.filter(game=game, location='t')
		hand = GameCard.objects.filter(game=game, location='h', owner=request.user)
		deckCount = len(GameCard.objects.filter(game=game, owner=request.user, location='d'))
		return render_to_response(
			'game.html',
			RequestContext(request, {"cards": playArea, "hand":hand, "chat_id":r.pk, "p1":game.player1, "p2":game.player2, "deckCount":deckCount })
		)
	except:
		raise Http404('Whoops')

@login_required
@csrf_exempt
def move(request, cID, x, y, z):
	try:
		card = GameCard.objects.get(id=cID)
		card.xLoc = x
		card.yLoc = y
		card.zLoc = z
		card.save()
		return HttpResponse('')
	except:
		raise Http404('Whoops move')

@login_required
def draw(request, gameID):
	game = Game.objects.get(id=gameID)
	deck = GameCard.objects.filter(game=game, owner=request.user, location='d')
	if( len(deck) > 0):
		draw = deck[random.randint(0, (len(deck) - 1))]
		draw.location = 'h'
		draw.yLoc = 786
		draw.xLoc = 50
		draw.save()
		game.lastAdd = time.time() * 1000
		game.save()
	return HttpResponse('')

@login_required
@csrf_exempt
def changeArea(request, cID, loc):
	try:
		card = GameCard.objects.get(id=cID)
		card.location = loc
		card.save()
		card.game.lastAdd = time.time() * 1000
		card.game.save()
		return HttpResponse('')
	except:
		raise Http404('Whoops changeArea')

@login_required
@csrf_exempt
def sync(request, id):
	try:	
		game = Game.objects.get(id=id)
		out = []
		cards = GameCard.objects.filter(game=game).exclude(location='d')
		for c in cards:
			tmp = {}
			tmp['type'] = 'card'
			tmp['id'] = c.id
			tmp['x'] = c.xLoc
			tmp['y'] = c.yLoc
			tmp['z'] = c.zLoc
			out.append(tmp)
		tokens = Token.objects.filter(game=game)
		for t in tokens:
			tmp = {}
			tmp['type'] = 'token'
			tmp['id'] = t.id
			tmp['x'] = t.xLoc
			tmp['y'] = t.yLoc
			tmp['qty'] = t.qty
			out.append(tmp)
		return HttpResponse(json.dumps([{'lastUpdate': game.lastAdd}, {'data':out}]))

	except:
		raise Http404('Whoops sync')

