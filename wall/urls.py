from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView, TemplateView
from wall.models import Entry

urlpatterns = patterns('',
	url(r'^(?P<pk>\d*)/$', 'wall.views.detailEntry', name = 'detailEntry')
)