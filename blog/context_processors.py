from django.db.models import Count

from public_html.blog.models import Post, Category

def archives(request):
    return {'archives': Post.objects.filter().dates('published_date', 'month')}

def categories(request):
    return {'categories': Category.objects.annotate(Count('post')).order_by('title')}

