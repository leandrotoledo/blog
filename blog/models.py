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


class Post(models.Model):
    title = models.CharField(
        _('title'),
        max_length = 255,
        help_text = _('Type the title here.'),
        unique = True)

    slug = models.SlugField(
        _('slug'),
        max_length = 100,
        help_text = _('Type the slug here.'),
        unique = True)

    excerpt = models.TextField(
        _('excerpt'),
        help_text = _('Abstracts are descriptions made manually on the content of your post.'))

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

    category = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save()

    @permalink
    def get_absolute_url(self):
        y = self.published_date.strftime('%Y')
        m = self.published_date.strftime('%m')
        d = self.published_date.strftime('%d')

        return ('post', None, {'year': y, 'month': m, 'day': d, 'slug': self.slug})

    class Meta:
        ordering = ['-published_date']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'user')

    search_fields = ['title']

    date_hierarchy = 'published_date'

    fieldsets = [
        (None, {'fields':   ['title'],
                'classes':  ['wide']}),

        (None, {'fields':   ['content'],
                'classes':  ['wide']}),

        (_('publish'), {'fields':   ['published_date', 'enable_comments'],
                        'classes':  ['collapse', 'wide']}),

        (_('excerpt'), {'fields':   ['excerpt'],
                        'classes':  ['collapse', 'wide']}),

        (_('category'), {'fields':  ['category'],
                        'classes':  ['collapse', 'wide']})
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
admin.site.register(Post, PostAdmin)

"""
class PostModerator(CommentModerator):
    email_notification = True
    #TODO: https://docs.djangoproject.com/en/dev/ref/contrib/comments/moderation/
    enable_field = 'enable_comments'
moderator.register(Post, PostModerator)


def comment_notification(sender, comment, request, **kwargs):
    post = Post.objects.get(pk=request.REQUEST['object_pk'])

    subject = u'[Blog do Leandro Toledo] Comentário: "%s"' % post
    author = _('Author: %s (IP: %s)' % (comment.user_name, comment.ip_address))
    email = _('E-mail: %s' % comment.user_email)
    url = _('URL: %s' % comment.user_url)

    content = _('New comment on post "%s"\n%s\n%s\n%s\n\n%s' % (post, author, email, url, comment.comment))

    send_mail(subject, content, 'blog@leandrotoledo.com.br', ['leandrotoledodesouza@gmail.com'])
comment_was_posted.connect(comment_notification)
"""
