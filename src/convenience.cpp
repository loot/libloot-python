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

#include "convenience.h"

#include <loot/api.h>

namespace loot {
PluginTags GetPluginTags(const std::shared_ptr<DatabaseInterface> db, const std::string& plugin, bool evaluateConditions) {
  PluginTags tags;

  auto metadata = db->GetPluginMetadata(plugin, false, evaluateConditions);
  if (metadata.has_value()) {
    for (const auto &tag : metadata.value().GetTags()) {
      if (tag.IsAddition())
        tags.added.insert(tag.GetName());
      else
        tags.removed.insert(tag.GetName());
    }
  }

  metadata = db->GetPluginUserMetadata(plugin, evaluateConditions);
  if (metadata.has_value()) {
    tags.userlist_modified = !metadata.value().GetTags().empty();
    for (const auto &tag : metadata.value().GetTags()) {
      if (tag.IsAddition())
        tags.added.insert(tag.GetName());
      else
        tags.removed.insert(tag.GetName());
    }
  }

  return tags;
}

PluginCleanliness GetPluginCleanliness(const std::shared_ptr<DatabaseInterface> db, const std::string& plugin, bool evaluateConditions) {
  auto metadata = db->GetPluginMetadata(plugin, true, evaluateConditions);

  if (!metadata.has_value()) {
    return PluginCleanliness::unknown;
  }

  auto dirtyInfo = metadata.value().GetDirtyInfo();
  auto cleanInfo = metadata.value().GetCleanInfo();

  if (dirtyInfo.empty() == cleanInfo.empty()) {
    return PluginCleanliness::unknown;
  }

  if (!cleanInfo.empty()) {
    return PluginCleanliness::clean;
  }

  for (const auto& info : dirtyInfo) {
    if (info.ChooseInfo("en").GetText().find("Do not clean") != std::string::npos) {
      return PluginCleanliness::do_not_clean;
    }
  }

  return PluginCleanliness::dirty;
}
}
