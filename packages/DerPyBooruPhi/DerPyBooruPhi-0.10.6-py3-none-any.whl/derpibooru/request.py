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

from typing import Callable, Iterable, Literal
from urllib.parse import urlencode
from requests import get, post, codes
from .helpers import format_params, format_params_url_galleries, slugging_tag

__all__ = [
    "url", "request", "get_images", "get_image_data", "get_image_faves",
    "url_related", "request_related", "get_related",
    "post_image",
    "url_comments", "request_comments", "get_comments", "get_comment_data",
    "url_tags", "request_tags", "get_tags", "get_tag_data",
    "get_user_id_by_name", "get_user_data",
    "request_filters",
    "get_filters", "get_filter_data",
    "url_galleries", "request_galleries", "get_galleries",
    "request_forums", "get_forums", "get_forum_data",
    "url_topics", "request_topics", "get_topics", "get_topic_data",
    "url_search_posts",
    "url_posts", "request_posts", "get_posts", "get_post_data"
]

def request_content(
    search: str,
    p: dict,
    items_name: str,
    post_request: bool = False,
    proxies: dict[str, str]|None = None
):
    if post_request:
        response = post(search, params=p, proxies=proxies)
    else:
        response = get(search, params=p, proxies=proxies)
    if "per_page" not in p:
        p["per_page"] = 50
    while response.status_code == codes.ok:
        items: list[dict[str]] = response.json()[items_name]
        item_count = 0
        for item in items:
            yield item
            item_count += 1
        if item_count < p["per_page"]:
            break
        p["page"] += 1
        response = get(search, params=p, proxies=proxies)

def get_content(
    request_func: Callable[..., Iterable[dict[str]]],
    *request_args,
    limit: int=50,
    **request_kwargs
):
    if limit is not None:
        if limit > 0:
            response = request_func(*request_args, **request_kwargs)
            for index, content_item in enumerate(response, start=1):
                yield content_item
                if index >= limit:
                    break
    else:
        response = request_func(*request_args, **request_kwargs)
        for content_item in response:
            yield content_item

def url(params: dict, url_domain: str="https://derpibooru.org") -> str:
    p = format_params(params)
    link_url = f"{url_domain}/search?{urlencode(p)}"
    return link_url

