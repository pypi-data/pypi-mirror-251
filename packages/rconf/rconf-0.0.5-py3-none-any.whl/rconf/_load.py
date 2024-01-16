from __future__ import annotations

import copy
import pathlib
import re
import typing
import urllib.error
import urllib.parse
import uuid
from collections import deque

from .decode import BaseHandler, DecodeError, DecoderDirector
from .patch import Patch, PatchOperation
from .pointer import Key, Pointer, traverse

if typing.TYPE_CHECKING:
    from collections.abc import Iterator
    from urllib.request import OpenerDirector

    from ._value import Value

# `RFC 3986 section 3.1 <https://datatracker.ietf.org/doc/html/rfc3986#section-3.1>`_,
_URL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+\-.]+:")


class _Ref:
    """Unique key."""


class _Missing:
    """Unique key."""


REF_KEYS = ("$ref", _Ref)


def _guess_url(locator: str | pathlib.Path | None = None) -> str:
    """Create a URL given a locator that can be a URL or a file path."""
    if locator is None:
        locator = f"./{uuid.uuid4()}"
    if isinstance(locator, str):
        if _URL_SCHEME_RE.match(locator):
            # an actual URL
            return locator
        # as_uri() drops trailing slash, so keep track of it
        is_folder = locator and locator[-1] in r"\/"
        locator = pathlib.Path(locator)
    else:
        is_folder = False
    locator = locator.expanduser().resolve().as_uri()
    return locator + "/" if is_folder else locator


def _url_ptr(url: str, ptr: str | None = None) -> str:
    """Add a URL fragment if ptr is not None."""
    if ptr is None:
        return url
    return f"{urllib.parse.urldefrag(url).url}#{urllib.parse.quote(ptr)}"


