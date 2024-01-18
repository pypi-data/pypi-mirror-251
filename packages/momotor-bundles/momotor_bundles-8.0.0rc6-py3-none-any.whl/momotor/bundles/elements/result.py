from __future__ import annotations

import enum
import typing
import warnings
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import ResultComplexType, ResultsComplexType, OutcomeSimpleType
from momotor.bundles.elements.base import NestedElement, Element
from momotor.bundles.elements.files import FilesMixin, File
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.properties import PropertiesMixin, Property
from momotor.bundles.exception import BundleFormatError
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['Result', 'Outcome', 'OutcomeLiteral', 'create_error_result']


OutcomeLiteral: TypeAlias = typing.Literal['pass', 'fail', 'skip', 'error']


class Outcome(enum.Enum):
    """ An enum for the :py:attr:`Result.outcome`.
    Mirrors :py:class:`~momotor.bundles.binding.momotor_1_0.OutcomeSimpleType`
    """
    PASS = 'pass'
    FAIL = 'fail'
    SKIP = 'skip'
    ERROR = 'error'

    @classmethod
    def from_simpletype(cls, st: OutcomeSimpleType) -> Self:
        """ Create an :py:class:`Outcome` from an :py:class:`~momotor.bundles.binding.momotor_1_0.OutcomeSimpleType`
        """
        return cls(st.value)

    def to_simpletype(self) -> OutcomeSimpleType:
        """ Convert into an :py:class:`~momotor.bundles.binding.momotor_1_0.OutcomeSimpleType`
        """
        return OutcomeSimpleType(self.value)

    @classmethod
    def condition(cls, state: typing.Any) -> Self:
        """ Get outcome based on a condition

        :return: returns :py:attr:`Outcome.PASS` if state is truthy, otherwise returns :py:attr:`Outcome.FAIL`
        """
        return cls.PASS if state else cls.FAIL


