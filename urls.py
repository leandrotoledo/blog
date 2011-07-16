from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'public_html.views.home', name='home'),
    # url(r'^public_html/', include('public_html.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^comments/', include('django.contrib.comments.urls')),

    url(r'^$',
        'public_html.blog.views.index',
        name='index'),

    url(r'^category/(?P<slug>[-\w]+)/$',
        'public_html.blog.views.category'),
    # http://leandrotoledo.com.br/category/gnu-linux/

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'public_html.blog.views.post'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'public_html.blog.views.index'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'public_html.blog.views.index'),

    url(r'^(?P<year>\d{4})/$',
        'public_html.blog.views.index'),
    # http://leandrotoledo.com.br/2011/07/09/sparkleshare-uma-alternativa-livre-do-dropbox/

    url(r'^about/$',
        'public_html.blog.views.about',
        name='about'),

    url(r'^contact/$',
        'public_html.blog.views.contact',
        name='contact'),
)