class Loader:
    """Load configurations, replace references and apply patches.

    Uses

    - an :class:`urllib.request.OpenerDirector` and
    - a :class:`rconf.decode.DecoderDirector`.
    """

    def __init__(
        self,
        opener: OpenerDirector | None = None,
        decoder: DecoderDirector | None = None,
    ) -> None:
        """Build a :class:`rconf.Loader`.

        :param opener: The :class:`urllib.request.OpenerDirector`.
        :param decoder: The :class:`rconf.decode.DecoderDirector`.
        """
        self.opener = opener
        self.decoder = decoder

    def load(
        self,
        fp: typing.BinaryIO,
        media_type: str | None = None,
        url: str | pathlib.Path | None = None,
        *,
        ptr: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a ``read``-supporting :term:`binary file` with references and patches.

        :param fp: ``read``-supporting :term:`binary file`.
        :param media_type: Assumed media type, overrides URL-derived media type.
            It can also be a filename extension.
        :param url: Assumed document URL or path
            for media type, fragment and relative reference resolution.
        :param ptr: Fragment pointer, overrides URL fragment.
        :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
            :class:`rconf.patch.PatchError` for patch errors.
        """
        url = _url_ptr(_guess_url(url), ptr)
        handler = self.decoder.get_handler(media_type, url)
        init = handler.load(fp, url, **kwargs)
        return self._load(init, url, handler, **kwargs)

    def loads(
        self,
        s: str,
        media_type: str | None = None,
        url: str | pathlib.Path | None = None,
        *,
        ptr: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a :class:`str` configuration document with references and patches.

        :param s: Configuration document.
        :param media_type: Assumed media type, overrides URL-derived media type.
            It can also be a filename extension.
        :param url: Assumed document URL or path
            for media type, fragment and relative reference resolution.
        :param ptr: Fragment pointer, overrides URL fragment.
        :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
            :class:`rconf.patch.PatchError` for patch errors.
        """
        url = _url_ptr(_guess_url(url), ptr)
        handler = self.decoder.get_handler(media_type, url)
        init = handler.loads(s, url, **kwargs)
        return self._load(init, url, handler, **kwargs)

    def loadc(
        self,
        config: Value,
        media_type: str | None = None,
        url: str | pathlib.Path | None = None,
        *,
        ptr: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a configuration document with references and patches.

        :param config: Configuration :class:`rconf.Value`.
        :param media_type: Assumed media type, overrides URL-derived media type.
            It can also be a filename extension.
        :param url: Assumed document URL or path
            for media type, fragment and relative reference resolution.
        :param ptr: Fragment pointer, overrides URL fragment.
        :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
            :class:`rconf.patch.PatchError` for patch errors.
        """
        url = _url_ptr(_guess_url(url), ptr)
        handler = self.decoder.get_handler(media_type, url)
        return self._load(
            copy.deepcopy(config),
            url,
            handler,
            **kwargs,
        )

    def loadu(
        self,
        url: str | pathlib.Path,
        media_type: str | None = None,
        *,
        base_url: str | pathlib.Path | None = None,
        ptr: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a configuration document at a URL or path with references and patches.

        :param url: Document URL or path,
            optionally with a language-specific pointer as URL fragment.
        :param media_type: Assumed media type, overrides URL-derived media type
            and content-type from :func:`urllib.request.OpenerDirector.open`.
            It can also be a filename extension.
        :param base_url: Assumed document URL or path
            for relative reference resolution, overrides URL base.
        :param ptr: Fragment pointer, overrides URL fragment.
        :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
            :class:`rconf.patch.PatchError` for patch errors.
        """
        url = _guess_url(url)
        handler, init = self._open(url, media_type)

        if base_url is None:
            url = _url_ptr(url, ptr)
        else:
            if ptr is None:
                ptr = urllib.parse.unquote(urllib.parse.urldefrag(url).fragment)
            url = _url_ptr(_guess_url(base_url), ptr)

        return self._load(init, url, handler, **kwargs)

    def _load(
        self,
        init: Value,
        url: str,
        handler: BaseHandler,
        **kwargs,
    ) -> Value:
        """Decode a configuration document at a URL with references and patches.

        :param init: Configuration :class:`rconf.Value`.
        :param url: Assumed document URL
            for fragment and relative reference resolution.
        :param handler: The :class:`BaseHandler` of the initial document.
        :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
            :class:`rconf.patch.PatchError` for patch errors.
        """
        # keep track of loaded documents
        url_handler_value: dict[str, tuple[BaseHandler, Value]] = {
            urllib.parse.urldefrag(url).url: (handler, init),
        }

        # embedded in a list to always have a parent
        result: Value = [{"$ref": url}]

        # traversal stack
        url_handler_items: deque[
            tuple[str, BaseHandler, Iterator[tuple[Pointer, Value, Key, Value]]]
        ] = deque(
            [
                (
                    "",
                    handler,
                    iter(
                        traverse(
                            result[0],
                            leafs=False,
                            lists=False,
                            parent=result,
                            key=0,
                            pointer_type=handler.pointer_type,
                        ),
                    ),
                ),
            ],
        )

        # iterate over dicts, looking for references
        while url_handler_items:
            src_url, src_handler, src_items = url_handler_items[-1]
            try:
                src_ptr, src_parent, src_key, src_value = next(src_items)
            except StopIteration:
                url_handler_items.pop()
                continue

            # unvisited reference
            src_ref = src_value.pop("$ref", _Missing)
            if src_ref is not _Missing:
                if not isinstance(src_ref, str):
                    msg = (
                        f'Error loading "{src_url}": {src_ptr/"$ref"} is not a string.'
                    )
                    raise DecodeError(msg)
                # parse URL
                target_url, target_fragment = urllib.parse.urldefrag(
                    urllib.parse.urljoin(src_url, src_ref),
                )
                # parse patch
                target_patch = _build_patch(src_value, src_handler.pointer_type)
                # load document if needed
                if target_url not in url_handler_value:
                    target_handler, target_value = self._open(target_url, **kwargs)
                    url_handler_value[target_url] = (target_handler, target_value)
                else:
                    target_handler, target_value = url_handler_value[target_url]

                # reduce ptr and insert
                # don't resolve because you might miss patches in target document
                ptr = target_handler.pointer_type.parse(
                    urllib.parse.unquote(target_fragment),
                )
                _, _, target_value, target_ptr = ptr.reduce(
                    target_value,
                    stop_keys=REF_KEYS,
                )

                src_value.clear()
                src_value[_Ref] = [target_value, target_ptr, target_patch]

                # referenced content should also be processed
                url_handler_items.append(
                    (
                        target_url,
                        target_handler,
                        iter(
                            traverse(
                                src_value,
                                leafs=False,
                                lists=False,
                                parent=src_parent,
                                key=src_key,
                                pointer_type=target_handler.pointer_type,
                            ),
                        ),
                    ),
                )
                continue

            # previously visited reference
            src_ref = src_value.get(_Ref, None)
            if src_ref is not None:
                value: Value
                ptr: Pointer | None
                patch: Patch | None
                value, ptr, patch = src_ref
                if ptr:
                    value = ptr.resolve(value)
                    src_ref[0] = value
                    src_ref[1] = None
                if id(value) == id(src_value):
                    msg = f"A reference cannot point to itself ({target_url}#{ptr})."
                    raise DecodeError(msg)
                if patch is not None:
                    src_value = copy.deepcopy(src_value)
                    src_ref = src_value[_Ref]
                    value, _, patch = src_ref
                    value = patch.apply(value, in_place=True)
                    src_ref[2] = None
                src_parent[src_key] = value

        # handle patched circular references
        for _, parent, key, child in traverse(
            result[0],
            leafs=False,
            lists=False,
            parent=result,
            key=0,
        ):
            ref = child.get(_Ref, None)
            if ref is not None:
                parent[key] = ref[0]

        return result[0]

    def _open(
        self,
        url: str,
        media_type: str | None = None,
        **kwargs,
    ) -> tuple[BaseHandler, Value]:
        try:
            with self.opener.open(url) as fp:
                if media_type is None and "content-type" in fp.headers:
                    media_type = fp.headers["content-type"]
                    if media_type not in self.decoder.handlers:
                        media_type = None
                handler = self.decoder.get_handler(media_type, url)
                return (handler, handler.load(fp, url, **kwargs))
        except urllib.error.URLError as error:
            msg = f'Error loading "{url}".'
            raise DecodeError(msg) from error


def _build_patch(value: Value, pointer_type: type[Pointer]) -> Patch | None:
    if value:
        patch = Patch(value.pop("$patch", None), pointer_type)
        for patch_key, patch_value in value.items():
            patch.add(PatchOperation.ASSIGN, patch_key, patch_value)
        return patch
    return None
