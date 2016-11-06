*************
API Reference
*************

As this API is just a wrapper for LOOT's C++ API, its documentation is linked to
for all non-Python-specific information.

Enumerations
============

The wrapped enumeration types below are classes in Python, but the distinction
makes no difference in practice, so they're grouped here for semantics. All
values are unsigned integer constants.

.. py:class:: loot_api.GameType

  Wraps :cpp:type:`loot::GameType` to expose the LOOT API's game
  codes.

  .. py:attribute:: fo3
  .. py:attribute:: fo4
  .. py:attribute:: fonv
  .. py:attribute:: tes4
  .. py:attribute:: tes5
  .. py:attribute:: tes5se

.. py:class:: loot_api.LanguageCode

  Wraps :cpp:type:`loot::LanguageCode` to expose the LOOT API's
  language codes.

  .. py:attribute:: english
  .. py:attribute:: spanish
  .. py:attribute:: russian
  .. py:attribute:: french
  .. py:attribute:: chinese
  .. py:attribute:: polish
  .. py:attribute:: brazilian_portuguese
  .. py:attribute:: finnish
  .. py:attribute:: german
  .. py:attribute:: danish
  .. py:attribute:: korean

.. py:class:: loot_api.MessageType

  Wraps :cpp:type:`loot::MessageType` to expose the LOOT API's
  message type codes.

  .. py:attribute:: error
  .. py:attribute:: say
  .. py:attribute:: warn

.. py:class:: loot_api.PluginCleanliness

  Wraps :cpp:type:`loot::PluginCleanliness` to expose the LOOT API's plugin cleanliness state codes.

  .. py:attribute:: clean
  .. py:attribute:: dirty
  .. py:attribute:: do_not_clean
  .. py:attribute:: unknown

Public-Field Data Structures
============================

Classes with public fields and no member functions.

.. py:class:: loot_api.MasterlistInfo

  Wraps :cpp:class:`loot::MasterlistInfo`.

  .. py:attribute:: revision_id

    A Unicode string containing a Git commit's SHA-1 checksum.

  .. py:attribute:: revision_date

    A Unicode string containing the date of the commit given by :py:attr:`revision_id`, in ISO 8601 format (YYYY-MM-DD).

  .. py:attribute:: is_modified

    A boolean that is true if the masterlist has been modified from its state
    at the commit given by :py:attr:`revision_id`.

.. py:class:: loot_api.Message

  Wraps :cpp:class:`loot::SimpleMessage`.

  .. py:attribute:: type

    A :py:class:`loot_api.MessageType` giving the message type.

  .. py:attribute:: language

    A :py:class:`loot_api.LanguageCode` giving the message text language.

  .. py:attribute:: text

    A Unicode string containing the message text.

.. py:class:: loot_api.PluginTags

  Wraps :cpp:class:`loot::PluginTags`.

  .. py:attribute:: added

    A set of Unicode strings giving Bash Tags suggested for addition.

  .. py:attribute:: removed

    A set of Unicode strings giving Bash Tags suggested for removal.

  .. py:attribute:: userlist_modified

    A boolean that is true if the suggestions contain metadata obtained from a loaded userlist.


Functions
=========

.. py:function:: loot_api.is_compatible(int, int, int) -> bool

  Checks for API compatibility. Wraps :cpp:func:`loot::IsCompatible`.

.. py:function:: loot_api.create_database(game : loot_api.GameType, [game_path : unicode = u'', [game_local_path : unicode = u'']]) -> loot_api.DatabaseInterface

  Initialise a new database handle. Wraps :cpp:func:`loot::IsCompatible`.

Classes
=======

.. py:class:: loot_api.DatabaseInterface

  Wraps :cpp:class:`loot::DatabaseInterface`.

  .. py:method:: eval_lists(loot_api.DatabaseInterface) -> NoneType

    Evaluates all conditions and regular expression metadata entries in the loaded metadata lists. Wraps :cpp:func:`EvalLists`.

  .. py:method:: get_masterlist_revision(loot_api.DatabaseInterface, unicode, bool) -> loot_api.MasterlistInfo

    Gets the give masterlist’s source control revision. Wraps :cpp:func:`GetMasterlistRevision`.

  .. py:method:: get_plugin_cleanliness(loot_api.DatabaseInterface, unicode) -> loot_api.PluginCleanliness

    Determines the database’s knowledge of a plugin’s cleanliness. Wraps :cpp:func:`GetPluginCleanliness`.

  .. py:method:: get_plugin_messages(loot_api.DatabaseInterface, unicode, loot_api.LanguageCode) -> list<loot_api.Message>

    Outputs the messages associated with the given plugin in the database. Wraps :cpp:func:`GetPluginMessages`.

  .. py:method:: get_plugin_tags(loot_api.DatabaseInterface, unicode) -> loot_api.PluginTags

    Outputs the Bash Tags suggested for addition and removal by the database for the given plugin. Wraps :cpp:func:`GetPluginTags`.

  .. py:method:: load_lists(loot_api.DatabaseInterface, masterlist_path : unicode, [userlist_path : unicode = u'']) -> NoneType

    Loads the masterlist and userlist from the paths specified. Wraps :cpp:func:`LoadLists`.

  .. py:method:: sort_plugins(loot_api.DatabaseInterface, list<unicode>) -> list<unicode>

    Calculates a new load order for all a game’s installed plugins and outputs the sorted order. Wraps :cpp:func:`SortPlugins`.

  .. py:method:: update_masterlist(loot_api.DatabaseInterface, unicode, unicode, unicode) -> bool

    Updates the given masterlist using the given Git repository details. Wraps :cpp:func:`UpdateMasterlist`.

  .. py:method:: write_minimal_list(loot_api.DatabaseInterface, unicode, bool) -> NoneType

    Writes a minimal metadata file containing only Bash Tag suggestions and/or cleanliness info from the loaded metadata. Wraps :cpp:func:`WriteMinimalList`.

.. py:class:: loot_api.Version

  Wraps :cpp:class:`loot::LootVersion`.

  .. py:attribute:: major

    An unsigned integer giving the major version number.

  .. py:attribute:: minor

    An unsigned integer giving the minor version number.

  .. py:attribute:: patch

    An unsigned integer giving the patch version number.

  .. py:attribute:: revision

    A Unicode string containing the SHA-1 of the Git revision that the wrapped C++ API was built from.

  .. py:staticmethod:: string() -> unicode

    Returns the API version as a string of the form ``major.minor.patch``

.. py:class:: loot_api.WrapperVersion

  Provides information about the version of the LOOT API Python wrapper that is
  being run.

  .. py:attribute:: major

    An unsigned integer giving the major version number.

  .. py:attribute:: minor

    An unsigned integer giving the minor version number.

  .. py:attribute:: patch

    An unsigned integer giving the patch version number.

  .. py:attribute:: revision

    A Unicode string containing the SHA-1 of the Git revision that the wrapped C++ API was built from.

  .. py:staticmethod:: string() -> unicode

    Returns the API version as a string of the form ``major.minor.patch``
