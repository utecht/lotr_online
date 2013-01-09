from django.contrib import admin
from deck.models import *
from chat.models import *
from game.models import *

admin.site.register(Deck)
admin.site.register(Decks)
admin.site.register(Card)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Game)
admin.site.register(Proposal)
admin.site.register(GameCard)
admin.site.register(Token)
