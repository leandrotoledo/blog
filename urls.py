# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from public_html.blog.models import *

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
        'django.views.generic.list_detail.object_list',
        {
            'queryset':             Post.objects.all().order_by('-published_date'),
            'paginate_by':          3,
            'template_name':        'list.html',
        },
        name='index'),

    url(r'^category/(?P<slug>[-\w]+)/$',
        'public_html.blog.views.category',
        name='category'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        'public_html.blog.views.post',
        name='post'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        'django.views.generic.date_based.archive_day',
        {
            'queryset':         Post.objects.all().order_by('-published_date'),
            'date_field':       'published_date',
            'month_format':     '%m',
            'template_name':    'list.html',
            'extra_context':    {
                'description':      'Histórico do dia:'
            }
        },
        name='archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        'django.views.generic.date_based.archive_month',
        {
            'queryset':         Post.objects.all().order_by('-published_date'),
            'date_field':       'published_date',
            'month_format':     '%m',
            'template_name':    'list.html',
            'extra_context':    {
                'description':      'Histórico do mês:'
            }
        },
        name='archive_month'),

    url(r'^(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year',
        {
            'queryset':         Post.objects.all().order_by('-published_date'),
            'date_field':       'published_date',
            'template_name':    'list.html',
            'make_object_list': True,
            'extra_context':    {
                'description':      'Histórico do ano: '
            }
        },
        name='archive_year'),

    url(r'^about/$',
        direct_to_template,
        {'template': 'about.html'},
        name='about'),

    url(r'^contact/$',
        direct_to_template,
        {'template': 'contact.html'},
        name='contact'),

    url(r'^search/$',
        direct_to_template,
        {'template': 'search.html'},
        name='search'),
)
