#!/usr/bin/env python

import cProfile
import os
import os.path
import shutil
import sys
import unittest

sys.path.append(os.getcwd())

from loot_api import Version
from loot_api import WrapperVersion
from loot_api import GameType
from loot_api import SimpleMessage
from loot_api import MessageType
from loot_api import PluginCleanliness
from loot_api import create_game_handle
from loot_api import is_compatible
from loot_api import set_logging_callback
from loot_api import initialise_locale

def logging_callback(level, message):
    pass

set_logging_callback(logging_callback)
initialise_locale()

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
        self.assertTrue(is_compatible(0, 14, 0))

    def test_version(self):
        self.assertEqual(Version.major, 0)
        self.assertEqual(Version.minor, 14)
        self.assertEqual(Version.patch, 5)
        self.assertNotEqual(Version.revision, u'')
        self.assertEqual(Version.string(), "0.14.5")

    def test_wrapper_version(self):
        self.assertEqual(WrapperVersion.major, 4)
        self.assertEqual(WrapperVersion.minor, 0)
        self.assertEqual(WrapperVersion.patch, 1)
        self.assertNotEqual(WrapperVersion.revision, u'')
        self.assertNotEqual(WrapperVersion.revision, Version.revision)
        self.assertEqual(WrapperVersion.string(), "4.0.1")

    def test_create_db(self):
        game = create_game_handle(GameType.tes4, self.game_path, self.local_path)
        db = game.get_database()
        self.assertNotEqual(db, None)

class TestDatabaseInterface(GameFixture):
    masterlist_path = os.path.join(os.path.dirname(__file__), u'masterlist.yaml')

    def setUp(self):
        super(TestDatabaseInterface, self).setUp()

        game = create_game_handle(GameType.tes4, self.game_path, self.local_path)
        game.load_current_load_order_state()

        self.db = game.get_database()

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

    def test_get_plugin_cleanliness_should_be_unknown_if_no_dirty_or_clean_metadata_exists(self):
        self.db.load_lists(self.masterlist_path, u'')

        cleanliness = self.db.get_plugin_cleanliness(u'unknown.esp')

        self.assertEqual(cleanliness, PluginCleanliness.unknown)

    def test_get_plugin_cleanliness_should_be_unknown_if_dirty_and_clean_metadata_exists(self):
        self.db.load_lists(self.masterlist_path, u'')

        cleanliness = self.db.get_plugin_cleanliness(u'clean_and_dirty.esp')

        self.assertEqual(cleanliness, PluginCleanliness.unknown)

    def test_get_plugin_cleanliness_should_be_clean_if_only_clean_metadata_exists(self):
        self.db.load_lists(self.masterlist_path, u'')

        cleanliness = self.db.get_plugin_cleanliness(u'clean.esp')

        self.assertEqual(cleanliness, PluginCleanliness.clean)

    def test_get_plugin_cleanliness_should_be_dirty_if_only_dirty_metadata_exists(self):
        self.db.load_lists(self.masterlist_path, u'')

        cleanliness = self.db.get_plugin_cleanliness(u'dirty.esp')

        self.assertEqual(cleanliness, PluginCleanliness.dirty)

    def test_get_plugin_cleanliness_should_be_do_not_clean_if_dirty_do_not_clean_info_exists(self):
        self.db.load_lists(self.masterlist_path, u'')

        cleanliness = self.db.get_plugin_cleanliness(u'do_not_clean.esp')

        self.assertEqual(cleanliness, PluginCleanliness.do_not_clean)

if __name__ == '__main__':
    unittest.main()
