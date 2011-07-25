from public_html.blog.models import *
from django.db import connections
from django.db.models import Count

from datetime import datetime


def archives(request):
    archives = Post.objects.extra(select={'month': connections[Post.objects.db].ops.date_trunc_sql('month', 'published_date')}).values('month').annotate(dcount=Count('published_date'))

    for archive in archives:
        archive['month'] = datetime.strptime(archive['month'][:10], '%Y-%m-%d')

    return {'archives': archives}


def categories(request):
    return {'categories': Category.objects.annotate(Count('post')).order_by('title')}

