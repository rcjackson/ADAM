===========================
ATMOS Analogue Digital Twin
===========================


.. image:: https://img.shields.io/pypi/v/adam.svg
        :target: https://pypi.python.org/pypi/adam

.. image:: https://readthedocs.org/projects/adam/badge/?version=latest
        :target: https://adam.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/rcjackson/adam/shield.svg
     :target: https://pyup.io/repos/github/rcjackson/adam/
     :alt: Updates




ADAM is the ATMOS Analogue Digital Twin, a Python package that provides tools and predictive models for analyzing lake breezes using NEXRAD radar data.
This initial package contains a model that determines the lake breeze front location from the 0.5 degree scan of the NEXRAD radar.

Installation
------------

The recommended way to install ADAM is via pip. This will ensure you get the latest stable release and 
all required dependencies:

.. code-block:: console

        pip install adam

Getting Started
---------------

After installation, you can import ADAM in your Python scripts or notebooks:

.. code-block:: python

        import adam

ADAM includes a predictive model for detecting and analyzing lake breezes from NEXRAD radar data.
See the documentation and example notebooks for usage details.

Links
-----

- Documentation: https://rcjackson.github.io/adam/
- Source code: https://github.com/rcjackson/adam


* Free software: BSD license
* Documentation: https://adam.readthedocs.io.


Features
--------

* Lake breeze detection from NEXRAD radar data using deep learning models.
* Easy-to-use API for loading and processing radar data.
* Example notebooks demonstrating functionality.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
