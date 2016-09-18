*****
Usage
*****

Installing the wrapper
======================

Build archives contain two binaries:

* ``loot_api.pyd`` is the Python wrapper
* ``loot_api.dll`` is the C++ API DLL that the Python wrapper was built against.

The C++ DLL requires the `Visual C++ 2015 Redistributable (x86)`_
to be installed.

To use the wrapper, copy both files to wherever you want to import them from
(they must be in the same folder), and you're done!

.. _Visual C++ 2015 Redistributable (x86): https://download.microsoft.com/download/9/3/F/93FCF1E7-E6A4-478B-96E7-D4B285925B00/vc_redist.x86.exe

Using the wrapper
=================

Checking Compatibility
**********************

To check if the module loaded is compatible with the version of the API that you
developed against::

  >>> import loot_api
  >>> loot_api.is_compatible(0,10,0)
  True
  >>> loot_api.is_compatible(0,9,0)
  False

Getting a Plugin's Bash Tag Suggestions
***************************************

To get a plugin's Bash Tag suggestions from a ``masterlist.yaml`` metadata file::

  >>> import loot_api
  >>> db = loot_api.create_database(loot_api.GameType.tes4, '', '')
  >>> db.load_lists('masterlist.yaml', '')
  >>> tags = db.get_plugin_tags(u'Unofficial Oblivion Patch.esp')
  >>> tags.added
  set([u'Scripts', u'Relations', u'C.Owner', u'Actors.AIPackages', u'Actors.Stats', u'Actors.ACBS', u'C.Music', u'Factions', u'Invent', u'Relev', u'Names', u'C.Light', u'Delev', u'C.Name', u'C.Climate', u'NPC.Class', u'Stats', u'Actors.DeathItem', u'Creatures.Blood', u'Actors.CombatStyle', u'Actors.AIData'])
  >>> tags.removed
  set([u'C.Water'])
  >>> tags.userlist_modified
  False
