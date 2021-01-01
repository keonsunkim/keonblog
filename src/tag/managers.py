from django.db import models
from django.db.models import Q

class TagManager(models.Manager):

    def qs_get_from_ids(self, tag_ids_list):
        tag_filters = Q()
        for id in tag_ids_list:
            tag_filters |= Q(id=id)
        qs = self.filter(tag_filters)
        return qs

    def qs_get_from_slugs(self, tag_slugs_list):
        tag_filters = Q()
        for slug in tag_slugs_list:
            tag_filters |= Q(slug__iexact=slug)
        qs = self.filter(tag_filters)
        return qs

    def qs_get_or_create_from_slugs(self, tag_slugs_list):
        for slug in tag_slugs_list:
            obj, created = self.get_or_create(slug=slug)
        qs = self.qs_get_from_slugs(tag_slugs_list)
        return qs

    def update_tag_count(self):
        qs_tag_count = self.filter(OuterRef='pk').annotate(tag_counts=Count('post'))
        self.update(count=Subquery(qs_tag_count).values('tag_counts'))


# class TagRelationManager(models.Manager):