def request(
    params: dict,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    if params.get("reverse_url", None):
        search, p = f"{url_domain}/api/v1/json/search/reverse", format_params(params)
        p = {
            i:i_value
            for i, i_value in p.items()
            if i in ('url', 'distance')
        }
        post_request = True
    else:
        search, p = f"{url_domain}/api/v1/json/search/images", format_params(params)
        p = {
            i:i_value
            for i, i_value in p.items()
            if i not in ('url', 'distance')
        }
        post_request = False
    for image in request_content(search, p, "images", post_request=post_request, proxies=proxies):
        yield image

def get_images(
    params: dict,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for image in get_content(request, params, limit=limit, url_domain=url_domain, proxies=proxies):
        yield image

def get_image_data(
    id_number: int|Literal["featured"],
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
) -> dict[str]:
    '''id_number can be "featured"'''
    link_url = f"{url_domain}/api/v1/json/images/{id_number}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data = response.json()

        if duplicate_id := data.get("image", {}).get("duplicate_of", None):
            return get_image_data(
                duplicate_id,
                url_domain=url_domain,
                proxies=proxies
            )
        return data["image"]

def get_image_faves(
    id_number: int,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/images/{id_number}/favorites"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data = response.text.rsplit('</h5>', 1)[-1].strip()
        if data.endswith('</a>'):
            data = data[:-4]
        data = data.split("</a> <")
        data = [useritem.rsplit('">', 1)[-1] for useritem in data]
        return data

def url_related(id_number: int, params: dict, url_domain: str="https://derpibooru.org") -> str:
    p = format_params(params)
    link_url = f"{url_domain}/images/{id_number}/related?{urlencode(p)}"
    return link_url

def request_related(
    id_number: int,
    params: dict,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    search, p = f"{url_domain}/images/{id_number}/related", format_params(params)
    response = get(search, params=p, proxies=proxies)

    # It should be temporary solution, until related returns to API
    if response.status_code == codes.ok:
        images = [
            f"""id:{image.split('"', 1)[0]}"""
            for image in response.text.split('<div class="media-box" data-image-id="')
        ][1:]
    params['q'] = (" || ".join(images),)
    params['sf'] = "_score"
    params['sd'] = "desc"
    search, p = f"{url_domain}/api/v1/json/search/images", format_params(params)

    for image in request_content(search, p, "images", proxies=proxies):
        yield image

def get_related(
    id_number: int,
    params: dict,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for image in get_content(
        request_related,
        id_number,
        params,
        limit=limit,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield image

def post_image(
    key: str,
    image_url: str,
    description: str = "",
    tag_input: Iterable = (),
    source_url: str = "",
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    '''
    You must provide the direct link to the image in the image_url parameter.
    Abuse of the endpoint will result in a ban.
    '''
    search = f"{url_domain}/api/v1/json/images"
    json = {
        "image": {
            "description": description,
            "tag_input": ", ".join(tag_input),
            "source_url": source_url
        },
        "url": image_url
    }
    response = post(search, params={"key": key}, json=json, proxies=proxies)
    if response.status_code == codes.ok:
        data: dict[str, dict[str]] = response.json()
        return data

def url_comments(params: dict, url_domain: str="https://derpibooru.org") -> str:
    p = format_params(params)
    p["qc"]=p["q"]
    del p["q"]
    link_url = f"{url_domain}/comments?{urlencode(p)}"
    return link_url

def request_comments(
    params: dict,
    url_domain: str="https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    search, p = f"{url_domain}/api/v1/json/search/comments", format_params(params)
    for comment in request_content(search, p, "comments", proxies=proxies):
        yield comment

def get_comments(
    params: dict,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for comment in get_content(
        request_comments,
        params,
        limit=limit,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield comment

def get_comment_data(
    id_number: int,
    url_domain: str="https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/api/v1/json/comments/{id_number}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data: dict[str, dict[str, str|int|None]] = response.json()

        return data["comment"]

def url_tags(params: dict, url_domain: str="https://derpibooru.org") -> str:
    p = format_params(params)
    p["tq"]=p["q"]
    del p["q"]
    link_url = f"{url_domain}/tags?{urlencode(p)}"
    return link_url

def request_tags(
    params: dict,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    search, p = f"{url_domain}/api/v1/json/search/tags", format_params(params)
    for tag in request_content(search, p, "tags", proxies=proxies):
        yield tag

def get_tags(
    params: dict,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for tag in get_content(
        request_tags,
        params,
        limit=limit,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield tag

def get_tag_data(
    tag: str,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/api/v1/json/tags/{tag}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data: dict[str, dict[str]] = response.json()

        return data["tag"]

def get_user_id_by_name(
    username: str,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/profiles/{slugging_tag(username)}"

    response = get(link_url, proxies=proxies)

    profile_data = response.text
    user_id = profile_data.split("/conversations?with=", 1)[-1].split('">', 1)[0]
    return int(user_id)

def get_user_data(
    user_id: int,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/api/v1/json/profiles/{user_id}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data: dict[str, dict[str]] = response.json()

        return data["user"]

def request_filters(
    filter_id: int|Literal["system", "user"],
    params: dict,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    '''filter_id can be "system"'''
    search, p = f"{url_domain}/api/v1/json/filters/{filter_id}", format_params(params)
    for filter_item in request_content(search, p, "filters", proxies=proxies):
        yield filter_item

def get_filters(
    filter_id: int|Literal["system", "user"],
    params: dict,
    url_domain: str = "https://derpibooru.org",
    limit: int = 50,
    proxies: dict[str, str]|None = None
):
    for filter_item in get_content(
        request_filters,
        filter_id,
        params,
        limit=limit,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield filter_item

def get_filter_data(
    filter_id: int|Literal["system", "user"],
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/api/v1/json/filters/{filter_id}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data: dict[str, dict[str]] = response.json()

        return data["filter"]

def url_galleries(params: dict, url_domain: str="https://derpibooru.org") -> str:
    p = format_params_url_galleries(params)
    link_url = f"{url_domain}/galleries?{urlencode(p)}"
    return link_url

def request_galleries(
    params: dict,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    search, p = f"{url_domain}/api/v1/json/search/galleries", format_params(params)
    for gallery in request_content(search, p, "galleries", proxies=proxies):
        yield gallery

def get_galleries(
    params: dict,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for gallery in get_content(
        request_galleries,
        params,
        limit=limit,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield gallery

def request_forums(
    params: dict,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    search, p = f"{url_domain}/api/v1/json/forums", format_params(params)
    for forum in request_content(search, p, "forums", proxies=proxies):
        yield forum

def get_forums(
    params: dict,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for forum in get_content(
        request_forums,
        params,
        limit=limit,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield forum

def get_forum_data(
    short_name: str,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/api/v1/json/forums/{short_name}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data: dict[str, dict[str, str|int]] = response.json()
        return data["forum"]

def url_topics(
    forum_short_name: str,
    params: dict,
    url_domain: str = "https://derpibooru.org"
) -> str:
    p = format_params(params)
    link_url = f"{url_domain}/forums/{forum_short_name}?{urlencode(p)}"
    return link_url

def request_topics(
    forum_short_name: str,
    params: dict,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    search, p = f"{url_domain}/api/v1/json/forums/{forum_short_name}/topics", format_params(params)
    for topic in request_content(search, p, "topics", proxies=proxies):
        yield topic

def get_topics(
    forum_short_name: str,
    params: dict,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for topic in get_content(
        request_topics,
        forum_short_name,
        params,
        limit=limit,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield topic

def get_topic_data(
    forum_short_name: str,
    topic_slug: str,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/api/v1/json/forums/{forum_short_name}/topics/{topic_slug}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data: dict[str, dict[str, str|int|bool]] = response.json()
        return data["topic"]

def url_search_posts(params: dict, url_domain: str="https://derpibooru.org") -> str:
    p = format_params(params)
    link_url = f"{url_domain}/posts?{urlencode(p)}"
    return link_url

def url_posts(
    forum_short_name: str,
    topic_slug: str,
    params: dict,
    url_domain: str = "https://derpibooru.org"
) -> str:
    p = format_params(params)
    api_page: int = p['page']
    api_per_page: int = p['per_page']
    web_per_page = 25
    api_last_post_on_page = api_page * api_per_page
    api_first_post_on_page = api_last_post_on_page - api_per_page + 1
    p['page'] = (api_first_post_on_page + web_per_page - 1) // web_per_page
    del p['per_page']
    link_url = f"{url_domain}/forums/{forum_short_name}/topics/{topic_slug}?{urlencode(p)}"
    return link_url

def request_posts(
    params: dict,
    forum_short_name: str|None = None,
    topic_slug: str|None = None,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    if forum_short_name and topic_slug:
        search = f"{url_domain}/api/v1/json/forums/{forum_short_name}/topics/{topic_slug}/posts"
        p = format_params(params)
    else:
        search = f"{url_domain}/api/v1/json/search/posts"
        p = format_params(params)
    for requested_post in request_content(search, p, "posts", proxies=proxies):
        yield requested_post

def get_posts(
    params: dict,
    forum_short_name: str|None = None,
    topic_slug: str|None = None,
    limit: int = 50,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    for requested_post in get_content(
        request_posts,
        params,
        limit=limit,
        forum_short_name=forum_short_name,
        topic_slug=topic_slug,
        url_domain=url_domain,
        proxies=proxies
    ):
        yield requested_post

def get_post_data(
    id_number: int,
    url_domain: str = "https://derpibooru.org",
    proxies: dict[str, str]|None = None
):
    link_url = f"{url_domain}/api/v1/json/posts/{id_number}"

    response = get(link_url, proxies=proxies)

    if response.status_code == codes.ok:
        data: dict[str, dict[str, str|int]] = response.json()
        return data["post"]
