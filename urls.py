from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView
from django.contrib.sitemaps import GenericSitemap
from public_html.blog.models import *
from public_html.blog.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

info_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'updated_date'
}

sitemaps = {
    'blog': GenericSitemap(info_dict, priority=1.0)
}

urlpatterns = patterns('',
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$',
        PostListView.as_view(),
        name='index'),

    (r'^posts/$',
        RedirectView.as_view(url='/')),

    (r'^categories/$',
        RedirectView.as_view(url='/')),

    (r'^pages/$',
        RedirectView.as_view(url='/')),

    url(r'^categories/(?P<category>[-\w]+)/$',
        PostCategoryListView.as_view(),
        name='category'),

    url(r'^users/(?P<user>[-\w]+)/$',
        PostUserListView.as_view(),
        name='user'),

    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name='post'),

    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        PostDayArchiveView.as_view(),
        name='archive_day'),

    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        PostMonthArchiveView.as_view(),
        name='archive_month'),

    url(r'^posts/(?P<year>\d{4})/$',
        PostYearArchiveView.as_view(),
        name='archive_year'),

    url(r'^pages/(?P<slug>[-\w]+)/$',
        PageDetailView.as_view(),
        name='page'),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

    # Criar redirect para compatibilidade com blog antigo
)
