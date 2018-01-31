===================================================================
xdd2id: CANopen XML dictionary to Ingenia dictionary converter tool
===================================================================

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

