===================================================================
xdd2id: CANopen XML dictionary to Ingenia dictionary converter tool
===================================================================

.. image:: https://travis-ci.org/ingeniamc/xdd2id.svg?branch=master
    :target: https://travis-ci.org/ingeniamc/xdd2id
    :alt: Build Status

.. image:: https://img.shields.io/pypi/v/xdd2id.svg
    :target: https://pypi.python.org/pypi/xdd2id
    :alt: PyPI Version

.. image:: https://api.codacy.com/project/badge/Grade/d8384ef1e0f148c1b92b012b482044ce
    :target: https://www.codacy.com/app/gmarull/xdd2id
    :alt: Code Quality

``xdd2id`` is a tool to convert CANopen XML dictionaries (XDD) to the
IngeniaDictionary format.

Installation
------------

You will need to have Python (2.7, >=3.4) installed. Then, the recommended way
to install ``xdd2id`` is by using ``pip``, i.e::

    pip install xdd2id


Usage
-----

A standalone command line tool will be installed which can be used like this::

        xdd2id -i Dictionary.xdd -o IngeniaDictionary.xml

Or, if you prefer, it can also be used on your Python code like this::

        import xdd2id

        xdd2id.convert('Dictionary.xdd', 'IngeniaDictionary.xml')

