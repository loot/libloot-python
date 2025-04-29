*****
Usage
*****

Installing the wrapper
======================

Build archives contain two binaries:

* ``loot.*.pyd`` is the Python wrapper
* ``loot.dll`` is the C++ library DLL that the Python wrapper was built against.

The C++ DLL requires the `Visual C++ 2022 Redistributable (x86)`_
to be installed.

To use the wrapper, copy both files to wherever you want to import them from
(they must be in the same folder), and you're done!

.. _Visual C++ 2022 Redistributable (x86): https://aka.ms/vs/17/release/vc_redist.x86.exe

Using the wrapper
=================

Checking Compatibility
**********************

To check if the module loaded is compatible with the version of the API that you
developed against::

  >>> import loot
  >>> loot.is_compatible(0,14,0)
  True
  >>> loot.is_compatible(0,9,0)
  False

Getting a Plugin's Bash Tag Suggestions
***************************************

To get a plugin's Bash Tag suggestions from a ``masterlist.yaml`` metadata file::

  >>> import loot
  >>> db = loot.create_game_handle(loot.GameType.tes4, 'C:\\path\\to\\oblivion\\directory')
  >>> db.load_lists('masterlist.yaml')
  >>> tags = db.get_plugin_tags(u'Unofficial Oblivion Patch.esp')
  >>> tags.added
  set([u'Scripts', u'Relations', u'C.Owner', u'Actors.AIPackages', u'Actors.Stats', u'Actors.ACBS', u'C.Music', u'Factions', u'Invent', u'Relev', u'Names', u'C.Light', u'Delev', u'C.Name', u'C.Climate', u'NPC.Class', u'Stats', u'Actors.DeathItem', u'Creatures.Blood', u'Actors.CombatStyle', u'Actors.AIData'])
  >>> tags.removed
  set([u'C.Water'])
  >>> tags.userlist_modified
  False
