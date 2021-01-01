from django.db import models
from django.conf import settings

from .managers import TagManager
from .utils import (
    classify_tag_input, tag_str_to_list, tag_data_lowercase
    )

from .settings import (HASH, HASHVALUES, COMMA, SEPARATOR,
                        IGNORE_NON_STRINGS, FORCE_LOWER_CASE)


USER = settings.AUTH_USER_MODEL

class PostTagModelQuerysetHandler:
    """
    A ListClass that treats multiple Tag Model instances.
    This Class allows the new TagField to parse through tags like
    a CharField, although being a JSON Field.
    Also, it does the saving and updates on the Through Model for the Tag
    objects.
    """

    def __init__(self, tag_data, *args, **kwargs):
        self.separator = SEPARATOR
        self.handle_input_func_dict = {
            'str' : self.tag_str_to_queryset,
            'queryset' : lambda a, *args : a,
            'dict' : self.tag_dict_to_queryset,
        }
        self.tag_queryset = self._get_tag_queryset_(tag_data)

    def __repr__(self):
        return self.stringify()

    def __str__(self):
        return self.stringify()

    def _get_tag_queryset_(self, tag_data):
        qs = self.handle_input_func_dict.get(
                classify_tag_input(tag_data_lowercase(tag_data))
             )(tag_data)
        print(qs)
        return qs

    def tag_dict_to_queryset(self, tag_dict, *args):
        return PostTag.objects.qs_get_from_ids(
                    [tag['id'] for tag in tag_dict['Tag']]
                )

    def tag_str_to_queryset(self, tag_string, *args):
        tag_slug = tag_str_to_list(tag_string, self.separator)
        return PostTag.objects.qs_get_or_create_from_slugs(tag_slug)

    def stringify(self):
        tag_string = ' '.join(
                    [HASH + obj.slug + self.separator for obj in self.tag_queryset]
                    )
        return tag_string

    def dictify(self):
        tag_dict = {'Tag' : []}
        for tag_obj in self.tag_queryset:
            tag_dict['Tag'].append({'id' : tag_obj.id, 'slug' : tag_obj.slug})
        return tag_dict


class PostTag(models.Model):
    slug = models.CharField(
                            unique=True,
                            max_length=100,
                            db_index=True
                            )

    count = models.SmallIntegerField(default=0)

    objects = TagManager()

    def __repr__(self):
        return f"{self.slug}({self.count})"


class PostTagRelation(models.Model):
    tag = models.ForeignKey(
                            'tag.PostTag',
                            on_delete=models.CASCADE,
                            db_index=True
                            )
    post = models.ForeignKey(
                            'post.Post',
                            on_delete=models.CASCADE,
                            db_index=True
                            )

    # objects = PostTagRelManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                    fields=['tag', 'post'],
                    name='unique_post_tag'
            ),
        ]

    def __str__(self):
        return f"{self.tag} -> {self.post}"
