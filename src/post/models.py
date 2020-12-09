from django.db import models
from django.conf import settings

USER = settings.AUTH_USER_MODEL

class Post(models.Model):
    author = models.ForeignKey(
        USER,
        on_delete = models.SET_NULL,
        null = True,
        blank= True
    )

    created_at = models.DateTimeField(auto_now_add = True)
    edited_at = models.DateTimeField(auto_now = True)

    theme = models.CharField(max_length=30)

    photo = models.ImageField()

    title = models.CharField(max_length=30)

    slug = models.SlugField()

    short_description = models.CharField(max_length=200)

    text = models.TextField(max_length=30)

    # tags = models.TagField()
