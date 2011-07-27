from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from public_html.blog.models import Post, Category

class PostCategoryListView(ListView):
    template_name = 'list.html'
    paginate_by = 3

    def get_queryset(self):
        category = get_object_or_404(Category, slug__iexact=self.args[0])
        return Post.objects.filter(category=category)
