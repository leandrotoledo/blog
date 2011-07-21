from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import list_detail
from public_html.blog.models import *


@csrf_protect
def post(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post.html', {'post': post,
                                         'context_instance': RequestContext(request)})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    response = list_detail.object_list(
        request,
        queryset = Post.objects.filter(category=category).order_by('-published_date'),
        paginate_by = 3,
        template_name = 'list.html'
    )

    return response
