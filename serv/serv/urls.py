from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from serv.sitemap import sitemaps

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'frontend.views.index', name='home'),
    url(r'^numerology/', include('numerology.urls')),
    url(r'^biorythms/', include('biorythms.urls')),

    url(r'', include('robots_txt.urls')),
    url(r'^', include('favicon.urls')),
    url(
        r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}
    ),

    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
