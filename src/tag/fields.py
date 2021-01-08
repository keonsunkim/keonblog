from django.apps import apps
from django.db import models
from django.db.models import signals

from django.contrib.postgres.fields import JSONField

from .models import PostTagModelQuerysetHandler
from .forms import TagField as TagFormField

from django.db.models import signals

from .utils import get_value_and_return_cls_object
from .settings import (HASH, HASHVALUES, COMMA, SEPARATOR,
                        IGNORE_NON_STRINGS, FORCE_LOWER_CASE)

from .models import PostTag, PostTagRelation

"""
A custom TagField which works with PostgreSQL's JSONField
Due to the use of bulk_create and JSONField, it must be used with PostgreSQL
"""

class TagField(JSONField):
    """
    Base TagField Class so that multiple types of TagFields can be easily
    created.

    I personally don't like using the GenericForeignKey of Django, so I decided
    enabling easy creation of multiple Tag / TagRelaion models and creating TagFields
    specifically corresponding to the following.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name):
        super(TagField, self).contribute_to_class(cls, name)
        # Save tags back to the database post-save
        signals.post_save.connect(self._tagrelation_save, cls, True)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': TagFormField,
            'initial':''
        }
        defaults.update(kwargs)
        return super(TagField, self).formfield(**defaults)

class PostTagField(TagField):
    """
    JSONField which saves tag information.
    Format looks like the following:
    {"Tags" : [{"id" : 5, "slug" : sociology"}, {"id" : 2, "slug" : "computer", }...]}

    This also saves tag relationship into designated through table.

    Field's clean() \ validate() ->  Form's clean() is run.
    #https://docs.djangoproject.com/en/2.2/_modules/django/db/models/fields/

    Make sure form's clean() method does not revert value back to Queryset Object!
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return PostTagModelQuerysetHandler(value)

    def to_python(self, value):
        value = get_value_and_return_cls_object(
                value,
                PostTagModelQuerysetHandler
                )
        return value.dictify()

    def _tagrelation_save(self, **kwargs):
        #update tag relations
        PostTagRelation.objects.update_tags(kwargs.get("instance"))
        #update tag counts
        PostTag.objects.update_tag_count()
