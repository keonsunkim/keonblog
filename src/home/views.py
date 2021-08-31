from django.shortcuts import render

from django.views.generic import TemplateView

from post.models import Post
from tag.models import PostTag


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tags = PostTag.objects.all()[:30]
        posts = Post.objects.all()[:5]
        context['tags'] = tags
        context['posts'] = posts
        return context
