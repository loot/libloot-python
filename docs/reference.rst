*************
API Reference
*************

As this API is just a wrapper for libloot's C++ API, its documentation is linked
to for all non-Python-specific information.

The wrapped enumeration types are classes in Python, but the distinction
makes no difference in practice, so they're grouped here for semantics. All
their values are unsigned integer constants.

.. automodule:: loot
    :members:
    :exclude-members: Version, WrapperVersion

.. py:class:: loot.Version

  Wraps :cpp:class:`loot::LootVersion`.

  .. py:attribute:: major

    An unsigned integer giving the major version number.

  .. py:attribute:: minor

    An unsigned integer giving the minor version number.

  .. py:attribute:: patch

    An unsigned integer giving the patch version number.

  .. py:attribute:: revision

    A Unicode string containing the SHA-1 of the Git revision that the wrapped C++ API was built from.

  .. py:staticmethod:: string() -> str

    Returns the API version as a string of the form ``major.minor.patch``

.. py:class:: loot.WrapperVersion

  Provides information about the version of libloot-python that is being run.

  .. py:attribute:: major

    An unsigned integer giving the major version number.

  .. py:attribute:: minor

    An unsigned integer giving the minor version number.

  .. py:attribute:: patch

    An unsigned integer giving the patch version number.

  .. py:attribute:: revision

    A Unicode string containing the SHA-1 of the Git revision that the wrapped C++ API was built from.

  .. py:staticmethod:: string() -> str

    Returns the API version as a string of the form ``major.minor.patch``
