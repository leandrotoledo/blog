# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from public_html.blog.models import *
from public_html.blog.views import PostCategoryListView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    #(r'^i18n/', include('django.conf.urls.i18n')),

    (r'^comments/', include('django.contrib.comments.urls')),

    url(r'^category/(\w+)/$',
        PostCategoryListView.as_view(),
        name='category'),

    url(r'^$',
        ListView.as_view(
            template_name = 'list.html',
            paginate_by = 3,
            model = Post
        ),
        name='index'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        DetailView.as_view(
            context_object_name = 'post',
            template_name = 'post.html',
            model = Post
        ),
        name='post'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(
            template_name = 'list.html',
            month_format = '%m',
            date_field = 'published_date',
            model = Post
        ),
        name='archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthArchiveView.as_view(
            template_name = 'list.html',
            month_format = '%m',
            date_field = 'published_date',
            model = Post
        ),
        name='archive_month'),

    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            make_object_list = True,
            template_name = 'list.html',
            date_field = 'published_date',
            model = Post
        ),
        name='archive_year'),

    url(r'^about/',
        TemplateView.as_view(
            template_name   = 'about.html'
        ),
        name='about'),

    url(r'^contact/',
        TemplateView.as_view(
            template_name   = 'contact.html'
        ),
        name='contact'),
)
