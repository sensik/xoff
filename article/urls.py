from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView, TemplateView
from wall.models import Entry

urlpatterns = patterns('',
	url(r'^(?P<slug>[-a-z0-9]+)/$', 'article.views.article', name = 'article')
)