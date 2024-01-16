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

from typing import Literal
from .request import get_image_data, get_image_faves, request as request_image
from .comments import Comments
from .tags import Tags
from .filters import system_filters
from .helpers import api_key, url_abs

__all__ = [
    "Image"
]

class Image:
    """
    This class provides a thin wrapper around JSON data, mapping each value to
    its own property. Once instantiated the data is immutable so as to reflect
    the stateless nature of a REST API.
    For getting image by id field data should be None and image_id contains id.
    For getting current featured image field data should be None and image_id="featured"
    API key need for checking my:***
    """
    def __init__(
        self,
        data: dict[str]|None,
        image_id: int|Literal['featured']|None = None,
        key: str|None = None,
        search_params: dict[str]|None = None,
        url_domain: str = "https://derpibooru.org",
        proxies: dict[str, str]|None = None
    ):
        if not search_params:
            search_params = {}

        self.proxies = proxies
        self.url_domain = url_domain
        # key needed for checking my:***
        if key:
            self.key = api_key(key) if key else search_params['key']
        else:
            self.key = api_key(search_params.get('key', ''))
        self._params = search_params

        # Set image_id="featured" for get current featured image
        if data is None and image_id is not None:
            self._data = data = get_image_data(image_id, url_domain=url_domain, proxies=proxies)
        else:
            self._data = data

        for field, body in data.items():
            if not hasattr(self, field):
                setattr(self, field, body)

    def __str__(self):
        return f"Image({self.id})"

    @property
    def tags(self) -> list[str]:
        return self.data.get("tags", [])

    @property
    def representations(self) -> dict[str, str]:
        sizes: dict[str, str] = self.data.get("representations", {})
        images = { image: url_abs(self.url_domain, url) for image, url in sizes.items() }

        return images

    @property
    def full(self) -> str:
        return self.representations.get("full", "")

    @property
    def large(self) -> str:
        return self.representations.get("large", "")

    @property
    def medium(self) -> str:
        return self.representations.get("medium", "")

    @property
    def small(self) -> str:
        return self.representations.get("small", "")

    @property
    def tall(self) -> str:
        return self.representations.get("tall", "")

    @property
    def thumb(self) -> str:
        return self.representations.get("thumb", "")

    @property
    def thumb_small(self) -> str:
        return self.representations.get("thumb_small", "")

    @property
    def thumb_tiny(self) -> str:
        return self.representations.get("thumb_tiny", "")

    @property
    def image(self) -> str:
        return url_abs(self.url_domain, self.data.get("view_url", ""))

    @property
    def faved_by(self):
        faved_by = "favourited_by_users"

        if not faved_by in self.data:
            if self.faves > 0:
                self._data[faved_by] = get_image_faves(
                    self.id,
                    url_domain=self.url_domain,
                    proxies=self.proxies
                )
            else:
                self._data[faved_by] = []

        return self._data[faved_by]

    @property
    def comments(self):
        # filter_id used to get comments for any image
        return Comments(
            filter_id=system_filters["everything"],
            url_domain=self.url_domain,
            proxies=self.proxies
        ).image_id(self.id)

    @property
    def url(self) -> str:
        return f"{self.url_domain}/images/{self.id}"

    @property
    def data(self):
        return self._data

    def update(self):
        if data := get_image_data(self.id, url_domain=self.url_domain, proxies=self.proxies):
            self._data = data

    @property
    def artists(self):
        self_tag_list = '(' + ' || '.join(f"name:{tag}" for tag in self.tags) + ')'
        art_tag_list = (
            '(category:origin, namespace:?* '
            '|| name:artist needed '
            '|| name:anonymous artist '
            '|| name:kotobukiya)'
        )
        tags = Tags(
            q=(self_tag_list, art_tag_list,),
            per_page=50,
            limit=len(self_tag_list),
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for tag in tags:
            yield tag.name_in_namespace

    @property
    def rating(self) -> list[str]:
        #all_ratings = {
        #   tag.name
        #   for tag in Tags(
        #       q={"category:rating"},
        #       url_domain=self.url_domain,
        #       proxies=self.proxies
        #   )
        #}
        all_ratings = {
            "safe", "suggestive", "questionable", "explicit",
            "semi-grimdark", "grimdark", "grotesque"
        }
        rating_tags = list(set(self.tags).intersection(all_ratings))
        return rating_tags

    @property
    def species(self):
        self_tag_list = '(' + ' || '.join(f"name:{tag}" for tag in self.tags) + ')'
        sp_tag_list = ('(category:species '
                       '|| name:humanized '
                       '|| name:anthro centaur '
                       '|| name:bat alicorn)')
        tags = Tags(
            q=(self_tag_list, sp_tag_list,),
            per_page=50,
            limit=len(self_tag_list),
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for tag in tags:
            yield tag.name_in_namespace

    @property
    def characters(self):
        self_tag_list = '(' + ' || '.join(f"name:{tag}" for tag in self.tags) + ')'
        ch_tag_list = '(category:character || category:oc)'
        tags = Tags(
            q=(self_tag_list, ch_tag_list, "-name:oc", "-name:oc only"),
            per_page=50,
            limit=len(self_tag_list),
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for tag in tags:
            yield tag.name_in_namespace

    @property
    def spoiler(self):
        spoiler_tags: list[str] = []
        self_tag_list = '(' + ' || '.join(f"name:{tag}" for tag in self.tags) + ')'
        sp_tag_list = '(category:spoiler || category:content-official)'
        tags = Tags(
            q=(self_tag_list, sp_tag_list,),
            per_page=50,
            limit=len(self_tag_list),
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        aliases: list[str] = []
        for tag in tags:
            if tag.category == "spoiler" and tag.name != "leak":
                spoiler_tags.append(tag.name_in_namespace)
            elif tag.category == "content-official" and tag.aliases:
                aliases.extend(tag.aliases)
            elif tag.category == "content-official":
                spoiler_tags.append(tag.name_in_namespace)
        if aliases:
            aliases_str = ' || '.join(f"slug:{tag}" for tag in set(aliases))
            tags = Tags(
                q=(aliases_str,),
                per_page=50,
                limit=len(aliases),
                url_domain=self.url_domain,
                proxies=self.proxies
            )
            for tag in tags:
                if tag.category == "spoiler" and tag.name != "leak":
                    spoiler_tags.append(tag.name_in_namespace)
        for tag in sorted(set(spoiler_tags)):
            yield tag

    @property
    def sources(self) -> list[str]:
        return self.data.get('source_urls', [ self.url ])

    @property
    def source(self) -> str:
        return self.sources[0]

    @property
    def upvoted(self) -> bool:
        """
        Checking image in my:upvotes.
        """
        images = request_image(
            {
                'key': self.key,
                'filter_id': system_filters["everything"],
                'per_page': 1,
                'q': (f'id:{self.id}', 'my:upvotes')
            },
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for _ in images:
            return True
        return False

    @property
    def downvoted(self) -> bool:
        """
        Checking image in my:downvotes.
        """
        images = request_image(
            {
                'key': self.key,
                'filter_id': system_filters["everything"],
                'per_page': 1,
                'q': (f'id:{self.id}', 'my:downvotes')
            },
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for _ in images:
            return True
        return False

    @property
    def uploaded(self) -> bool:
        """
        Checking image in my:uploads.
        """
        images = request_image(
            {
                'key': self.key,
                'filter_id': system_filters["everything"],
                'per_page': 1,
                'q': (f'id:{self.id}', 'my:uploads')
            },
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for _ in images:
            return True
        return False

    @property
    def faved(self) -> bool:
        """
        Checking image in my:faves.
        """
        images = request_image(
            {
                'key': self.key,
                'filter_id': system_filters["everything"],
                'per_page': 1,
                'q': (f'id:{self.id}', 'my:faves')
            },
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for _ in images:
            return True
        return False

    @property
    def watched(self) -> bool:
        """
        Checking image in my:watches.
        """
        images = request_image(
            {
                'key': self.key,
                'filter_id': system_filters["everything"],
                'per_page': 1,
                'q': (f'id:{self.id}', 'my:faves')
            },
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        for _ in images:
            return True
        return False

    def next(self):
        """
        Get next Image in Search().
        """
        parameters = {**self._params, 'per_page': 1, 'sf': 'created_at'}
        parameters['q'].add(f'id.lt:{self.id}')
        data = request_image(parameters, url_domain=self.url_domain, proxies=self.proxies)
        try:
            return Image(
                next(data),
                search_params={
                    **self._params,
                    'key': self.key if self.key else self._params.get("key", None)
                },
                url_domain=self.url_domain,
                proxies=self.proxies
            )
        except StopIteration:
            return self

    def prev(self):
        """
        Get previous Image in Search().
        """
        parameters = {**self._params, 'per_page': 1, 'sf': 'created_at'}
        parameters['q'].add(f'id.gt:{self.id}')
        parameters['sd'] = 'desc' if self._params.get('sd', 'desc')=='asc' else 'asc'
        data = request_image(parameters, url_domain=self.url_domain, proxies=self.proxies)
        try:
            return Image(
                next(data),
                search_params={
                    **self._params,
                    'key': self.key if self.key else self._params.get("key", None)
                },
                url_domain=self.url_domain,
                proxies=self.proxies
            )
        except StopIteration:
            return self
