from __future__ import annotations

import dataclasses
import typing

import momotor.bundles
from momotor.bundles.base import Bundle
from momotor.bundles.binding import Product as ProductRootType
from momotor.bundles.const import BundleCategory
from momotor.bundles.elements.meta import MetaMixin, Meta
from momotor.bundles.mixins.id import IdMixin
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.properties import Property, PropertiesMixin
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['ProductBundle']


class ProductBundle(Bundle[ProductRootType], IdMixin, MetaMixin, OptionsMixin, FilesMixin, PropertiesMixin):
    """ A product bundle. This implements the interface to create and access Momotor product files
    """
    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str | None = None,
               meta: Meta | None = None,
               options: typing.Iterable[Option] | None = None,
               files: typing.Iterable[File] | None = None,
               properties: typing.Iterable[Property] | None = None) -> Self:
        """ Set all attributes for this ProductBundle

        Usage:

        .. code-block:: python

           product = ProductBundle(...).create(id, meta, options, files, properties)

        :param id: `id` of the bundle (optional)
        :param meta: `meta` of the bundle (optional)
        :param options: list of options (optional)
        :param files: list of files (optional)
        :param properties: list of properties (optional)
        :return: self
        """
        self.id = id
        self.meta = meta
        self.options = options
        self.files = files
        self.properties = properties
        return self

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ProductRootType, *, args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)

        return self.create(
            id=node.id,
            meta=self._collect_meta(node, args=args),
            options=self._collect_options(node, [], args=args),
            files=self._collect_files(node, [], args=args),
            properties=self._collect_properties(node, args=args),
        )

    def _construct_node(self, *, args: BundleConstructionArguments) -> ProductRootType:
        child_args = dataclasses.replace(args, generator_name=False)
        return ProductRootType(
            id=self.id,
            meta=list(self._construct_meta_node(args=args)),
            options=list(self._construct_options_nodes(args=child_args)),
            files=list(self._construct_files_nodes(args=child_args)),
            properties=list(self._construct_properties_nodes(args=child_args)),
        )

    @staticmethod
    def get_node_type() -> type[ProductRootType]:
        return ProductRootType

    @staticmethod
    def get_default_xml_name():
        """ Get the default XML file name

        :return: 'product.xml'
        """
        return 'product.xml'

    @staticmethod
    def get_category():
        """ Get the category for this bundle

        :return: :py:const:`BundleCategory.PRODUCT`
        """
        return BundleCategory.PRODUCT


# Extend the docstring with the generic documentation of Bundle
if ProductBundle.__doc__ and Bundle.__doc__:
    ProductBundle.__doc__ += "\n".join(Bundle.__doc__.split("\n")[1:])
