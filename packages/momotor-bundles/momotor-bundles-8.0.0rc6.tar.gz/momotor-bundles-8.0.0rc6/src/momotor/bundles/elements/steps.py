from __future__ import annotations

import dataclasses
import typing
import warnings
from enum import IntEnum
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import DependsComplexType, StepComplexType, DependenciesComplexType, \
    StepsComplexType, RecipeComplexType, StepComplexTypePriority, CheckletComplexType
from momotor.bundles.elements.base import Element, NestedElement
from momotor.bundles.elements.checklets import Checklet, CheckletMixin
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.meta import MetaMixin, Meta
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.resources import ResourcesMixin, Resource, ResourcesType
from momotor.bundles.mixins.id import IdMixin
from momotor.bundles.utils.assertion import assert_elements_instanceof
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.filters import FilterableTuple
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['Priority', 'Depends', 'Step']


class Priority(IntEnum):
    """ An enum for the step priority """
    MUST_PASS = 0
    HIGH = 1
    NORMAL = 2
    DEFAULT = 2
    LOW = 3


# Map StepComplexTypePriority to Priority
PRIORITY_LEVEL_MAP: dict[StepComplexTypePriority, Priority] = {
    StepComplexTypePriority.MUST_PASS: Priority.MUST_PASS,
    StepComplexTypePriority.HIGH: Priority.HIGH,
    StepComplexTypePriority.DEFAULT: Priority.DEFAULT,
    StepComplexTypePriority.NORMAL: Priority.NORMAL,
    StepComplexTypePriority.LOW: Priority.LOW,
}


class Depends(Element[DependsComplexType]):
    # noinspection PyUnresolvedReferences
    """ A Depends element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.DependsComplexType`
    """

    __unset: typing.ClassVar = object()
    _step: str | None = __unset

    @typing.final
    @property
    def step(self) -> str:
        """ `step` attribute """
        assert self._step is not self.__unset, "Uninitialized attribute `step`"
        return self._step

    @step.setter
    def step(self, step: str):
        assert self._step is self.__unset, "Immutable attribute `step`"
        assert isinstance(step, str)
        self._step = step

    @staticmethod
    def get_node_type() -> type[DependsComplexType]:
        return DependsComplexType

    def create(self, *, step: str) -> Self:
        self.step = step
        return self

    # noinspection PyMethodOverriding
    def recreate(self, target_bundle: "momotor.bundles.Bundle") -> "Depends":
        """ Recreate this :py:class:`Depends` in a target bundle.
        All attributes are copied unchanged.

        :param target_bundle: The target bundle
        :return: The recreated :py:class:`Depends`
        """
        return Depends(target_bundle).create(step=self.step)

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: DependsComplexType, *, args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)

        return self.create(step=node.step)

    def _construct_node(self, *, args: BundleConstructionArguments) -> DependsComplexType:
        return DependsComplexType(step=self.step)


if Depends.__doc__ and Element.__doc__:
    Depends.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


