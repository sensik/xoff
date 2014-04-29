from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView, TemplateView
from wall.models import Entry

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xoff.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^entry/', include('wall.urls')),
	url(r'^tag/', include('wall.urls')),
	url(r'^author/(?P<author>[a-zA-Z0-9]+)/$', 'wall.views.author', name = 'author'),
	url(r'^$', 'wall.views.allEntries', name = 'allEntries'),
)