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
from typing import Iterable, Literal
from .request import get_images, url, get_related, url_related
from .image import Image
from .helpers import norm_query_list, tags, api_key, sort_format, sort, join_params, set_limit, \
                     validate_filter, set_distance, validate_url

__all__ = [
    "Search",
    "Related"
]

class Search:
    """
    Search() is the primary interface for interacting with Derpibooru's REST API.

    All properties are read-only, and every method returns a new instance of
    Search() to avoid mutating state in ongoing search queries. This makes object
    interactions predictable as well as making versioning of searches relatively
    easy.
    """
    def __init__(
        self,
        key: str|None = None,
        q: Iterable[str]|str|None = None,
        sf: str = "created_at",
        sd: Literal['asc', 'desc'] = "desc",
        limit: int = 50,
        faves: bool|None = None,
        upvotes: bool|None = None,
        uploads: bool|None = None,
        watched: bool|None = None,
        filter_id: int|None = None,
        per_page: int = 25,
        page: int = 1,
        reverse_url: str|None = None,
        distance: Real = 0.25,
        url_domain: str = "https://derpibooru.org",
        proxies: dict[str, str]|None = None
    ):
        """
        By default initializes an instance of Search with the parameters to get
        the first 25 images on Derpibooru's front page.
        For reverse searching by image use reverse_url field.
        """
        self.proxies = proxies
        self.url_domain = url_domain
        self._params = {
            "key": api_key(key),
            "reverse_url": validate_url(reverse_url),
            "distance": set_distance(distance),
            "q": tags(q),
            "sf": sort_format(sf),
            "sd": sd,
            "filter_id": validate_filter(filter_id),
            "per_page": set_limit(per_page),
            "page": set_limit(page)
        }

        if faves is not None and self._params.get("key", None):
            if faves:
                self._params["q"] -= {"-my:faves"}
                self._params["q"].add("my:faves")
            else:
                self._params["q"] -= {"my:faves"}
                self._params["q"].add("-my:faves")
        else:
            self._params["q"] -= {"-my:faves", "my:faves"}
        if upvotes is not None and self._params.get("key", None):
            if upvotes:
                self._params["q"] -= {"-my:upvotes"}
                self._params["q"].add("my:upvotes")
            else:
                self._params["q"] -= {"my:upvotes"}
                self._params["q"].add("-my:upvotes")
        else:
            self._params["q"] -= {"-my:upvotes", "my:upvotes"}
        if uploads is not None and self._params.get("key", None):
            if uploads:
                self._params["q"] -= {"-my:uploads"}
                self._params["q"].add("my:uploads")
            else:
                self._params["q"] -= {"my:uploads"}
                self._params["q"].add("-my:uploads")
        else:
            self._params["q"] -= {"-my:uploads", "my:uploads"}
        if watched is not None and self._params.get("key", None):
            if watched:
                self._params["q"] -= {"-my:watched"}
                self._params["q"].add("my:watched")
            else:
                self._params["q"] -= {"my:watched"}
                self._params["q"].add("-my:watched")
        else:
            self._params["q"] -= {"-my:watched", "my:watched"}

        self._limit = set_limit(limit)
        self._search = get_images(
            self._params,
            self._limit,
            url_domain=self.url_domain,
            proxies=self.proxies
        )

    def __iter__(self):
        """
        Make Search() iterable so that new search results can be lazily generated
        for performance reasons.
        """
        return self

    @property
    def parameters(self):
        """
        Returns a list of available parameters; useful for passing state to new
        instances of Search().
        """
        return self._params

    @property
    def url(self) -> str:
        """
        Returns a search URL built on set parameters. Example based on default
        parameters:

        https://derpibooru.org/search?sd=desc&sf=created_at&q=%2A
        """
        return url(self.parameters, url_domain=self.url_domain)

    def key(self, key: str|None = None):
        """
        Takes a user's API key string which applies content settings. API keys can
        be found at <https://derpibooru.org/registration/edit>.
        """
        params = join_params(
            self.parameters,
            {
                "key": api_key(key),
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def query(self, *q: str|Iterable[str]):
        """
        Takes one or more strings for searching by tag and/or metadata.
        """
        params = join_params(
            self.parameters,
            {
                "q": norm_query_list(q),
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def sort_by(self, sf: str):
        """
        Determines how to sort search results. Available sorting methods are
        sort.SCORE, sort.COMMENTS, sort.HEIGHT, sort.RELEVANCE, sort.CREATED_AT,
        and sort.RANDOM; default is sort.CREATED_AT.
        """
        params = join_params(
            self.parameters,
            {
                "sf": sf,
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def descending(self):
        """
        Order results from largest to smallest; default is descending order.
        """
        params = join_params(
            self.parameters, {
                "sd": "desc",
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def ascending(self, sd: Literal["asc", "desc"] = "asc"):
        """
        Order results from smallest to largest; default is descending order.
        """
        params = join_params(
            self.parameters,
            {
                "sd": sd,
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def limit(self, limit: int):
        """
        Set absolute limit on number of images to return, or set to None to return
        as many results as needed; default 50 posts. This limit on app-level.
        """
        params = join_params(
            self.parameters,
            {
                "limit": set_limit(limit),
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def filter(self, filter_id: int|None = None):
        """
        Takes a filter's ID to be used in the current search context. Filter IDs can
        be found at <https://derpibooru.org/filters/> by inspecting the URL parameters.

        If no filter is provided, the user's current filter will be used.
        """
        params = join_params(
            self.parameters,
            {
                "filter_id": validate_filter(filter_id),
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)


    def faves(self, option: bool|None):
        """
        Set whether to filter by a user's faves list. Options available are
        user.ONLY, user.NOT, and None; default is None.
        """
        if self.parameters["key"] and option is True:
            query = self.query_remove("-my:faves").query_append("my:faves")
        elif self.parameters["key"] and option is False:
            query = self.query_remove("my:faves").query_append("-my:faves")
        else:
            query = self.query_remove("my:faves").query_remove("-my:faves")
        return query

    def upvotes(self, option: bool|None):
        """
        Set whether to filter by a user's upvoted list. Options available are
        user.ONLY, user.NOT, and None; default is None.
        """
        if self.parameters["key"] and option is True:
            query = self.query_remove("-my:upvotes").query_append("my:upvotes")
        elif self.parameters["key"] and option is False:
            query = self.query_remove("my:upvotes").query_append("-my:upvotes")
        else:
            query = self.query_remove("my:upvotes").query_remove("-my:upvotes")
        return query

    def uploads(self, option: bool|None):
        """
        Set whether to filter by a user's uploads list. Options available are
        user.ONLY, user.NOT, and None; default is None.
        """
        if self.parameters["key"] and option is True:
            query = self.query_remove("-my:uploads").query_append("my:uploads")
        elif self.parameters["key"] and option is False:
            query = self.query_remove("my:uploads").query_append("-my:uploads")
        else:
            query = self.query_remove("my:uploads").query_remove("-my:uploads")
        return query

    def watched(self, option: bool|None):
        """
        Set whether to filter by a user's watchlist. Options available are
        user.ONLY, user.NOT, and None; default is None.
        """
        if self.parameters["key"] and option is True:
            query = self.query_remove("-my:watched").query_append("my:watched")
        elif self.parameters["key"] and option is False:
            query = self.query_remove("my:watched").query_append("-my:watched")
        else:
            query = self.query_remove("my:watched").query_remove("-my:watched")
        return query

    def top(self):
        """
        Returns search for Trending Images from front page.
        """
        return self.query('first_seen_at.gt:3 days ago').sort_by(sort.SCORE)

    def exclude_by_id(self, *ids: int):
        """
        Excludes images from search by id.
        """
        return (
            self
            .query_remove(f"id:{elem}" for elem in ids)
            .query_append(f"-id:{elem}" for elem in ids)
        )

    def query_append(self, *q: str|Iterable[str]):
        """
        Adds tags to current search.
        """
        q = norm_query_list(q)

        query: set[str] = self.parameters.get('q', set()).union(q)
        params = join_params(
            self.parameters,
            {
                "q": query,
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def query_remove(self, *q: str|Iterable[str]):
        """
        Removes tags from current search.
        """
        q = norm_query_list(q)

        query: set[str] = self.parameters.get('q', set()).difference(q)
        params = join_params(
            self.parameters,
            {
                "q": query,
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def get_related(self, image: int|Literal["featured"]|Image):
        if isinstance(image, Image):
            return Related(
                image,
                key=self.parameters.get('key', ''),
                limit=self._limit,
                filter_id=self.parameters.get('filter_id', None),
                per_page=self.parameters.get('per_page', None),
                url_domain=self.url_domain,
                proxies=self.proxies
            )
        return Related(
            Image(None, image_id=image, url_domain=self.url_domain, proxies=self.proxies),
            key=self.parameters.get('key', ''),
            limit=self._limit,
            filter_id=self.parameters.get('filter_id', None),
            per_page=self.parameters.get('per_page', None),
            url_domain=self.url_domain,
            proxies=self.proxies
        )

    def get_page(self, page: int):
        """
        Set page for gets result of search.
        """
        params = join_params(
            self.parameters,
            {
                "page": set_limit(page),
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def per_page(self, limit: int):
        """
        Set absolute limit on number of images to get, or set to None to return
        defaulting 25 posts; max 50 posts. This limit on API-level.
        """
        params = join_params(
            self.parameters,
            {
                "per_page": set_limit(limit),
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def reverse(self, url_link: str):
        """
        Takes an url image for reverse search.
        """
        params = join_params(
            self.parameters,
            {
                "reverse_url": url_link,
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def distance(self, distance: Real):
        """
        Match distance for reverse search (suggested values: between 0.2 and 0.5)
        """
        params = join_params(
            self.parameters,
            {
                "distance": set_distance(distance),
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def __next__(self):
        """
        Returns a result wrapped in a new instance of Image().
        """
        return Image(
            next(self._search),
            search_params=self.parameters,
            url_domain=self.url_domain,
            proxies=self.proxies
        )

class Related(Search):
    """
    Related() is the Search-like interface based on related images instead query.
    Related images gets with old API in JSON and with new API in Web.
    This class should returns Search() for any query-like actions.
    """
    def __init__(
        self,
        image: Image,
        key: str|None = None,
        limit: int = 50,
        filter_id: int|None = None,
        per_page: int = 25,
        url_domain: str = "https://derpibooru.org",
        proxies: dict[str, str]|None = None
    ):
        """
        By default initializes with the parameters to get the first 25 related images.
        """
        if proxies:
            self.proxies = proxies
        else:
            self.proxies = image.proxies
        self.url_domain = url_domain
        self.image = image
        self._params = {
            "key": api_key(key) if key else api_key(image._params.get("key", "")),
            "filter_id": validate_filter(filter_id),
            "per_page": set_limit(per_page)
        }
        self._limit = set_limit(limit)
        self._search = get_related(
            self.image.id,
            self._params,
            self._limit,
            url_domain=self.url_domain,
            proxies=self.proxies
        )

    @property
    def url(self) -> str:
        """
        Returns a search URL built on set parameters. Example based on default
        parameters:

        https://derpibooru.org/images/***/related?key=&filter_id=&per_page=25
        """
        return url_related(self.image.id, self.parameters, url_domain=self.url_domain)

    def query(self, *q: str|Iterable[str]):
        """
        Takes one or more strings for searching by tag and/or metadata.
        """
        params = join_params(
            self.parameters,
            {
                "q": norm_query_list(q),
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )
        return Search(**params)

    def sort_by(self, sf: str):
        """
        Related() can't be sorted.
        """
        return self

    def descending(self):
        """
        Related() can't be sorted.
        """
        return self

    def ascending(self, sd: Literal["asc", "desc"] = "asc"):
        """
        Related() can't be sorted.
        """
        return self

    def query_append(self, *q: str|Iterable[str]):
        """
        Synonyme of query() for Related().
        """
        return self.query(*q)

    def query_remove(self, *q: str|Iterable[str]):
        """
        Nothing remove from Related().
        """
        return self

    def get_page(self, page: int):
        """
        Related() hasn't pages.
        """
        return self

    def reverse(self, url_link: str):
        """
        Takes an url image for reverse search.
        """
        params = join_params(
            self.parameters,
            {
                "reverse_url": url_link,
                "limit": self._limit,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return Search(**params)

    def distance(self, distance: Real):
        """
        It hasn't any sense in Related()
        """
        return self