class Step(
    NestedElement[StepComplexType, StepsComplexType],
    CheckletMixin[StepComplexType],
    IdMixin, MetaMixin, OptionsMixin, FilesMixin, ResourcesMixin,
):
    """ A Step element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.StepComplexType`
    """
    __unset: typing.ClassVar = object()
    _priority: StepComplexTypePriority | None = __unset
    _depends: FilterableTuple[Depends] | None = __unset
    _checklet: Checklet | None = __unset
    _merged_resources = None

    @typing.final
    @property
    def priority(self) -> str:
        """ `priority` attribute """
        assert self._priority is not self.__unset, "Uninitialized attribute `priority`"
        return typing.cast(str, self._priority.value)

    @priority.setter
    def priority(self, priority: str):
        assert self._priority is self.__unset, "Immutable attribute `priority`"
        assert isinstance(priority, str)

        try:
            priority_enum = StepComplexTypePriority(priority)
        except ValueError:
            warnings.warn(f"Invalid priority attribute value '{priority}' ignored (will use 'default")
            priority_enum = StepComplexTypePriority.DEFAULT

        self._priority = priority_enum

    @typing.final
    @property
    def depends(self) -> FilterableTuple[Depends] | None:
        """ `depends` """
        assert self._depends is not self.__unset, "Uninitialized attribute `depends`"
        return self._depends

    @depends.setter
    def depends(self, depends: typing.Iterable[Depends] | None):
        assert self._depends is self.__unset, "Immutable attribute `depends`"
        if depends is not None:
            self._depends = assert_elements_instanceof(FilterableTuple(depends), Depends, self.bundle)
        else:
            self._depends = None

    @typing.final
    @property
    def checklet(self) -> Checklet | None:
        """ `checklet` """
        assert self._checklet is not self.__unset, "Uninitialized attribute `checklet`"
        return self._checklet

    @checklet.setter
    def checklet(self, checklet: Checklet | None):
        assert self._checklet is self.__unset, "Immutable attribute `checklet`"
        assert checklet is None or (isinstance(checklet, Checklet) and checklet.bundle == self.bundle)
        self._checklet = checklet
        self._resources_updated()

    def _resources_updated(self):
        super()._resources_updated()
        self._merged_resources = None

    @staticmethod
    def get_node_type() -> type[StepComplexType]:
        return StepComplexType

    @staticmethod
    def _get_parent_type() -> type[StepsComplexType]:
        return StepsComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str,
               meta: Meta | None = None,
               priority: str = 'default',
               depends: typing.Iterable[Depends] | None = None,
               checklet: Checklet | None = None,
               options: typing.Iterable[Option] | None = None,
               files: typing.Iterable[File] | None = None,
               resources: typing.Iterable[Resource] | None = None) -> Self:

        self.id = id
        self.priority = priority
        self.meta = meta
        self.depends = depends
        self.checklet = checklet
        self.options = options
        self.files = files
        self.resources = resources
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", *, id: str | None = None) -> "Step":
        """ Recreate this :py:class:`Step` in a target bundle, optionally changing the `id`.
        All other attributes are copied unchanged.

        :param target_bundle: The target bundle
        :param id: New id for the step
        :return: The recreated :py:class:`Step`
        """
        return Step(target_bundle).create(
            id=id or self.id,
            priority=self.priority,
            meta=self.meta,
            depends=Depends.recreate_list(self.depends, target_bundle),
            checklet=self.checklet.recreate(target_bundle) if self.checklet else None,
            options=Option.recreate_list(self.options, target_bundle),
            files=File.recreate_list(self.files, target_bundle),
            resources=Resource.recreate_list(self.resources, target_bundle),
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: StepComplexType, steps: StepsComplexType, recipe: RecipeComplexType, *,
                          args: BundleFactoryArguments) -> Self:
        # recipe > steps > step
        #
        # step has <files> children
        #  - file.ref can refer to file in recipe.files
        #
        # step has single <checklet> child
        #  - checklet.ref can refer to checklet in steps.checklets or recipe.checklets

        self._check_node_type(node)
        self._check_parent_type(steps)
        # self._check_node_type(recipe, RecipeComplexType)

        return self.create(
            id=node.id,
            priority=node.priority.value,
            meta=self._collect_meta(node, args=args),
            depends=self._collect_depends(node, args=args),
            checklet=self._collect_checklet(node, [steps.checklets, recipe.checklets], args=args),
            options=self._collect_options(node, [steps.options, recipe.options], args=args),
            files=self._collect_files(node, [recipe.files], args=args),
            resources=self._collect_resources(node, args=args)
        )

    def _collect_depends(self, node: StepComplexType, *,
                         args: BundleFactoryArguments) -> typing.Generator[Depends, None, None]:
        for tag_name, child in get_nested_complex_nodes(node, 'dependencies', 'depends'):
            if tag_name == 'depends':
                # noinspection PyProtectedMember
                yield Depends(self.bundle)._create_from_node(node=typing.cast(DependsComplexType, child), args=args)

    def _construct_node(self, *, args: BundleConstructionArguments) -> StepComplexType:
        child_args = dataclasses.replace(args, generator_name=False)
        return StepComplexType(
            id=self.id,
            priority=self._priority,
            meta=list(self._construct_meta_node(args=args)),
            dependencies=list(self._construct_dependencies_nodes(args=child_args)),
            checklet=list(self._construct_checklet_nodes(args=child_args)),
            options=list(self._construct_options_nodes(args=child_args)),
            files=list(self._construct_files_nodes(PurePosixPath('step', self.id), args=child_args)),
            resources=list(self._construct_resources_nodes(args=child_args)),
        )

    def _construct_dependencies_nodes(self, *, args: BundleConstructionArguments) \
            -> typing.Generator[DependenciesComplexType, None, None]:
        depends = self.depends
        if depends:
            yield DependenciesComplexType(depends=[
                dep._construct_node(args=args)
                for dep in depends
            ])

    def _construct_checklet_nodes(self, *, args: BundleConstructionArguments) \
            -> typing.Generator[CheckletComplexType, None, None]:
        checklet = self.checklet
        if checklet:
            # noinspection PyProtectedMember
            yield self.checklet._construct_node(args=args)

    @property
    def priority_value(self) -> Priority:
        """ `priority` attribute as :py:class:`Priority` instance """
        return PRIORITY_LEVEL_MAP.get(self._priority)

    def get_dependencies_ids(self) -> typing.Generator[str, None, None]:
        """ ids of the dependencies """
        if self.depends:
            for depend in self.depends:
                yield depend.step

    def get_resources(self) -> dict[str, ResourcesType]:
        """ get all resources needed by this step """
        if self._merged_resources is None:
            merged_resources = self._get_resources().copy()
            if self.checklet:
                for name, resources in self.checklet.get_resources().items():
                    if name in merged_resources:
                        merged_resources[name] += resources
                    else:
                        merged_resources[name] = resources

            self._merged_resources = merged_resources

        return self._merged_resources


if Step.__doc__ and Element.__doc__:
    Step.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
