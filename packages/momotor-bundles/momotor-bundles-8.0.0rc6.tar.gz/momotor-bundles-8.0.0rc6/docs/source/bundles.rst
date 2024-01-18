Bundles
=======

There is a class for each bundle type:
:class:`~momotor.bundles.ConfigBundle`,
:class:`~momotor.bundles.ProductBundle`,
:class:`~momotor.bundles.RecipeBundle`,
:class:`~momotor.bundles.ResultsBundle`, and
:class:`~momotor.bundles.TestResultBundle`.

All classes implement the same basic functionality to implement reading and writing bundles,
plus functionality specific to the bundle type.

:class:`~momotor.bundles.Bundle`
--------------------------------

:class:`~momotor.bundles.Bundle` is the base class from which all other bundle types extend. It provides the shared
functionality for all bundle classes.

The constructor creates a new uninitialized bundle. The
:py:meth:`~momotor.bundles.Bundle.create` method can be used to initialize a newly created bundle, the class methods
:py:meth:`~momotor.bundles.Bundle.from_bytes_factory` and
:py:meth:`~momotor.bundles.Bundle.from_file_factory`
can be used to create an initialized instance of a bundle class from an existing bundle file,
either from memory or disk.

The methods :py:meth:`~momotor.bundles.Bundle.to_buffer`, :py:meth:`~momotor.bundles.Bundle.to_directory`, and
:py:meth:`~momotor.bundles.Bundle.to_file` can be used to export a bundle to various destinations. A bundle must be
fully initialized before it can be exported.

Bundles are immutable, it's not possible to modify a bundle once it has been created, however
:py:meth:`~momotor.bundles.elements.base.Element.recreate` exists to create a new bundle based on an existing bundle
by copying elements from an existing bundle to the new bundle.

.. autoclass:: momotor.bundles.Bundle
   :members:
   :exclude-members: recreate
   :inherited-members:

:class:`~momotor.bundles.ConfigBundle`
--------------------------------------

A :class:`~momotor.bundles.ConfigBundle` contains all configuration needed by the recipe.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor_1_0.ConfigComplexType`

See the documentation of the base class :class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.ConfigBundle
   :members: create,
             id, meta,
             options, get_options, get_option_value,
             files, copy_files_to

:class:`~momotor.bundles.ProductBundle`
---------------------------------------

A :class:`~momotor.bundles.ProductBundle` contains the product to be evaluated by the recipe.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor_1_0.ProductComplexType`

See the documentation of the base class :class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.ProductBundle
   :members: create,
             id, meta,
             options, get_options, get_option_value,
             files, copy_files_to,
             properties, get_properties, get_property_value

:class:`~momotor.bundles.RecipeBundle`
--------------------------------------

A :class:`~momotor.bundles.RecipeBundle` describes the process of processing a product into a result.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor_1_0.RecipeComplexType`

See the documentation of the base class :class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.RecipeBundle
   :members: create,
             id, meta,
             steps, tests,
             options, get_options, get_option_value,
             files, copy_files_to

:class:`~momotor.bundles.ResultsBundle`
---------------------------------------

A :class:`~momotor.bundles.ResultsBundle` contains the results of the recipe applied to a product.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor_1_0.ResultsComplexType`

It also implements all methods and properties inherited :class:`~momotor.bundles.elements.results.Results`

See the documentation of the base class :class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.ResultsBundle
   :members: create,
             id, meta,
             results

.. autofunction:: momotor.bundles.results.create_error_result_bundle

:class:`~momotor.bundles.TestResultBundle`
------------------------------------------

A :class:`~momotor.bundles.TestResultBundle` contains the results of a recipe's self-test.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor_1_0.TestResultComplexType`

See the documentation of the base class :class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.TestResultBundle
   :members: create, results
