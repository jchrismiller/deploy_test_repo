from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^logout$', views.index),
	url(r'^registration$', views.registration),
	url(r'^success$', views.success),
	url(r'^ship/(P?\d+)$', views.ship)
	# url(r'^user/(?P<user_id>\d+)$', views.show)
]