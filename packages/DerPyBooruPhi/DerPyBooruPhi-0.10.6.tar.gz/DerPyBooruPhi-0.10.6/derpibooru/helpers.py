# -*- coding: utf-8 -*-

# Copyright (c) 2014, Joshua Stone
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from numbers import Real
from typing import Iterable
from urllib.parse import quote_plus

__all__ = [
    "tags",
    "search_comments_fields",
    "api_key",
    "validate_filter",
    "validate_url",
    "validate_description",
    "sort_format",
    "user_option",
    "format_params",
    "join_params",
    "set_limit",
    "set_distance",
    "slugging_tag",
    "destructive_slug"
]

from .sort import sort
from .user import user

def tags(q: str|Iterable[str]|None) -> set[str]:
    if not q:
        return set()

    if isinstance(q, str):
        q = q.split(',')
    tags_list = {f'{tag}'.strip() for tag in q if tag}

    return tags_list if tags_list else set()

def search_comments_fields(
    q: str|Iterable[str]|None,
    author: str|None = None,
    body: str|Iterable[str]|None = None,
    created_at: str|None = None,
    comment_id: int|None = None,
    image_id: int|None = None,
    my: bool|None = None,
    user_id: int|None = None
) -> set[str]:
    if not q:
        q = []
    if isinstance(q, str):
        q = q.split(',')

    if isinstance(body, str):
        if body:
            query_words = body.split(',')
        else:
            query_words = []
    elif isinstance(body, Iterable):
        query_words = list(body)
    else:
        query_words = []

    for query_word in q:
        if query_word:
            query_word = f"{query_word}".strip()
            if query_word.startswith("author:"):
                if not author:
                    author = query_word.replace("author:", "", 1)
            elif query_word.startswith("created_at:"):
                if not created_at:
                    created_at = query_word.replace("created_at:", "", 1)
            elif query_word.startswith("comment_id:"):
                if not comment_id:
                    comment_id = int(query_word.replace("comment_id:", "", 1))
            elif query_word.startswith("image_id:"):
                if not image_id:
                    image_id = int(query_word.replace("image_id:", "", 1))
            elif query_word.startswith("user_id:"):
                if not user_id:
                    user_id = int(query_word.replace("user_id:", "", 1))
            elif query_word.startswith("-my:"): # -my:comments
                if my is None:
                    if query_word == "-my:comments":
                        my = False
            elif query_word.startswith("my:"): # my:comments
                if not my:
                    if query_word == "my:comments":
                        my = True
            else:
                query_words.append(query_word)

    if author:
        query_words.append(f"author:{author}")
    if created_at:
        query_words.append(f"created_at:{created_at}")
    if comment_id:
        query_words.append(f"id:{comment_id}")
    if image_id:
        query_words.append(f"image_id:{image_id}")
    if user_id:
        query_words.append(f"user_id:{user_id}")
    if my is not None:
        if my:
            query_words.append("my:comments")
        else:
            query_words.append("-my:comments")

    query_words = set(query_words)

    return query_words if query_words else set()

def api_key(key: str|None) -> str:
    return f"{key}" if key else ""

def validate_filter(filter_id: int|None) -> str|None:
    # is it always an number?
    return f"{filter_id}" if filter_id else None

def validate_url(url: str|None) -> str:
    if url:
        norm_url = f"{url}".strip().strip('/')
        if any(norm_url.startswith(scheme) for scheme in ("http://", "https://")):
            return norm_url
        if "://" in norm_url:
            return ""
        return f"http://{norm_url}"
    return ""

def validate_description(string: str|None) -> str:
    if not string:
        return ""

    byte_lenght=50000
    if len(string.encode('utf-8'))<byte_lenght:
        return string
    while True:
        try:
            cutted_string = string.encode('utf-8')[:byte_lenght].decode('utf-8')
            return cutted_string
        except UnicodeDecodeError:
            byte_lenght -= 1

def sort_format(sf: str):
    if sf not in sort.methods and not sf.startswith("gallery_id:"):
        raise AttributeError(sf)
    return sf

def user_option(option: str):
    if option:
        if option not in user.options():
            raise AttributeError(option)
        return option
    return ""

def format_params(params: dict):
    formatted_params = {}

    for key, value in params.items():
        if key == "q":
            formatted_params["q"] = ",".join(value) if value else "*"
        elif key == "reverse_url" and value:
            formatted_params["url"] = value
        elif key == "distance":
            if params.get("reverse_url", None):
                formatted_params[key] = value
        elif value:
            formatted_params[key] = value

    return formatted_params

def format_params_url_galleries(params: dict):
    formatted_params = {}

    for key, value in params.items():
        if key == "q":
            q = ",".join(value) if value else "*"
            q = (i.strip() for i in q.split(","))
            for tag in q:
                if tag.startswith("title:"):
                    formatted_params["gallery[title]"] = tag[6:]
                elif tag.startswith("description:"):
                    formatted_params["gallery[description]"] = tag[12:]
                elif tag.startswith("user:"):
                    formatted_params["gallery[creator]"] = tag[5:]
                elif tag.startswith("image_ids:"):
                    formatted_params["gallery[include_image]"] = tag[10:]
        elif value:
            formatted_params[key] = value

    return formatted_params

def join_params(old_params: dict, new_params: dict):
    new_dict = {**old_params, **new_params}

    return new_dict

def norm_query_list(query_list: Iterable[str|Iterable[str]]) -> set[str]:
    query_list_temp = []
    for q_item in query_list:
        if isinstance(q_item, str):
            query_list_temp.append(q_item)
        else:
            query_list_temp.extend(q_item)
    query_list = set(query_list_temp)
    return query_list

def set_limit(limit: Real|str):

    if limit is not None:
        formatted_limit = int(limit)
    else:
        formatted_limit = None

    return formatted_limit

def set_distance(distance: Real|str):
    if distance:
        try:
            distance: float = float(distance)
            if distance < 0.2:
                distance = 0.2
            elif distance >= 1:
                distance = 0.5
        except (ValueError, TypeError):
            distance = 0.25
    else:
        distance = 0.25
    return distance

def slugging_tag(tag: str) -> str:
    slug = tag.strip().lower()
    slugging_dict = {
        '-':'-dash-',
        '/':'-fwslash-',
        '\\':'-bwslash-',
        ':':'-colon-',
        '.':'-dot-',
        '+':'-plus-'
    }
    special_chars = '/\\:.+ '
    # slugging if tag has special_chars or hasn't slugging_dict values
    if (
        any(True for char in slug if char in special_chars)
        or (
            '-' in slug
            and not any(True for char in slug if char in slugging_dict.values())
        )
    ):
        for i, j in slugging_dict.items():
            slug = slug.replace(i, j)
        slug = quote_plus(slug)
    return slug

def destructive_slug(string: str) -> str:
    string = string.lower()
    for char in set(string):
        if (
            not char.isascii()
            or ord(char) not in range(ord(" "), ord("~"))
            or char=="'"
        ):
            string = string.replace(char, "")
        elif not char.isalnum():
            string = string.replace(char, "-")
    while "--" in string:
        string = string.replace("--", "-")
    string = string.strip("-")
    return string

def url_abs(url_domain: str, url: str) -> str:
    if url.startswith('//'):
        return f"https:{url}"
    if url.startswith('/'):
        return f"{url_domain}{url}"
    return url
