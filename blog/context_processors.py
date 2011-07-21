from public_html.blog.models import *
from django.db.models import Count

def categories(request):
    return {'categories': Category.objects.annotate(Count('post')).order_by('title')}

def user(request):
    return {'user': request.user}

