import ast
import json

from django.db import models
from django.conf import settings

from django.db.models import Q

from .utils import (
    classify_tag_input, tag_str_to_list, 
    )

from .settings import (HASH, HASHVALUES, COMMA, SEPARATOR,
                        IGNORE_NON_STRINGS, FORCE_LOWER_CASE)


class TagManager(models.Manager):

    def qs_get_from_ids(self, tag_ids_list):
        if not tag_ids_list:
            return self.none()  

        tag_filters = Q()
        for id in tag_ids_list:
            tag_filters |= Q(id=id)
        qs = self.filter(tag_filters)
        return qs

    def qs_get_from_slugs(self, tag_slugs_list):
        if not tag_slugs_list:
            return self.none()  

        tag_filters = Q()
        for slug in tag_slugs_list:
            tag_filters |= Q(slug__iexact=slug)
        qs = self.filter(tag_filters)
        return qs

    def qs_get_or_create_from_slugs(self, tag_slugs_list):
        if not tag_slugs_list:
            return self.none()

        for slug in tag_slugs_list:
            obj, created = self.get_or_create(slug=slug)
        qs = self.qs_get_from_slugs(tag_slugs_list)
        return qs



class PostTagManager(TagManager):

    def update_tag_count(self):
        """
        This needs explanation and improvements.
        """
        #create subquery to update matching values
        qs_tag_count = self.filter(
                id=models.OuterRef('id')
            ).annotate(
                tag_counts=models.Count('posttagrelation__tag')
            ).values('tag_counts')[:1]
        #update tag counts from subquery
        self.update(count=models.Subquery(qs_tag_count))

class PostTagRelManager(models.Manager):

    def update_tags(self, instance):
        #generate queryset of tag relations of instance
        qs_tags_of_instance = self.filter(post__id=instance.pk)

        #get ids of tags of instance
        current_tag_ids = set(list(
            qs_tags_of_instance.values_list('tag',flat=True)
        ))

        if isinstance(instance.tags, str):
            tag_ids_from_instance = set([tag.id for tag in PostTag.objects.qs_get_from_slugs(instance.tags)])
        else: 
            tag_ids_from_instance = set([tag_dict['id'] for tag_dict in instance.tags['Tag']])

        #find ids of tags that needs to be added and deleted
        tag_ids_to_add = tag_ids_from_instance.difference(current_tag_ids)
        tags_ids_to_delete = current_tag_ids.difference(tag_ids_from_instance)

        #delete obsolete tag relationships
        self.filter(tag__id__in=tags_ids_to_delete).delete()

        #add new tag relationships
        for tag_id in tag_ids_to_add:
            tag, created = PostTag.objects.get_or_create(id=tag_id)
            self.create(post_id=instance.pk, tag=tag)


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
                classify_tag_input(tag_data)
             )(tag_data)
        return qs

    def tag_dict_to_queryset(self, tag_dict, *args):
        return PostTag.objects.qs_get_from_ids(
                    [tag['id'] for tag in tag_dict['Tag']]
                )

    def tag_str_to_queryset(self, tag_string, *args):
        if FORCE_LOWER_CASE:
            tag_string = tag_string.lower()
        form_dict, tag_list = tag_str_to_list(tag_string)

        if form_dict.get('form') == 'id':
            return PostTag.objects.qs_get_from_ids(tag_list)
        elif form_dict.get('form') == 'slug':
            return PostTag.objects.qs_get_or_create_from_slugs(tag_list)

    def stringify(self):
        tag_string = ' '.join(
                    [HASH + obj.slug for obj in self.tag_queryset]
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

    objects = PostTagManager()

    def __str__(self):
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

    objects = PostTagRelManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                    fields=['tag', 'post'],
                    name='unique_post_tag'
            ),
        ]

    def __str__(self):
        return f"{self.tag} -> {self.post}"
