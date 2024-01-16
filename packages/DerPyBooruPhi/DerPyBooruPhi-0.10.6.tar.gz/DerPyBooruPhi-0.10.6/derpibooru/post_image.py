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

from typing import Iterable
from .request import post_image
from .tags import Tags
from .image import Image
from .search import Search
from .helpers import join_params, tags, api_key, validate_url, validate_description

__all__ = [
    "PostImage",
    "ImageError", "TagsError", "LengthError", "PostError", "DuplicateError"
]

class PostImage:
    """
    This class is a helper for submits a new image by using API.
    Abuse will result in a ban.
    You must provide the direct link to the image in the url parameter.
    """
    def __init__(
        self,
        key: str|None = None,
        image_url: str|None = None,
        description: str|None = None,
        tag_input: Iterable[str]|str|None = None,
        source_url: str|None = None,
        url_domain: str = "https://derpibooru.org",
        proxies: dict[str, str]|None = None
    ):

        self.proxies = proxies
        self.url_domain = url_domain
        self._params: dict[str, str|set[str]|None] = {
            "key": api_key(key),
            "image_url": validate_url(image_url),
            "description": validate_description(description),
            "tag_input": tags(tag_input),
            "source_url": validate_url(source_url)
        }

    def __str__(self):
        params = ", ".join(
            f"{param_name}='{param_value}'"
            for param_name, param_value in self.parameters.items()
        )
        return f"PostImage({params})"

    @property
    def parameters(self):
        """
        Returns a list of available parameters; useful for passing state to new
        instances of PostImage().
        """
        return self._params

    def key(self, key: str|None=None):
        """
        Takes a user's API key string which applies content settings. API keys can
        be found at <https://derpibooru.org/registration/edit>.
        """
        params = join_params(
            self.parameters,
            {
                "key": key,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def image_url(self, image_url: str|None=None):
        """
        Direct link to the image.
        """
        params = join_params(
            self.parameters,
            {
                "image_url": image_url,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def description(self, description: str|None=None):
        """
        Describe this image in plain words - this should generally be info about
        the image that doesn't belong in the tags or source.
        This field supports simple html.
        Can be 50000 bytes max.
        """
        params = join_params(
            self.parameters,
            {
                "description": description,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def tag_input(self, *tags_list: str):
        """
        Describe with 3+ tags, including ratings and applicable artist tags
        """
        params = join_params(
            self.parameters,
            {
                "tag_input": tags_list,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def source_url(self, source_url: str|None=None):
        """
        Describe with 3+ tags, including ratings and applicable artist tags
        """
        params = join_params(
            self.parameters,
            {
                "source_url": source_url,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def post(self, new_tags: bool=False, dnp: bool=False, dupe: bool=False):
        """
        Post new image and return Image() object or raise error.
        Set "new_tags"=True for accept adding new tags.
        Set "dnp"=True for accept posting image from DNP artist.
        Set "dupe"=True for ignore duplicate checking.
        """
        if self.parameters.get('key', '') and self.parameters.get('image_url', ''):
            self.validate_tags()
            if not new_tags:
                if fix_tags := self.check_tags()[1]:
                    error_tags_str = {
                        ', '.join(
                            f'{tag_name} -> {tag_value}' if tag_value else tag_name
                            for tag_name, tag_value in fix_tags.items()
                        )
                    }
                    raise TagsError(
                        self.parameters['tag_input'],
                        reason=(
                            "this tags wasn't used before "
                            f"({error_tags_str})"
                        )
                    )
            if not dnp:
                if dnp_tags := self.dnp():
                    br = '\n'
                    error_tags = []
                    for tag_name in sorted(dnp_tags):
                        dnp_conditions = (
                            dnp_entry['conditions']
                            for dnp_entry in dnp_tags[tag_name]
                        )
                        error_tags_str = (
                            f"{tag_name} : [\n"
                            f"{br.join(dnp_conditions) : >{len(tag_name)}}\n]"
                        )
                        error_tags.append(error_tags_str)
                    dnp_reasons = br.join(error_tags)
                    raise TagsError(
                        self.parameters['tag_input'],
                        reason=f"DNP\n{dnp_reasons}"
                    )
            if not dupe:
                if duplicates := self.check_duplicate():
                    raise DuplicateError(self.parameters, duplicates)
            response = post_image(
                **self.parameters,
                url_domain=self.url_domain,
                proxies=self.proxies
            )
            if "errors" in response:
                raise ImageError(response["errors"])
            return Image(
                response["image"],
                key=self.parameters.get('key', ''),
                url_domain=self.url_domain,
                proxies=self.proxies
            )
        raise PostError(self.parameters)

    def validate_tags(self):
        """
        Preposting tag validation will raise TagsError() if tag_input is incorrect.
        tag_input require:
        - 3+ tags;
        - at least one rating tag, and for non-safe images can have one of each non-safe type;
        - not blacklisted (you can found blacklist at
        <https://github.com/derpibooru/philomena/blob/master/config/tag.json>)
        """
        tag_input: set[str] = self.parameters['tag_input']
        safe_rating = set(("safe",))
        sexual_ratings = set(("suggestive", "questionable", "explicit",))
        horror_ratings = set(("semi-grimdark", "grimdark",))
        gross_rating = set(("grotesque",))
        rating_tags = safe_rating | sexual_ratings | horror_ratings | gross_rating
        blacklist = set((
            "tagme", "tag me", "not tagged", "no tag", "notag",
            "notags", "upvotes galore", "downvotes galore", "wall of faves",
            "drama in the comments", "drama in comments", "tag needed",
            "paywall", "cringeworthy", "solo oc", "tag your shit"
        ))
        if len(tag_input) < 3:
            reason = "must contain at least 3 tags"
        elif tag_input & blacklist:
            reason = f"contains forbidden tag ({', '.join(sorted(tag_input & blacklist))})'"
        elif not (tag_input & rating_tags):
            reason = "must contain at least one rating tag"
        elif (safe_rating & tag_input) and (tag_input & (rating_tags-safe_rating)):
            reason = (
                "may not contain any other rating if safe "
                f"({', '.join(sorted(tag_input & (rating_tags-safe_rating)))})"
            )
        elif len(sexual_ratings & tag_input) > 1:
            reason = (
                "may contain at most one sexual rating "
                f"({', '.join(sorted(sexual_ratings & tag_input))})"
            )
        elif len(horror_ratings & tag_input) > 1:
            reason = (
                "may contain at most one grim rating "
                f"({', '.join(sorted(horror_ratings & tag_input))})"
            )
        else:
            reason = ""
        if reason:
            raise TagsError(tag_input, reason)
        return True

    def check_tags(self):
        """
        Returns dict() with image count as value for every tag in tag_input.
        So, if tag has 0 image count, it means that tag does not exist on Derpibooru.
        """
        query = ' || '.join(f"name:{tag}" for tag in self.parameters['tag_input'])
        tags_list = Tags(
            q=(query,),
            per_page=50,
            limit=len(self.parameters['tag_input']),
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        tags_count: dict[str, int] = {
            tag.name: (tag.alias_parent().images if tag.alias_parent() else tag.images)
            for tag in tags_list
        }
        num_tags = {
            tag_name: tags_count.get(tag_name, 0)
            for tag_name in self.parameters['tag_input']
        }
        fix_tags: dict[str, str|None] = {}
        for tag_name, tag_count in num_tags.items():
            if tag_count==0:
                if ft := list(
                    Tags(
                        q=(f"name:{tag_name}~1.0",),
                        per_page=50,
                        limit=1,
                        url_domain=self.url_domain,
                        proxies=self.proxies
                    )
                ):
                    fix_tags[tag_name] = ft[0].name
                else:
                    fix_tags[tag_name] = None
        return num_tags, fix_tags

    def dnp(self):
        """
        Returns dict() of tags artists who have a restriction on the uploading
        of their artwork. Values are conditions for upload and empty condition
        means that only artist can upload.
        """
        query = ' || '.join(f"name:{tag}" for tag in self.parameters['tag_input'])
        tags_list = Tags(
            q=(query,),
            per_page=50,
            limit=len(self.parameters['tag_input']),
            url_domain=self.url_domain,
            proxies=self.proxies
        )
        dnp_tags: dict[str, list[dict[str]]] = {
            tag.name : tag.dnp_entries
            for tag in tags_list
            if tag.dnp_entries
        }
        return dnp_tags

    def check_duplicate(self):
        """
        Return duplicates of image or False if image is unique.
        """
        if reverse := tuple(
            Search(
                reverse_url=self.parameters['image_url'],
                distance=0.25,
                url_domain=self.url_domain,
                proxies=self.proxies
            )
        ):
            return reverse
        return False

    def tags_append(self, *tags_list: str):
        """
        Adds tags to current tag_input.
        """
        new_tags = self.parameters.get('tag_input', set()).union(tags_list)
        params = join_params(
            self.parameters,
            {
                "tag_input": new_tags,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

    def tags_remove(self, *tags_list: str):
        """
        Removes tags from current tag_input.
        """
        new_tags = self.parameters.get('tag_input', set()).difference(tags_list)
        params = join_params(
            self.parameters,
            {
                "tag_input": new_tags,
                "url_domain": self.url_domain,
                "proxies": self.proxies
            }
        )

        return self.__class__(**params)

class ImageError(Exception):
    """
    Trying to upload image returns response with errors.
    """
    def __init__(self, data: dict[str]):
        self.data = data

    def __str__(self):
        data = '\n'.join(f'{item} : {self.data[item]}' for item in self.data)
        reasons = []
        if "image_format" in self.data:
            reasons.append("unsupported format")
        if "image_height" in self.data:
            reasons.append("probably too big height (32767 px max)")
        if "image_width" in self.data:
            reasons.append("probably too big width (32767 px max)")
        if "image_size" in self.data:
            reasons.append("probably too big size (26 214 400 max)")
        if "image_mime_type" in self.data:
            reasons.append(
                'probably unsupported mime '
                '(should be One of "image/gif", "image/jpeg", '
                '"image/png", "image/svg+xml", "video/webm")'
            )
        if "image_orig_sha512_hash" in self.data:
            reasons.append("image already exists in the database")
        if "tag_input" in self.data:
            reasons.append("errors with the tag metadata")

        return f"{', '.join(reasons)}\n{data}"

class TagsError(Exception):
    """
    Tags are incorrect error.
    """
    def __init__(self, tag_input: set[str], reason: str|None=None):
        self.tag_input = tag_input

        if reason:
            self.reason = reason
        else:
            self.reason = ""
            safe_rating = {"safe"}
            sexual_ratings = {"suggestive", "questionable", "explicit"}
            horror_ratings = {"semi-grimdark", "grimdark"}
            gross_rating = {"grotesque"}
            rating_tags = safe_rating | sexual_ratings | horror_ratings | gross_rating
            blacklist = {
                "tagme", "tag me", "not tagged", "no tag", "notag",
                "notags", "upvotes galore", "downvotes galore", "wall of faves",
                "drama in the comments", "drama in comments", "tag needed",
                "paywall", "cringeworthy", "solo oc", "tag your shit"
            }
            if len(tag_input) < 3:
                self.reason = "must contain at least 3 tags"
            elif tag_input & blacklist:
                self.reason = (
                    "contains forbidden tag "
                    f"({', '.join(sorted(tag_input & blacklist))})'"
                )
            elif not (tag_input & rating_tags):
                self.reason = "must contain at least one rating tag"
            elif (safe_rating & tag_input) and (tag_input & (rating_tags-safe_rating)):
                self.reason = (
                    "may not contain any other rating if safe "
                    f"({', '.join(sorted(tag_input & (rating_tags-safe_rating)))})"
                )
            elif len(sexual_ratings & tag_input) > 1:
                self.reason = (
                    "may contain at most one sexual rating "
                    f"({', '.join(sorted(sexual_ratings & tag_input))})"
                )
            elif len(horror_ratings & tag_input) > 1:
                self.reason = (
                    "may contain at most one grim rating "
                    f"({', '.join(sorted(horror_ratings & tag_input))})"
                )

    def __str__(self):
        return f"{self.reason}"

class LengthError(Exception):
    """
    Too long string error.
    """
    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        message = (
            f"'{self.string[:20]}' has "
            f"{len(self.string.encode('utf-8'))} bytes when max is 50000"
        )
        return message

class PostError(Exception):
    """
    PostImage() has empty required fields error.
    """
    def __init__(self, parameters: dict[str]):
        self.parameters = parameters

    def __str__(self):
        if self.parameters['key']:
            return "should include image_url"
        if self.parameters['image_url']:
            return "should include key"
        return "should include key and image_url"

class DuplicateError(Exception):
    """
    Image already exists error.
    """
    def __init__(self, parameters: dict[str], duplicates: Iterable[Image]):
        self.parameters = parameters
        self.duplicates = duplicates

    def __str__(self):
        message = (
            f"<{self.parameters['image_url']}> already exists "
            f"({', '.join(f'{image.id}' for image in self.duplicates)})"
        )
        return message
