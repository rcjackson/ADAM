Welcome to ATMOS Analogue Digital Twin (ADAM)'s documentation!
==============================================================

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: :octicon:`book;10em`
        :link: user_guide/index
        :link-type: doc
        :text-align: center

        **User Guide**

        The cookbook provides in-depth information on how
        to use ADAM, including how to get started.
        This is where to look for general conceptual descriptions on how
        to use parts of ADAM, including how to make your first lake breeze front and
        the required data preprocessing to do so.

    .. grid-item-card:: :octicon:`list-unordered;10em`
        :link: dev_reference/index
        :link-type: doc
        :text-align: center

        **Reference Guide**

        The reference guide contains detailed descriptions on
        every function and class within ADAM. This is where to turn to understand
        how to use a particular feature or where to search for a specific tool

    .. grid-item-card:: :octicon:`terminal;10em`
        :link: contributors_guide/index
        :link-type: doc
        :text-align: center

        **Developer Guide**

        Want to help make ADAM better? Found something
        that's not working quite right? You can find instructions on how to
        contribute to ADAM here. You can also find detailed descriptions on
        tools useful for developing ADAM.

    .. grid-item-card:: :octicon:`graph;10em`
        :link: source/auto_examples/index
        :link-type: doc
        :text-align: center

        **Example Gallery**

        Check out ADAM's gallery of examples which contains
        sample code demonstrating various parts of ADAM's functionality.

============
Installation
============


Stable release
--------------

To install the Argonne Testbed for Multiscale Observational Studies (ATMOS)
Analogue Digital Twin, run this command in your terminal:

.. code-block:: console

    $ pip install adam

This is the preferred method to install the ATMOS Analogue Digital Twin,
as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for ATMOS Analogue Digital Twin can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/rcjackson/adam

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/rcjackson/adam/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/rcjackson/adam
.. _tarball: https://github.com/rcjackson/adam/tarball/master

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
