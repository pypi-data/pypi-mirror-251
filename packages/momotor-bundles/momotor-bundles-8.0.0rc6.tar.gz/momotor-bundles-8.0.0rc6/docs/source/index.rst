.. Momotor Bundles documentation master file, created by
   sphinx-quickstart on Mon Jan 20 10:13:19 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#############################
Momotor Bundles documentation
#############################

The `momotor-bundles` package contains the interfaces to read and write Momotor bundles.

A Momotor bundle is an XML document with optional attachments. Bundles without attachments can be pure XML
documents, bundles with attachments are contained in zip files.

Bundles are at the heart of a Momotor transformation, as a Momotor transformation
takes a recipe, config and product bundle as input and produces a result bundle
as output.

The recipe bundle describes the transformations that need to be performed, the config
bundle provides additional files and configuration to the recipe,
while the product bundle defines the job specific files and configuration.

In an educational setting, the recipe defines a generic way to process a student's
submission, while the config defines the assignment specific details like the
expected answers. The product contains the student's submission.

*************
Example usage
*************

Reading configuration bundle
============================

The following example loads a configuration bundle and reads an option value from it in several ways:

Considering the following `config.xml` file:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <config xmlns="http://momotor.org/1.0"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://momotor.org/1.0 http://momotor.org/schema/momotor-1.0.xsd"
           id="example-config">

       <options>
           <option name="is_this_cool"><true/></option>
           <option name="inline_text">Inline text option</option>
       </options>

       <options domain="example">
           <option name="time" type="integer" value="10" />
       </options>

   </config>

The following Python script will print the values of the options in several ways:

.. code-block:: python

   import contextlib
   from momotor.bundles import ConfigBundle

   with contextlib.closing(ConfigBundle.from_file_factory('config.xml')) as bundle:
      print('Options of', bundle.id)
      print()

      # Looping over all options and printing some attributes:
      for option in bundle.options:
          # option is of type momotor.bundles.elements.Option
          print(option.domain, option.name, repr(option.value))
      print()

      # Directly access an option using the get_option_value method:
      print('Direct access of time:', bundle.get_option_value('time', domain='example'))

Creating result bundle
======================

The following example will create a result bundle with some properties and write a `result.xml`:

.. code-block:: python

   from momotor.bundles import ResultsBundle
   from momotor.bundles.elements.results import Result
   from momotor.bundles.elements.properties import Property

   bundle = ResultsBundle()
   bundle.create(results=[
       Result(bundle).create(
           step_id='first',
           outcome='pass',
           properties=[
               Property(bundle).create(name='status', type_='string', value='OK'),
               Property(bundle).create(name='report', type_='string', value='this is the report'),
           ]
       )
   ])
   bundle.to_file('result.xml', pretty_xml=True)


########
Contents
########

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   bundles
   elements
   exceptions
   constants
   content
   filters
   utils
   binding

##################
Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
