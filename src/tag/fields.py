from django.apps import apps
from django.db import models
from django.db.models import signals

from django.contrib.postgres.fields import JSONField

from .models import PostTagModelQuerysetHandler
from .forms import TagField as TagFormField

from django.db.models import signals

from .settings import (HASH, HASHVALUES, COMMA, SEPARATOR,
                        IGNORE_NON_STRINGS, FORCE_LOWER_CASE)

"""
A custom TagField which works with PostgreSQL's JSONField
Due to the use of bulk_create and JSONField, it must be used with PostgreSQL
"""

class PostTagField(JSONField):
    """
    JSONField which saves tag information.
    Format looks like the following:
    {"Tags" : [{"id" : 5, "slug" : sociology"}, {"id" : 2, "slug" : "computer", }...]}

    This also saves tag relationship into designated through table.

    Field's clean() \ validate() ->  Form's clean() is run.
    Make sure form's clean() method does not revert value back to Queryset Object!
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    # def contribute_to_class(self, cls, name):
    #     super(PostTagField, self).contribute_to_class(cls, name)
    #     signals.post_save.connect(self._save, cls, True)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return PostTagModelQuerysetHandler(value)

    def to_python(self, value):
        if isinstance(value, PostTagModelQuerysetHandler):
            return value
        if value is None:
            return value
        return PostTagModelQuerysetHandler(value)

    # def to_db_prep_value(self, value, expression, connection):

    def validate(self, value, model_instance):
        if isinstance(value, PostTagModelQuerysetHandler):
            #This should be running if the form's clean method is properly working.
            pass
        elif value is None:
            pass
        elif isinstance(value, str):
            value = PostTagModelQuerysetHandler(value)
        else:
            raise ValueError(f"This theoretically should never happen : value :{value}")
        super().validate(value, model_instance)
        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': TagFormField,
            'initial':''
        }
        defaults.update(kwargs)
        return super(PostTagField, self).formfield(**defaults)
