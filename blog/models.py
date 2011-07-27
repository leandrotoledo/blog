from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

from django.contrib import admin
from django.utils.translation import gettext as _

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

    category = models.ManyToManyField('blog.Category')

    def __unicode__(self):
        return self.title

    def save(self):
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


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')

    search_fields = ['title']

    date_hierarchy = 'published_date'

    fieldsets = [
        (None, {'fields':   ['title'],
                'classes':  ['wide']}),

        (None, {'fields':   ['content'],
                'classes':  ['wide']}),

        (_('publish'), {'fields':   ['published_date'],
                        'classes':  ['collapse', 'wide']}),

        (_('excerpt'), {'fields':   ['excerpt'],
                        'classes':  ['collapse', 'wide']}),

        (_('category'), {'fields':  ['category'],
                        'classes':  ['collapse', 'wide']})
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
