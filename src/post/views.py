from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import Post

class PostDetailView(DetailView):
    template_name = "home.html"
    model = Post
