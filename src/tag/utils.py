import re

"""
Functions to handle tagging functionality.
"""
# re_hash_sep = re.compile(r'')
re_hash_sep_only_str = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)



def parse_tags_str_to_list(string ,separator, force_lower_case):
    global re_hash_sep_only_str

    re_hash_sep_only_str = re.compile(
                                f"(?:^|\s)[＃#]{{1}}(\w+)(?:{separator})",
                                re.UNICODE
                                )
    if force_lower_case:
        string = string.lower()
    tag_list_without_hash = re_hash_sep_only_str.findall(string)
    return tag_list_without_hash





def parse_list_to_tags_str(list ,separator, force_lower_case):
    if force_lower_case:
        list = [''.join(['#', tag.lower(), separator]) for tag in list]
    string = ' '.join(list)
    return string
