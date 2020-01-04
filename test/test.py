#!/usr/bin/env python

import cProfile
import os
import os.path
import shutil
import sys
import unittest

sys.path.append(os.getcwd())

from loot import Version
from loot import WrapperVersion
from loot import GameType
from loot import SimpleMessage
from loot import MessageType
from loot import PluginCleanliness
from loot import create_game_handle
from loot import is_compatible
from loot import set_logging_callback

def logging_callback(level, message):
    print(level, message)

set_logging_callback(logging_callback)

class GameFixture(unittest.TestCase):
    game_path = os.path.join(u'.', u'Oblivion')
    local_path = os.path.join(u'.', u'local')
    master_filename = u'Oblivion.esm'

    def setUp(self):
        open(self.master_file_path(), 'a').close()

        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

    def tearDown(self):
        os.remove(self.master_file_path())
        shutil.rmtree(self.local_path)

    def master_file_path(self):
        return os.path.join(self.game_path, 'Data', self.master_filename)

class TestLootApi(GameFixture):
    def test_is_compatible(self):
        self.assertFalse(is_compatible(0, 9, 0))
        self.assertTrue(is_compatible(0, 15, 0))

    def test_version(self):
        self.assertEqual(Version.major, 0)
        self.assertEqual(Version.minor, 15)
        self.assertEqual(Version.patch, 0)
        self.assertNotEqual(Version.revision, u'')
        self.assertEqual(Version.string(), "0.15.0")

    def test_wrapper_version(self):
        self.assertEqual(WrapperVersion.major, 4)
        self.assertEqual(WrapperVersion.minor, 0)
        self.assertEqual(WrapperVersion.patch, 2)
        self.assertNotEqual(WrapperVersion.revision, u'')
        self.assertNotEqual(WrapperVersion.revision, Version.revision)
        self.assertEqual(WrapperVersion.string(), "4.0.2")

    def test_create_db(self):
        game = create_game_handle(GameType.tes4, self.game_path, self.local_path)
        db = game.get_database()
        self.assertNotEqual(db, None)

class TestGameInterface(GameFixture):
    def setUp(self):
        super(TestGameInterface, self).setUp()

        self.game = create_game_handle(GameType.tes4, self.game_path, self.local_path)

    def test_load_plugins(self):
        self.game.load_plugins([u'Blank.esm'], True)
        self.game.load_plugins([u'Blank.esm'], False)

    def test_get_plugin(self):
        self.game.load_plugins([u'Blank.esm'], True)
        plugin = self.game.get_plugin(u'Blank.esm')

        self.assertNotEqual(plugin, None)

class TestPluginInterface(GameFixture):
    game_path = os.path.join(u'.', u'SkyrimSE')
    master_filename = u'Skyrim.esm'

    def setUp(self):
        super(TestPluginInterface, self).setUp()

        self.game = create_game_handle(GameType.tes5se, self.game_path, self.local_path)
        self.game.load_plugins([u'Blank.esm', u'Blank.esl'], False)

    def test_name(self):
        plugin = self.game.get_plugin(u'Blank.esm')

        self.assertNotEqual(plugin, None)
        self.assertEqual(plugin.name, u'Blank.esm')

    def test_is_master(self):
        plugin = self.game.get_plugin(u'Blank.esm')

        self.assertNotEqual(plugin, None)
        self.assertTrue(plugin.is_master())

    def test_is_light_master(self):
        plugin = self.game.get_plugin(u'Blank.esm')

        self.assertNotEqual(plugin, None)
        self.assertFalse(plugin.is_light_master())

        plugin = self.game.get_plugin(u'Blank.esl')

        self.assertNotEqual(plugin, None)
        self.assertTrue(plugin.is_light_master())

    def test_is_valid_as_light_master(self):
        plugin = self.game.get_plugin(u'Blank.esm')

        self.assertNotEqual(plugin, None)
        self.assertTrue(plugin.is_valid_as_light_master())

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
