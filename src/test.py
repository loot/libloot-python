#!/usr/bin/env python

import cProfile
import os.path
import shutil
import unittest
from loot_api import Version
from loot_api import WrapperVersion
from loot_api import GameType
from loot_api import LanguageCode
from loot_api import Message
from loot_api import MessageType
from loot_api import create_database
from loot_api import is_compatible

class GameFixture(unittest.TestCase):
    game_path = os.path.join(u'.', u'Oblivion')
    local_path = os.path.join(u'.', u'local')

    def setUp(self):
        data_path = os.path.join(self.game_path, 'Data')
        master_file = os.path.join(data_path, 'Oblivion.esm')

        os.makedirs(data_path)
        open(master_file, 'a').close()

        os.makedirs(self.local_path)

    def tearDown(self):
        shutil.rmtree(self.game_path)
        shutil.rmtree(self.local_path)

class TestLootApi(GameFixture):
    def test_is_compatible(self):
        self.assertFalse(is_compatible(0, 9, 0))
        self.assertTrue(is_compatible(0, 10, 0))

    def test_version(self):
        self.assertEqual(Version.major, 0)
        self.assertEqual(Version.minor, 10)
        self.assertEqual(Version.patch, 0)
        self.assertNotEqual(Version.revision, u'')
        self.assertEqual(Version.string(), "0.10.0")

    def test_wrapper_version(self):
        self.assertEqual(WrapperVersion.major, 1)
        self.assertEqual(WrapperVersion.minor, 0)
        self.assertEqual(WrapperVersion.patch, 1)
        self.assertNotEqual(WrapperVersion.revision, u'')
        self.assertNotEqual(WrapperVersion.revision, Version.revision)
        self.assertEqual(WrapperVersion.string(), "1.0.1")

    def test_create_db(self):
        db = create_database(GameType.tes4, self.game_path, self.local_path)
        self.assertNotEqual(db, None)

class TestDatabaseInterface(GameFixture):
    masterlist_path = u'masterlist.yaml'

    def setUp(self):
        super(TestDatabaseInterface, self).setUp()

        self.db = create_database(GameType.tes4, self.game_path, self.local_path)

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

        messages = self.db.get_plugin_messages(u'Oblivion.esm', LanguageCode.english)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].type, MessageType.error)
        self.assertEqual(messages[0].text, u'This must not be activated. However, it can be useful when porting Oblivion mods to Nehrim.')


if __name__ == '__main__':
    unittest.main()
