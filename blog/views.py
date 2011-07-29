from django.shortcuts import get_object_or_404
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.models import User
from public_html.blog.models import *


class PostListView(ListView):
    """
    Index
    """

    template_name = 'list.html'
    paginate_by = 3
    model = Post


class PostDetailView(DetailView):
    """
    Post
    """

    context_object_name = 'post'
    template_name = 'post.html'
    model = Post


class PostCategoryListView(ListView):
    """
    Category
    """

    template_name = 'list.html'
    paginate_by = 3

    def get_queryset(self):
        category = get_object_or_404(Category, slug__iexact = self.kwargs['category'])
        return Post.objects.filter(category = category)

    def render_to_response(self, context):
        messages.info(self.request, _('Category: <strong>%s</strong>' % self.kwargs['category']))
        return super(PostCategoryListView, self).render_to_response(context)


class PostUserListView(ListView):
    """
    User
    """

    template_name = 'list.html'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username__iexact = self.kwargs['user'])
        return Post.objects.filter(user = user)

    def render_to_response(self, context):
        messages.info(self.request, _('User: <strong>%s</strong>' % self.kwargs['user']))
        return super(PostUserListView, self).render_to_response(context)


class PostDayArchiveView(DayArchiveView):
    """
    Archive Day
    """

    template_name = 'list.html'
    month_format = '%m'
    date_field = 'published_date'
    model = Post

    def render_to_response(self, context):
        messages.info(self.request, _('Day: <strong>%s/%s/%s</strong>' % (self.kwargs['day'], self.kwargs['month'], self.kwargs['year'])))
        return super(PostDayArchiveView, self).render_to_response(context)


class PostMonthArchiveView(MonthArchiveView):
    """
    Archive Month
    """

    template_name = 'list.html'
    month_format = '%m'
    date_field = 'published_date'
    model = Post

    def render_to_response(self, context):
        messages.info(self.request, _('Month: <strong>%s/%s</strong>' % (self.kwargs['month'], self.kwargs['year'])))
        return super(PostMonthArchiveView, self).render_to_response(context)


class PostYearArchiveView(YearArchiveView):
    """
    Archive Year
    """

    make_object_list = True
    template_name = 'list.html'
    date_field = 'published_date'
    model = Post

    def render_to_response(self, context):
        messages.info(self.request, _('Year: <strong>%s</strong>' % self.kwargs['year']))
        return super(PostYearArchiveView, self).render_to_response(context)
