*************
API Reference
*************

As this API is just a wrapper for LOOT's C++ API, its documentation is linked to
for all non-Python-specific information.

Enumerations
============

The wrapped enumeration types below are classes in Python, but the distinction
makes no difference in practice, so they're grouped here for semantics.

.. autoclass:: loot_api.GameType
   :members:
   :undoc-members:

.. autoclass:: loot_api.LanguageCode
   :members:
   :undoc-members:

.. autoclass:: loot_api.MessageType
   :members:
   :undoc-members:

.. autoclass:: loot_api.PluginCleanliness
   :members:
   :undoc-members:

Public-Field Data Structures
============================

Classes with public fields and no member functions.

.. autoclass:: loot_api.MasterlistInfo
   :members:
   :undoc-members:

.. autoclass:: loot_api.Message
   :members:
   :undoc-members:

.. autoclass:: loot_api.PluginTags
   :members:
   :undoc-members:


Functions
=========

.. autofunction:: loot_api.is_compatible

.. autofunction:: loot_api.create_database

Classes
=======

.. autoclass:: loot_api.DatabaseInterface
   :members:

.. autoclass:: loot_api.Version
   :members:
   :undoc-members:
