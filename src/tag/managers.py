from django.db import models

from post.models import Post

class PostTagManager(models.Manager):

    def set_tags(self, tag_list):
        return
