import re
import json

from django.db import models

from .settings import (HASH, HASHVALUES, COMMA, SEPARATOR,
                        IGNORE_NON_STRINGS, FORCE_LOWER_CASE)

"""
Functions to handle tagging functionality.
string(input) -> queryset(object) -> json/dict(field)
json/dict(db) -> queryset(object) -> string(output)
"""
# re_hash_sep = re.compile(r'')
# re_hash_sep_only_str = re.compile(f"(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
re_hash_sep_only_str = re.compile(f"(?:^|\s)[＃#]{{1}}(\w+)", re.UNICODE)
re_json_string_id_slug = re.compile('{"id":[\s?]([0-9]+),[\s?]"slug":[\s?]"(\w+)"}', re.UNICODE)


def classify_tag_input(tag_data):
    if isinstance(tag_data, dict):
        return 'dict'
    elif isinstance(tag_data, models.QuerySet):
        return 'queryset'
    elif isinstance(tag_data, str):
        return 'str'
    else:
        raise ValueError(f"Wrong Data Input : {tag_data}")

def tag_str_to_list(tag_string, separator=SEPARATOR, *args):
    global re_hash_sep_only_str
    global re_json_string_id_slug

    json_id_slug_match = re_json_string_id_slug.findall(tag_string)
    if json_id_slug_match:
        id_list = [element[0] for element in json_id_slug_match]
        return ({'form' : 'id'}, id_list)
    else:
        slug_list = re_hash_sep_only_str.findall(tag_string)
        return ({'form' : 'slug'}, slug_list)

def post_tag_default_dict():
    return dict(Tag=list())

def get_value_and_return_cls_object(value, cls):
    if isinstance(value, cls):
        return value
    else:
        return cls(value)
