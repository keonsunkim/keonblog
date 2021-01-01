from django.db import models
from django.conf import settings

from tag.fields import PostTagField
from tag.utils import post_tag_default_dict

USER = settings.AUTH_USER_MODEL

class Post(models.Model):
    ANNOUNCEMENT = 0
    ARTICLE = 1
    PROJECT = 2
    ACADEMIC = 3

    POST_CATEGORY_CHOICES = [
        (ANNOUNCEMENT, 'Announcment'),
        (ARTICLE, 'Article'),
        (PROJECT, 'Project'),
        (ACADEMIC,' Academic')
    ]

    category = models.SmallIntegerField(
            choices=POST_CATEGORY_CHOICES,
            db_index=True
            )


    author = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    theme = models.CharField(max_length=30)

    photo = models.ImageField()

    title = models.CharField(max_length=30)

    slug = models.SlugField()

    short_description = models.CharField(max_length=200)

    text = models.TextField(max_length=30)

    tags = PostTagField(
            null=True,
            blank=True,
            default = post_tag_default_dict,
    )
