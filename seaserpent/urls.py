from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'seaserpent.core.views.home', name='home'),
    url(r'^(\d+)/$', 'seaserpent.core.views.price_history', name='price_history'),
    url(r'^admin/', include(admin.site.urls)),
)
