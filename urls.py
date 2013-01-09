from django.conf.urls.defaults import *
from deck.views import *
from game.views import *
import os.path
from django.contrib import admin

site_media = os.path.join(
	os.path.dirname(__file__), 'site_media'
)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', main_page),
	(r'^user/(\w+)/$', user_page),
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', logout_page),
	(r'^deck_builder/(\d+)/$', deck_builder),
	(r'^deck_builder/(\d+)/add/(\d+)/$', add_to_deck),
	(r'^deck_builder/(\d+)/del/(\d+)/$', delete_from_deck),
	(r'^deck_builder/$', deck_select),
	(r'^herebedragons/$', register_page),
	(r'^goaway/', include(admin.site.urls)),
	(r'^accept/(\d+)/(\d+)/$', accept_proposal),
	(r'^decline/(\d+)/$', decline_proposal),
	(r'^propose/$', propose),
	(r'^games/$', games_page),
	(r'^game/(\d+)/$', game_page),
	(r'^game/(\d+)/draw/$', draw),
	(r'^game/(\d+)/sync$', 'game.views.sync'),
	(r'^game/move/(\d+)/x(\d+)/y(\d+)/z(\d+)/$', move),
	(r'^game/changeArea/(\d+)/(\w)/$', changeArea),
#	(r'^test/$', 'chat.views.test'),
	(r'^chat/send/$', 'chat.views.send'),
 	(r'^chat/receive/$', 'chat.views.receive'),
 	(r'^chat/sync/$', 'chat.views.sync'),
    	(r'^chat/join/$', 'chat.views.join'),
	(r'^chat/leave/$', 'chat.views.leave'),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': site_media }), 
   # Example:
    # (r'^django_test/', include('django_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
)
