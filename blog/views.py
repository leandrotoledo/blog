from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_protect

from public_html.blog.models import *


def index(request, year=None, month=None, day=None):
    if year and month and day:
        posts = Post.objects.filter(published_date__year=year, published_date__month=month, published_date__day=day)
        description = _('Archive of day: %(day)s/%(month)s/%(year)s.') % {'day': day, 'month': month, 'year': year}
    elif year and month:
        posts = Post.objects.filter(published_date__year=year, published_date__month=month)
        description = _('Archive of month: %(month)s/%(year)s.') % {'month': month, 'year': year}
    elif year:
        posts = Post.objects.filter(published_date__year=year)
        description = _('Archive of year: %(year)s.') % {'year': year}
    else:
        posts = Post.objects.all()
        description = None

    posts = posts.order_by('-published_date')
    categories = Category.objects.all()

    return render(request, 'list.html', {'posts':            paginate(request, posts),
                                         'description':      description,
                                         'categories':       categories,
                                         'user':             request.user})


@csrf_protect
def post(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug)
    categories = Category.objects.all()

    return render(request, 'post.html', {'post':             post,
                                         'user':             request.user,
                                         'categories':       categories,
                                         'context_instance': RequestContext(request)})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    description = _('Archive of category: %(category)s.') % {'category': category}

    posts = Post.objects.filter(category=category).order_by('-published_date')
    categories = Category.objects.all()

    return render(request, 'list.html', {'posts':            paginate(request, posts, 5),
                                         'description':      description,
                                         'categories':       categories,
                                         'user':             request.user})


def paginate(request, posts, posts_per_page=3):
    paginator = Paginator(posts, posts_per_page)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts
