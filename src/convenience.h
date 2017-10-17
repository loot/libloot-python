/*  LOOT

A load order optimisation tool for Oblivion, Skyrim, Fallout 3 and
Fallout: New Vegas.

Copyright (C) 2014-2017    Oliver Hamlet

This file is part of LOOT.

LOOT is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

LOOT is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LOOT.  If not, see
<https://www.gnu.org/licenses/>.
*/

#ifndef LOOT_API_PYTHON_CONVENIENCE
#define LOOT_API_PYTHON_CONVENIENCE

#include <memory>

#include <loot/enum/game_type.h>
#include <loot/database_interface.h>

#include "plugin_cleanliness.h"
#include "plugin_tags.h"

namespace loot {
std::shared_ptr<DatabaseInterface> CreateDatabase(const GameType game,
                                                  const std::string& game_path = "",
                                                  const std::string& game_local_path = "");

PluginTags GetPluginTags(const std::shared_ptr<DatabaseInterface> db,
                         const std::string& plugin,
                         bool evaluateConditions = false);

PluginCleanliness GetPluginCleanliness(const std::shared_ptr<DatabaseInterface> db,
                                       const std::string& plugin,
                                       bool evaluateConditions = false);
}

#endif
