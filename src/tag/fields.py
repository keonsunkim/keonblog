from django.db import models
from django.db.models import signals

from django.contrib.postgres.fields import JSONField

from .models import Tag, PostTagRelation
from .utils import parse_tags

from .settings import *

"""
A custom TagField which works with PostgreSQL's JSONField
"""


class TagField(JSONField):

    def __init__(self, *args, **kwargs):
        self.tag_symbol = kwargs.get('tag_symbol', HASH)
        self.tag_separator = kwargs.get('tag_separator', COMMA)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['tag_symbol']
        del kwargs['tag_separator']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        self.instance



    def get_internal_type(self):
        return 'JSONField'
