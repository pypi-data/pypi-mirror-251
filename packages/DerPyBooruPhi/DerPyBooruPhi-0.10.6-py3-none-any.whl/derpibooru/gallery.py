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
from .request import get_galleries
from .search import Search
from .image import Image

__all__ = [
    "Gallery"
]

class Gallery:
    """
    This class provides a thin wrapper around JSON data, mapping each value to
    its own property. Once instantiated the data is immutable so as to reflect
    the stateless nature of a REST API.
    """
    def __init__(
        self,
        data: dict[str, str|int]|None,
        gallery_id: int|None = None,
        search_params: dict|None = None,
        url_domain: str = "https://derpibooru.org",
        proxies: dict[str, str]|None = None
    ):
        if not search_params:
            search_params = {}

        self.proxies = proxies
        self.url_domain = url_domain
        self._params = search_params

        if data is None and gallery_id:
            search_params['q'] = (f"id:{gallery_id}",)
            self._data = data = next(
                get_galleries(
                    search_params,
                    limit=1,
                    url_domain=url_domain,
                    proxies=proxies
                )
            )
        else:
            self._data = data

        for field, body in data.items():
            if not hasattr(self, field):
                setattr(self, field, body)

    def __str__(self):
        return f"Gallery({self.id})"

    @property
    def url(self) -> str:
        return f"{self.url_domain}/galleries/{self.id}"

    @property
    def data(self):
        return self._data

    def update(self):
        data: dict[str, str|int] = next(
            get_galleries(
                self._params,
                limit=1,
                url_domain=self.url_domain,
                proxies=self.proxies
            )
        )

        if data:
            self._data = data

    @property
    def thumbnail(self):
        return Image(
            None,
            image_id=self.thumbnail_id,
            search_params=self._params,
            url_domain=self.url_domain,
            proxies=self.proxies
        )

    def images(
        self,
        sf: str = "created_at",
        sd: Literal["asc", "desc"] = "desc",
        limit: int = 50,
        faves: bool|None = None,
        upvotes: bool|None = None,
        uploads: bool|None = None,
        watched: bool|None = None,
        filter_id: int|None = None,
        per_page: int = 25,
        page: int = 1
    ):
        return Search(
            key=self._params.get("key", None),
            q=(f"gallery_id:{self.id}",),
            sf=sf,
            sd=sd,
            limit=limit,
            faves=faves,
            upvotes=upvotes,
            uploads=uploads,
            watched=watched,
            filter_id=filter_id,
            per_page=per_page,
            page=page,
            url_domain=self.url_domain,
            proxies=self.proxies
        )
