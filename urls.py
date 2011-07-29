from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView
from public_html.blog.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$',
        PostListView.as_view(),
        name='index'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name='post'),

    url(r'^category/(?P<category>[-\w]+)/$',
        PostCategoryListView.as_view(),
        name='category'),

    url(r'^user/(?P<user>[-\w]+)/$',
        PostUserListView.as_view(),
        name='user'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        PostDayArchiveView.as_view(),
        name='archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        PostMonthArchiveView.as_view(),
        name='archive_month'),

    url(r'^(?P<year>\d{4})/$',
        PostYearArchiveView.as_view(),
        name='archive_year'),

    url(r'^about/',
        TemplateView.as_view(template_name = 'about.html'),
        name='about'),

    url(r'^contact/',
        TemplateView.as_view(template_name = 'contact.html'),
        name='contact'),
)
