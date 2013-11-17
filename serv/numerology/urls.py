from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^$', 'numerology.views.index', name='num_home'),
    url(r'(?P<digit>[0-9]+)', 'numerology.views.digit_birhday', name='num_birthday'),
    url(r'^all$', 'numerology.views.all', name='all_nums'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