class Result(
    NestedElement[ResultComplexType, ResultsComplexType],
    PropertiesMixin, OptionsMixin, FilesMixin
):
    """ A Result element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.ResultComplexType`
    """
    __unset: typing.ClassVar = object()

    _step_id: str = __unset
    _outcome: Outcome = __unset
    _parent_id: str | None = __unset

    @typing.final
    @property
    def step_id(self) -> str:
        """ `step_id` attribute """
        assert self._step_id is not self.__unset, "Uninitialized attribute `step_id`"
        return self._step_id

    @step_id.setter
    def step_id(self, step_id: str):
        assert self._step_id is self.__unset, "Immutable attribute `step_id`"
        assert isinstance(step_id, str)
        self._step_id = step_id

    @typing.final
    @property
    def outcome(self) -> OutcomeLiteral:
        """ `outcome` attribute as string value. Valid values are ``pass``, ``fail``, ``skip`` and ``error`` """
        assert self._outcome is not self.__unset, "Uninitialized attribute `outcome`"
        return typing.cast(OutcomeLiteral, self._outcome.value)

    @outcome.setter
    def outcome(self, outcome: OutcomeLiteral | OutcomeSimpleType | Outcome):
        assert self._outcome is self.__unset, "Immutable attribute `outcome`"

        assert isinstance(outcome, (str, OutcomeSimpleType, Outcome))

        try:
            if isinstance(outcome, Outcome):
                outcome_enum = outcome
            elif isinstance(outcome, OutcomeSimpleType):
                # noinspection PyProtectedMember
                outcome_enum = Outcome.from_simpletype(outcome)
            else:
                outcome_enum = Outcome(outcome)

        except (TypeError, ValueError):
            warnings.warn(f"Invalid outcome attribute value '{outcome}' ignored (will use 'error')")
            outcome_enum = Outcome.ERROR

        self._outcome = outcome_enum

    @typing.final
    @property
    def outcome_enum(self) -> Outcome:
        """ `outcome` attribute as an :py:class:`~momotor.bundles.elements.result.Outcome` enum """
        assert self._outcome is not self.__unset, "Uninitialized attribute `outcome`"
        return self._outcome

    def set_parent_id(self, parent_id: str | None):
        """ Set the id of the result parent """
        assert self._parent_id is self.__unset, "Immutable attribute `parent_id`"
        if parent_id:
            assert isinstance(parent_id, str)
            self._parent_id = parent_id
        else:
            self._parent_id = None

    @staticmethod
    def get_node_type() -> type[ResultComplexType]:
        return ResultComplexType

    @staticmethod
    def _get_parent_type() -> type[ResultsComplexType]:
        return ResultsComplexType

    def create(self, *,
               step_id: str,
               outcome: str | Outcome,
               properties: typing.Iterable[Property] | None = None,
               options: typing.Iterable[Option] | None = None,
               files: typing.Iterable[File] | None = None,
               parent_id: str | None = None) -> Self:

        self.set_parent_id(parent_id)
        self.step_id = step_id
        self.outcome = outcome
        self.properties = properties
        self.options = options
        self.files = files
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", *, step_id: str | None = None) -> "Result":
        """ Recreate this :py:class:`Result` in a target bundle, optionally changing the `step_id`.
        All other attributes are copied unchanged.

        :param target_bundle: The target bundle
        :param step_id: New step_id for the result
        :return: The recreated :py:class:`Result`
        """
        return Result(target_bundle).create(
            step_id=step_id or self.step_id,
            outcome=self.outcome,
            properties=Property.recreate_list(self.properties, target_bundle),
            options=Option.recreate_list(self.options, target_bundle),
            files=File.recreate_list(self.files, target_bundle),
            parent_id=self._parent_id,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ResultComplexType, results: ResultsComplexType | None = None, *,
                          args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)
        self._check_parent_type(results, True)

        if node.checklet and not args.legacy:
            msg = '`checklet` in result nodes has been removed'
            if args.validate_xml:
                raise BundleFormatError(msg)
            else:
                warnings.warn(msg)

        return self.create(
            step_id=node.step,
            outcome=typing.cast(str, node.outcome.value),
            properties=self._collect_properties(node, args=args),
            options=self._collect_options(node, [], args=args),
            files=self._collect_files(node, [], args=args),
            parent_id=results.id if results else None,
        )

    def _construct_node(self, *, args: BundleConstructionArguments) -> ResultComplexType:
        # noinspection PyProtectedMember
        return ResultComplexType(
            step=self.step_id,
            outcome=self._outcome.to_simpletype(),
            properties=list(self._construct_properties_nodes(args=args)),
            options=list(self._construct_options_nodes(args=args)),
            files=list(self._construct_files_nodes(PurePosixPath('result', self.step_id), args=args)),
        )

    @typing.final
    @property
    def passed(self) -> bool:
        """ Returns True if `outcome` is ``pass`` """
        return self.outcome_enum == Outcome.PASS

    @typing.final
    @property
    def failed(self) -> bool:
        """ Returns True if `outcome` is ``fail`` """
        return self.outcome_enum == Outcome.FAIL

    @typing.final
    @property
    def skipped(self) -> bool:
        """ Returns True if `outcome` is ``skip`` """
        return self.outcome_enum == Outcome.SKIP

    @typing.final
    @property
    def erred(self) -> bool:
        """ Returns True if `outcome` is ``error`` """
        return self.outcome_enum == Outcome.ERROR


if Result.__doc__ and Element.__doc__:
    Result.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


def create_error_result(bundle: "momotor.bundles.ResultsBundle", result_id: str, status: str, report: str | None = None,
                        **properties) -> Result:
    """ Create an error result """
    properties = {
        'status': status,
        'report': report,
        **properties
    }

    return Result(bundle).create(
        step_id=result_id,
        outcome=Outcome.ERROR,
        properties=[
            Property(bundle).create(name=key, value=value)
            for key, value in properties.items()
            if value is not None
        ]
    )
