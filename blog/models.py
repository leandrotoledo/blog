# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.contrib import admin
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.contrib.comments.signals import comment_was_posted
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator


class Category(models.Model):
    title = models.CharField(
        _('title'),
        max_length = 50,
        db_index = True)

    slug = models.SlugField(
        _('slug'),
        max_length = 50,
        db_index = True)

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        super(Category, self).save()

    @permalink
    def get_absolute_url(self):
        return ('category', [self.slug])
admin.site.register(Category)


class CommonPage(models.Model):
    title = models.CharField(
        _('title'),
        max_length = 50,
        help_text = _('Type the title here.'),
        unique = True)

    slug = models.SlugField(
        _('slug'),
        max_length = 50,
        help_text = _('Type the slug here.'),
        unique = True)

    excerpt = models.TextField(
        _('excerpt'),
        max_length = 140,
        help_text = _('Abstracts are descriptions made manually on the content.'))

    content = models.TextField(
        _('content'),
        help_text = _('HTML is allowed.'))

    created_date = models.DateTimeField(
        _('date-created'),
        auto_now_add = True)

    updated_date = models.DateTimeField(
        _('date-updated'),
        auto_now = True)

    published_date = models.DateTimeField(
        _('date-published'))

    enable_comments = models.BooleanField(
        _('enable-comments'),
        default = True)

    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(CommonPage, self).save()

    class Meta:
        abstract = True
        ordering = ['-published_date']


class Post(CommonPage):
    category = models.ManyToManyField(Category)

    @permalink
    def get_absolute_url(self):
        y = self.published_date.strftime('%Y')
        m = self.published_date.strftime('%m')
        d = self.published_date.strftime('%d')

        return ('post', None, {'year': y, 'month': m, 'day': d, 'slug': self.slug})
admin.site.register(Post)


class Page(CommonPage):
    @permalink
    def get_absolute_url(self):
        return ('page', [self.slug])
admin.site.register(Page)


class Link(models.Model):
    title = models.CharField(
        _('title'),
        max_length = 50,
        help_text = _('Type the link title here.'),
        unique = True)

    url = models.URLField(
        _('url'))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
admin.site.register(Link)
