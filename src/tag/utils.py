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
re_hash_sep_only_str = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)


def tag_data_lowercase(tag_data, *args):
    if FORCE_LOWER_CASE:
        if isinstance(tag_data, str):
            tag_data = tag_data.lower()
        elif isinstance(tag_data, dict):
            for tag_dict in tag_data['Tag']:
                tag_dict['slug'] = str(tag_dict['slug']).lower()
        else:
            pass
    return tag_data

def classify_tag_input(tag_data):
    if isinstance(tag_data, dict):
        return 'dict'
    elif isinstance(tag_data, str):
        return 'str'
    elif isinstance(tag_data, models.QuerySet):
        return 'queryset'
    else:
        raise ValueError(f"Wrong Data Input : {tag_data}")


def tag_str_to_list(tag_string, separator, *args):
    global re_hash_sep_only_str
    re_hash_sep_only_str = re.compile(
                                f"(?:^|\s)[＃#]{{1}}(\w+)(?:{separator})",
                                re.UNICODE
                                )
    tag_list_without_hash = re_hash_sep_only_str.findall(tag_string)
    return tag_list_without_hash

def post_tag_default_dict():
    return dict(Tag=list())
