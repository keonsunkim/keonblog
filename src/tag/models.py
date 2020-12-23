from django.db import models
from django.conf import settings

from post.models import Post

from .managers import PostTagManager

USER = settings.AUTH_USER_MODEL


class Tag(models.Model):
    slug = models.CharField(
                            max_length=100,
                            primary_key=True,
                            db_index=True
                            )

    # objects = TagManager()

    def __str__(self):
        return self.slug


class PostTagRelation(models.Model):
    tag = models.ForeignKey(
                            Tag,
                            on_delete=models.CASCADE,
                            db_index=True
                            )
    post = models.ForeignKey(
                            Post,
                            on_delete=models.CASCADE,
                            db_index=True
                            )

    objects = PostTagManager()

    def __str__(self):
        return f"{self.tag} -> {self.post}"
