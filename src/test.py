#!/usr/bin/env python

import cProfile
import unittest
from loot_api import Version
from loot_api import GameType
from loot_api import Message
from loot_api import MessageType
from loot_api import create_database
from loot_api import is_compatible

class TestLootApi(unittest.TestCase):
    def test_is_compatible(self):
        self.assertFalse(is_compatible(0, 10, 0))
        self.assertTrue(is_compatible(0, 9, 2))

    def test_version(self):
        self.assertEqual(Version.major, 0)
        self.assertEqual(Version.minor, 9)
        self.assertEqual(Version.patch, 2)
        self.assertNotEqual(Version.revision, u'')

    def test_create_db(self):
        db = create_database(GameType.tes4, u'', u'')
        self.assertNotEqual(db, None)

class TestDatabaseInterface(unittest.TestCase):
    masterlist_path = u'masterlist.yaml'

    def setUp(self):
        self.db = create_database(GameType.tes4, u'', u'')

    def test_load_lists(self):
        self.db.load_lists(self.masterlist_path, u'')

    def test_get_plugin_tags(self):
        self.db.load_lists(self.masterlist_path, u'')
        tags = self.db.get_plugin_tags(u'Unofficial Oblivion Patch.esp')

        self.assertNotEqual(tags, None)
        self.assertFalse(tags.userlist_modified)
        self.assertEqual(tags.added, set([
            u'Actors.ACBS', 
            u'Actors.AIData', 
            u'Actors.AIPackages', 
            u'Actors.CombatStyle', 
            u'Actors.DeathItem', 
            u'Actors.Stats', 
            u'C.Climate', 
            u'C.Light', 
            u'C.Music', 
            u'C.Name', 
            u'C.Owner', 
            u'Creatures.Blood', 
            u'Delev', 
            u'Factions', 
            u'Invent', 
            u'Names', 
            u'NPC.Class', 
            u'Relations', 
            u'Relev', 
            u'Scripts', 
            u'Stats'
        ]))
        self.assertEqual(tags.removed, set([u'C.Water']))

#        cProfile.runctx('self.test_get_plugin_tags_performance()', globals(), locals(), sort='cumtime')

#    def test_get_plugin_tags_performance(self):
#        self.db.load_lists(self.masterlist_path, u'')
#
#        for i in xrange(200000):
#            tags = self.db.get_plugin_tags(u'Unofficial Oblivion Patch.esp')

    def test_get_plugin_messages(self):
        self.db.load_lists(self.masterlist_path, u'')

        messages = self.db.get_plugin_messages(u'Oblivion.esm')

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].type, MessageType.error)
        self.assertEqual(messages[0].text, u'This must not be activated. However, it can be useful when porting Oblivion mods to Nehrim.')


if __name__ == '__main__':
    unittest.main()
