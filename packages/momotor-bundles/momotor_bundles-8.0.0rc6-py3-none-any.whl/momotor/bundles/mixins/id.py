from __future__ import annotations

import typing

__all__ = ["IdMixin"]


class IdMixin:
    """ A mixin for elements with an `id` attribute
    """
    __unset: typing.ClassVar = object()
    _id: str = __unset

    @typing.final
    @property
    def id(self) -> str | None:
        """ The `id` attribute """
        assert self._id is not self.__unset, "Uninitialized attribute `id`"
        return self._id

    # noinspection PyShadowingBuiltins
    @id.setter
    def id(self, id: str | None):
        assert self._id is self.__unset, "Immutable attribute `id`"
        assert id is None or isinstance(id, str), "Invalid type for attribute `id`"
        self._id = id
