#!/usr/bin/env python

import cProfile
import os.path
import shutil
import unittest
from loot_api import Version
from loot_api import WrapperVersion
from loot_api import GameType
from loot_api import SimpleMessage
from loot_api import MessageType
from loot_api import create_database
from loot_api import is_compatible
from loot_api import set_logging_callback
from loot_api import initialise_locale

def logging_callback(level, message):
    pass

set_logging_callback(logging_callback)
initialise_locale("")

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
        self.assertTrue(is_compatible(0, 12, 0))

    def test_version(self):
        self.assertEqual(Version.major, 0)
        self.assertEqual(Version.minor, 12)
        self.assertEqual(Version.patch, 0)
        self.assertNotEqual(Version.revision, u'')
        self.assertEqual(Version.string(), "0.12.0")

    def test_wrapper_version(self):
        self.assertEqual(WrapperVersion.major, 3)
        self.assertEqual(WrapperVersion.minor, 0)
        self.assertEqual(WrapperVersion.patch, 0)
        self.assertNotEqual(WrapperVersion.revision, u'')
        self.assertNotEqual(WrapperVersion.revision, Version.revision)
        self.assertEqual(WrapperVersion.string(), "3.0.0")

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

    def test_get_plugin_messages(self):
        self.db.load_lists(self.masterlist_path, u'')

        messages = self.db.get_plugin_metadata(u'Oblivion.esm').get_simple_messages(u'en')

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].type, MessageType.error)
        self.assertEqual(messages[0].text, u'This must not be activated. However, it can be useful when porting Oblivion mods to Nehrim.')


if __name__ == '__main__':
    unittest.main()
