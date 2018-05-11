/*  LOOT

    A load order optimisation tool for Oblivion, Skyrim, Fallout 3 and
    Fallout: New Vegas.

    Copyright (C) 2012-2016    WrinklyNinja

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

#include <loot/api.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "convenience.h"
#include "wrapper_version.h"

using pybind11::arg;
using pybind11::enum_;
using pybind11::class_;
using pybind11::metaclass;

namespace loot {
void bindEnums(pybind11::module& module) {
  enum_<GameType>(module, "GameType")
    .value("tes4", GameType::tes4)
    .value("tes5", GameType::tes5)
    .value("tes5se", GameType::tes5se)
    .value("tes5vr", GameType::tes5vr)
    .value("fo3", GameType::fo3)
    .value("fonv", GameType::fonv)
    .value("fo4", GameType::fo4)
    .value("fo4vr", GameType::fo4vr);

  enum_<LogLevel>(module, "LogLevel")
    .value("trace", LogLevel::trace)
    .value("debug", LogLevel::debug)
    .value("info", LogLevel::info)
    .value("warning", LogLevel::warning)
    .value("error", LogLevel::error)
    .value("fatal", LogLevel::fatal);

  enum_<MessageType>(module, "MessageType")
    .value("say", MessageType::say)
    .value("warn", MessageType::warn)
    .value("error", MessageType::error);

  enum_<PluginCleanliness>(module, "PluginCleanliness")
    .value("clean", PluginCleanliness::clean)
    .value("dirty", PluginCleanliness::dirty)
    .value("do_not_clean", PluginCleanliness::do_not_clean)
    .value("unknown", PluginCleanliness::unknown);
}

void bindMetadataClasses(pybind11::module& module) {
  class_<MasterlistInfo>(module, "MasterlistInfo")
    .def_readwrite("revision_id", &MasterlistInfo::revision_id)
    .def_readwrite("revision_date", &MasterlistInfo::revision_date)
    .def_readwrite("is_modified", &MasterlistInfo::is_modified);

  class_<SimpleMessage>(module, "SimpleMessage")
    .def_readwrite("type", &SimpleMessage::type)
    .def_readwrite("language", &SimpleMessage::language)
    .def_readwrite("text", &SimpleMessage::text)
    .def_readwrite("condition", &SimpleMessage::condition);

  class_<PluginTags>(module, "PluginTags")
    .def_readwrite("added", &PluginTags::added)
    .def_readwrite("removed", &PluginTags::removed)
    .def_readwrite("userlist_modified", &PluginTags::userlist_modified);

  class_<PluginMetadata>(module, "PluginMetadata")
    .def("get_simple_messages", &PluginMetadata::GetSimpleMessages);
}

void bindVersionClasses(pybind11::module& module) {
  class_<LootVersion>(module, "Version")
    .def_readonly_static("major", &LootVersion::major)
    .def_readonly_static("minor", &LootVersion::minor)
    .def_readonly_static("patch", &LootVersion::patch)
    .def_readonly_static("revision", &LootVersion::revision)
    .def_static("string", LootVersion::string);

  class_<WrapperVersion>(module, "WrapperVersion")
    .def_readonly_static("major", &WrapperVersion::major)
    .def_readonly_static("minor", &WrapperVersion::minor)
    .def_readonly_static("patch", &WrapperVersion::patch)
    .def_readonly_static("revision", &WrapperVersion::revision)
    .def_static("string", WrapperVersion::string);
}

void bindInterfaceClasses(pybind11::module& module) {
  class_<GameInterface, std::shared_ptr<GameInterface>>(module, "GameInterface")
    .def("load_current_load_order_state", &GameInterface::LoadCurrentLoadOrderState)
    .def("get_database", &GameInterface::GetDatabase);

  class_<DatabaseInterface, std::shared_ptr<DatabaseInterface>>(module, "DatabaseInterface")
    .def("load_lists", &DatabaseInterface::LoadLists, arg("masterlist_path"), arg("userlist_path") = "")
    .def("update_masterlist", &DatabaseInterface::UpdateMasterlist)
    .def("get_masterlist_revision", &DatabaseInterface::GetMasterlistRevision)
    .def("get_plugin_metadata", &DatabaseInterface::GetPluginMetadata,
      arg("plugin"),
      arg("includeUserMetadata") = true,
      arg("evaluateConditions") = false)
    .def("get_plugin_tags", &GetPluginTags,
      arg("plugin"),
      arg("evaluateConditions") = false)
    .def("get_plugin_cleanliness", &GetPluginCleanliness,
      arg("plugin"),
      arg("evaluateConditions") = false)
    .def("write_minimal_list", &DatabaseInterface::WriteMinimalList);
}

void bindClasses(pybind11::module& module) {
  bindMetadataClasses(module);
  bindVersionClasses(module);
  bindInterfaceClasses(module);
}

void bindFunctions(pybind11::module& module) {
  module.def("set_logging_callback", &SetLoggingCallback);

  module.def("is_compatible", &IsCompatible);

  module.def("initialise_locale", &InitialiseLocale, arg("id") = "");

  module.def("create_game_handle", &CreateGameHandle,
    arg("game"),
    arg("game_path"),
    arg("game_local_path") = "");
}
}

PYBIND11_PLUGIN(loot_api) {
  pybind11::module module("loot_api", "A Python module that wraps the LOOT API, generated by pybind11.");

  loot::bindEnums(module);
  loot::bindClasses(module);
  loot::bindFunctions(module);

  return module.ptr();
}
