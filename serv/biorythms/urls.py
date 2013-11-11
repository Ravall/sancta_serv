from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from datetime import date

urlpatterns = patterns('',
    url(r'^$', 'biorythms.views.index', name='bio_home'),
    url(
        r'(?P<birthday>\d{4}-\d{2}-\d{2})/(?P<cur_date>\d{4}-\d{2}-\d{2})',
        'biorythms.views.biorythm', name='bio_birthday'
    ),
    url(
        r'(?P<birthday>\d{4}-\d{2}-\d{2})',
        'biorythms.views.biorythm', {'cur_date':None},
        name='bio_birthday'
    )
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
