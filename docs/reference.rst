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

  Wraps :cpp:type:`loot::GameType` to expose the LOOT API's game codes.

  .. py:attribute:: fo3
  .. py:attribute:: fo4
  .. py:attribute:: fonv
  .. py:attribute:: tes4
  .. py:attribute:: tes5
  .. py:attribute:: tes5se

.. py:class:: loot_api.LogLevel

  Wraps :cpp:type:`loot::LogLevel` to expose the LOOT API's log level codes.

  .. py:attribute:: trace
  .. py:attribute:: debug
  .. py:attribute:: info
  .. py:attribute:: warning
  .. py:attribute:: error
  .. py:attribute:: fatal

.. py:class:: loot_api.MessageType

  Wraps :cpp:type:`loot::MessageType` to expose the LOOT API's message type
  codes.

  .. py:attribute:: error
  .. py:attribute:: say
  .. py:attribute:: warn

.. py:class:: loot_api.PluginCleanliness

  Codes used to indicate the cleanliness of a plugin according to the
  information contained within the loaded masterlist/userlist.

  .. py:attribute:: clean

    Indicates that the plugin is clean.

  .. py:attribute:: dirty

    Indicates that the plugin is dirty.

  .. py:attribute:: do_not_clean

    Indicates that the plugin contains dirty edits, but that they are part of
    the plugin’s intended functionality and should not be removed.

  .. py:attribute:: unknown

    Indicates that no data is available on whether the plugin is dirty or not.

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

.. py:class:: loot_api.SimpleMessage

  Wraps :cpp:class:`loot::SimpleMessage`.

  .. py:attribute:: type

    A :py:class:`loot_api.MessageType` giving the message type.

  .. py:attribute:: language

    A Unicode string giving the message text language.

  .. py:attribute:: text

    A Unicode string containing the message text.

  .. py:attribute:: condition

    A Unicode string containing the message condition.

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

.. py:function:: loot_api.set_logging_callback(callback) -> NoneType

  Set the callback function that is called when logging. Wraps
  :cpp:func:`loot::SetLoggingCallback`.

.. py:function:: loot_api.is_compatible(int, int, int) -> bool

  Checks for API compatibility. Wraps :cpp:func:`loot::IsCompatible`.

.. py:function:: loot_api.InitialiseLocale(unicode) -> NoneType

  Initialise the current global locale using the given ID. Wraps
  :cpp:func:`loot::InitialiseLocale`.

.. py:function:: loot_api.create_game_handle(game : loot_api.GameType, [game_path : unicode = u'', [game_local_path : unicode = u'']]) -> loot_api.GameInterface

  Initialise a new game handle. Wraps :cpp:func:`loot::CreateGameHandle`.

Classes
=======

.. py:class:: loot_api.GameInterface

  Wraps :cpp:class:`loot::GameInterface`.

  .. py:function:: loot_api.get_database() -> loot_api.DatabaseInterface

    Get a database handle. Wraps :cpp:func:`loot::GetDatabase`.

  .. py:function:: loot_api.load_current_load_order_state() -> NoneType

    Load the current load order state, discarding any previously held state.
    Wraps :cpp:func:`loot::LoadCurrentLoadOrderState`.

.. py:class:: loot_api.DatabaseInterface

  Wraps :cpp:class:`loot::DatabaseInterface`.

  .. py:method:: get_masterlist_revision(loot_api.DatabaseInterface, unicode, bool) -> loot_api.MasterlistInfo

    Gets the give masterlist’s source control revision. Wraps :cpp:func:`GetMasterlistRevision`.

  .. py:method:: get_plugin_metadata(loot_api.DatabaseInterface, plugin : unicode, [includeUserMetadata : bool = True, [evaluateConditions : bool = False]]) -> loot_api.PluginMetadata

    Get all a plugin’s loaded metadata. Wraps :cpp:func:`GetPluginMetadata`.

  .. py:method:: get_plugin_cleanliness(loot_api.DatabaseInterface, plugin : unicode, [evaluateConditions : bool = False]) -> loot_api.PluginCleanliness

    Determines the database’s knowledge of a plugin’s cleanliness. Outputs whether the plugin should be cleaned or not, or if no data is available.

  .. py:method:: get_plugin_tags(loot_api.DatabaseInterface, plugin : unicode, [evaluateConditions : bool = False]) -> loot_api.PluginTags

    Outputs the Bash Tags suggested for addition and removal by the database for the given plugin.

  .. py:method:: load_lists(loot_api.DatabaseInterface, masterlist_path : unicode, [userlist_path : unicode = u'']) -> NoneType

    Loads the masterlist and userlist from the paths specified. Wraps :cpp:func:`LoadLists`.

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

.. py:class:: loot_api.PluginMetadata

  Wraps :cpp:class:`loot::PluginMetadata`.

  .. py:method:: get_simple_messages(loot_api.PluginMetadata, unicode) -> list<loot_api.SimpleMessage>

    Get the plugin’s messages as SimpleMessage objects for the given language.
    Wraps :cpp:func:`GetPluginMessages`.
