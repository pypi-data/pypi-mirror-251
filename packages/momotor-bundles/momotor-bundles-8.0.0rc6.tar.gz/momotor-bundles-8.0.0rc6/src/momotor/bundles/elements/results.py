from __future__ import annotations

import collections.abc
import dataclasses
import typing
import warnings
from abc import ABC

import momotor.bundles
from momotor.bundles.binding import ResultsComplexType, TestResultComplexType, ResultComplexType
from momotor.bundles.elements.base import Element, NestedElement
from momotor.bundles.elements.meta import MetaMixin, Meta
from momotor.bundles.elements.result import Result
from momotor.bundles.exception import BundleFormatError
from momotor.bundles.mixins.id import IdMixin
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.assertion import assert_elements_instanceof
from momotor.bundles.utils.keyedtuple import KeyedTuple

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['ResultsBase', 'Results', 'ResultKeyedTuple']

RT = typing.TypeVar("RT")


ResultsType: TypeAlias = typing.Union[KeyedTuple[Result], typing.Mapping[str, Result], typing.Iterable[Result]]


class ResultKeyedTuple(KeyedTuple[Result]):
    """ The results as a :py:class:`~momotor.bundles.utils.keyedtuple.KeyedTuple`
    of :py:class:`~momotor.bundles.elements.result.Result` objects.

    The KeyedTuple allows access as a tuple or a mapping. Results are indexed by their `step_id` attribute
    """

    def __init__(self, results: ResultsType | None = None):
        super().__init__(results, key_attr='step_id')


# noinspection PyProtectedMember
class ResultsBase(typing.Generic[RT], NestedElement[ResultsComplexType, TestResultComplexType],
                  IdMixin, MetaMixin, ABC):
    # noinspection PyUnresolvedReferences
    __unset: typing.ClassVar = object()
    _results: ResultKeyedTuple = __unset

    @typing.final
    @property
    def results(self) -> ResultKeyedTuple:
        """ `results` children """
        assert self._results is not self.__unset, "Uninitialized attribute `results`"
        return self._results

    @results.setter
    def results(self, results: typing.Iterable[Result] | None):
        assert self._results is self.__unset, "Immutable attribute `results`"
        if results is None:
            self._results = ResultKeyedTuple()
        else:
            assert isinstance(results, (KeyedTuple, collections.abc.Mapping, collections.abc.Iterable))
            self._results = assert_elements_instanceof(
                ResultKeyedTuple(results), Result, self.bundle
            )

    @staticmethod
    def _get_parent_type() -> type[TestResultComplexType]:
        return TestResultComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str | None = None,
               meta: Meta | None = None,
               results: ResultsType | None = None) -> Self:
        self.id = id
        self.meta = meta
        self.results = results
        return self

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ResultsComplexType, testresult: TestResultComplexType | None = None, *,
                          args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)
        self._check_parent_type(testresult, True)

        if node.checklets and not args.legacy:
            msg = '`checklets` in results nodes has been removed'
            if args.validate_xml:
                raise BundleFormatError(msg)
            else:
                warnings.warn(msg)

        return self.create(
            id=node.id,
            meta=self._collect_meta(node, args=args),
            results=[
                Result(self.bundle)._create_from_node(result, node, args=args) for result in node.result
            ] if node.result else None
        )

    def _construct_node(self, *, args: BundleConstructionArguments) -> RT:
        child_args = dataclasses.replace(args, generator_name=False)
        return self.get_node_type()(
            id=self.id,
            meta=list(self._construct_meta_node(args=args)),
            result=list(self._construct_result_nodes(args=child_args)),
        )

    def _construct_result_nodes(self, *, args: BundleConstructionArguments) \
            -> typing.Generator[ResultComplexType, None, None]:
        results = self.results
        if results:
            for result in results.values():
                yield result._construct_node(args=args)


class Results(ResultsBase[ResultsComplexType]):
    """ A Results element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.ResultsComplexType`
    """

    @staticmethod
    def get_node_type() -> type[ResultsComplexType]:
        return ResultsComplexType

    # noinspection PyMethodOverriding
    def recreate(self, target_bundle: "momotor.bundles.Bundle") -> typing.NoReturn:
        raise ValueError("Cannot recreate Results in a target bundle")


if Results.__doc__ and Element.__doc__:
    Results.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
