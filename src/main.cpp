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
using std::filesystem::path;
using std::filesystem::u8path;

namespace loot {
namespace py {
std::shared_ptr<GameInterface> CreateGameHandle(GameType gameType, std::string gamePath, std::string gameLocalPath) {
  return CreateGameHandle(gameType, u8path(gamePath), u8path(gameLocalPath));
}

void LoadLists(std::shared_ptr<DatabaseInterface> db, std::string masterlistPath, std::string userlistPath) {
  return db->LoadLists(u8path(masterlistPath), u8path(userlistPath));
}

void WriteMinimalList(std::shared_ptr<DatabaseInterface> db, std::string outputFile, bool overwrite) {
  return db->WriteMinimalList(u8path(outputFile), overwrite);
}

bool UpdateMasterlist(std::shared_ptr<DatabaseInterface> db, std::string masterlistPath, std::string remoteUrl, std::string remoteBranch) {
  return db->UpdateMasterlist(u8path(masterlistPath), remoteUrl, remoteBranch);
}

MasterlistInfo GetMasterlistRevision(std::shared_ptr<DatabaseInterface> db, std::string masterlistPath, bool getShortId) {
  return db->GetMasterlistRevision(u8path(masterlistPath), getShortId);
}

void SetLoggingCallback(std::function<void(LogLevel, const char*)> callback) {
  callback = [callback](LogLevel level, const char* message) {
    pybind11::gil_scoped_acquire acquire;
    callback(level, message);
  };
  loot::SetLoggingCallback(callback);
}
}

void bindEnums(pybind11::module& module) {
  pybind11::options options;
  options.disable_function_signatures();

  enum_<GameType>(module, "GameType", "Wraps :cpp:enum:`loot::GameType` to expose libloot's game codes.")
    .value("tes4", GameType::tes4)
    .value("tes5", GameType::tes5)
    .value("tes5se", GameType::tes5se)
    .value("tes5vr", GameType::tes5vr)
    .value("fo3", GameType::fo3)
    .value("fonv", GameType::fonv)
    .value("fo4", GameType::fo4)
    .value("fo4vr", GameType::fo4vr);

  enum_<LogLevel>(module, "LogLevel", "Wraps :cpp:enum:`loot::LogLevel` to expose libloot's log level codes.")
    .value("trace", LogLevel::trace)
    .value("debug", LogLevel::debug)
    .value("info", LogLevel::info)
    .value("warning", LogLevel::warning)
    .value("error", LogLevel::error)
    .value("fatal", LogLevel::fatal);

  enum_<MessageType>(module, "MessageType", "Wraps :cpp:enum:`loot::MessageType` to expose libloot's message type codes.")
    .value("say", MessageType::say)
    .value("warn", MessageType::warn)
    .value("error", MessageType::error);

  enum_<PluginCleanliness>(module, "PluginCleanliness", "Codes used to indicate the cleanliness of a plugin according to the information contained within the loaded masterlist / userlist.")
    .value("clean", PluginCleanliness::clean, "Indicates that the plugin is clean.")
    .value("dirty", PluginCleanliness::dirty, "Indicates that the plugin is dirty.")
    .value("do_not_clean", PluginCleanliness::do_not_clean, "Indicates that the plugin contains dirty edits, but that they are part of the plugin's intended functionality and should not be removed.")
    .value("unknown", PluginCleanliness::unknown, "Indicates that no data is available on whether the plugin is dirty or not.");
}

void bindMetadataClasses(pybind11::module& module) {
  class_<MasterlistInfo>(module, "MasterlistInfo", "Wraps :cpp:class:`loot::MasterlistInfo`.")
    .def_readwrite("revision_id", &MasterlistInfo::revision_id, "A Unicode string containing a Git commit's SHA-1 checksum.")
    .def_readwrite("revision_date", &MasterlistInfo::revision_date, "A Unicode string containing the date of the commit given by :py:attr:`~loot.MasterlistInfo.revision_id`, in ISO 8601 format (YYYY-MM-DD).")
    .def_readwrite("is_modified", &MasterlistInfo::is_modified, "A boolean that is true if the masterlist has been modified from its state at the commit given by :py:attr:`~loot.MasterlistInfo.revision_id`.");

  class_<SimpleMessage>(module, "SimpleMessage", "Wraps :cpp:class:`loot::SimpleMessage`.")
    .def_readwrite("type", &SimpleMessage::type, "A :py:class:`loot.MessageType` giving the message type.")
    .def_readwrite("language", &SimpleMessage::language, "A Unicode string giving the message text language.")
    .def_readwrite("text", &SimpleMessage::text, "A Unicode string containing the message text.")
    .def_readwrite("condition", &SimpleMessage::condition, "A Unicode string containing the message condition.");

  class_<PluginTags>(module, "PluginTags")
    .def_readwrite("added", &PluginTags::added, "A set of Unicode strings giving Bash Tags suggested for addition.")
    .def_readwrite("removed", &PluginTags::removed, "A set of Unicode strings giving Bash Tags suggested for removal.")
    .def_readwrite("userlist_modified", &PluginTags::userlist_modified, "A boolean that is true if the suggestions contain metadata obtained from a loaded userlist.");

  class_<PluginMetadata>(module, "PluginMetadata", "Wraps :cpp:class:`loot::PluginMetadata`.")
    .def("get_simple_messages",
      &PluginMetadata::GetSimpleMessages,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Get the plugin's messages as SimpleMessage objects for the given language. Wraps :cpp:func:`GetSimpleMessages`.");
}

void bindVersionClasses(pybind11::module& module) {
  // FIXME: For some reason the static properties have their docstrings ignored.
  class_<LootVersion>(module, "Version", "Wraps :cpp:class:`loot::LootVersion`.")
    .def_readonly_static("major", &LootVersion::major, "An unsigned integer giving the major version number. Read-only.")
    .def_readonly_static("minor", &LootVersion::minor, "An unsigned integer giving the minor version number. Read-only.")
    .def_readonly_static("patch", &LootVersion::patch, "An unsigned integer giving the patch version number. Read-only.")
    .def_readonly_static("revision", &LootVersion::revision, "A Unicode string containing the Git commit hash that the wrapped libloot was built from.")
    .def_static("string",
      LootVersion::GetVersionString,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Returns the libloot version as a string of the form ``major.minor.patch``.");

  class_<WrapperVersion>(module, "WrapperVersion", "Provides information about the version of libloot-python that is being run.")
    .def_readonly_static("major", &WrapperVersion::major, "An unsigned integer giving the major version number. Read-only.")
    .def_readonly_static("minor", &WrapperVersion::minor, "An unsigned integer giving the minor version number. Read-only.")
    .def_readonly_static("patch", &WrapperVersion::patch, "An unsigned integer giving the patch version number. Read-only.")
    .def_readonly_static("revision", &WrapperVersion::revision, "A Unicode string containing the Git commit hash that the Python module was built from.")
    .def_static("string",
      WrapperVersion::string,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Returns the module version as a string of the form ``major.minor.patch``.");
}

void bindInterfaceClasses(pybind11::module& module) {
  class_<GameInterface, std::shared_ptr<GameInterface>>(module, "GameInterface", "Wraps :cpp:class:`loot::GameInterface`.")
    .def("load_current_load_order_state",
      &GameInterface::LoadCurrentLoadOrderState,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Load the current load order state, discarding any previously held state. Wraps :cpp:func:`LoadCurrentLoadOrderState`.")
    .def("get_database",
      &GameInterface::GetDatabase,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Get a database handle. Wraps :cpp:func:`GetDatabase`.")
    .def("load_plugins",
      &GameInterface::LoadPlugins,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Load the given plugins. Wraps :cpp:func:`LoadPlugins`.")
    .def("get_plugin",
      &GameInterface::GetPlugin,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Get the given loaded plugin. Wraps :cpp:func:`GetPlugin`.");

  class_<DatabaseInterface, std::shared_ptr<DatabaseInterface>>(module, "DatabaseInterface", "Wraps :cpp:class:`loot::DatabaseInterface`.")
    .def("load_lists",
      &py::LoadLists,
      arg("masterlist_path"),
      arg("userlist_path") = "",
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Loads the masterlist and userlist from the paths specified. Wraps :cpp:func:`LoadLists`.")
    .def("update_masterlist",
      &py::UpdateMasterlist,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Updates the given masterlist using the given Git repository details. Wraps :cpp:func:`UpdateMasterlist`.")
    .def("get_masterlist_revision",
      &py::GetMasterlistRevision,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Gets the give masterlist's source control revision. Wraps :cpp:func:`GetMasterlistRevision`.")
    .def("get_plugin_metadata",
      &DatabaseInterface::GetPluginMetadata,
      arg("plugin"),
      arg("includeUserMetadata") = true,
      arg("evaluateConditions") = false,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Get all a plugin's loaded metadata. Wraps :cpp:func:`GetPluginMetadata`.")
    .def("get_plugin_tags",
      &GetPluginTags,
      arg("plugin"),
      arg("evaluateConditions") = false,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Outputs the Bash Tags suggested for addition and removal by the database for the given plugin.")
    .def("get_plugin_cleanliness",
      &GetPluginCleanliness,
      arg("plugin"),
      arg("evaluateConditions") = false,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Determines the database's knowledge of a plugin's cleanliness. Outputs whether the plugin should be cleaned or not, or if no data is available.")
    .def("write_minimal_list",
      &py::WriteMinimalList,
      pybind11::call_guard<pybind11::gil_scoped_release>(), 
      "Writes a minimal metadata file containing only Bash Tag suggestions and/or cleanliness info from the loaded metadata. Wraps :cpp:func:`WriteMinimalList`.");

  class_<PluginInterface, std::shared_ptr<PluginInterface>>(module, "PluginInterface")
    .def_property_readonly("name",
      &PluginInterface::GetName,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "The plugin's name. Read-only. Wraps :cpp:func:`GetName`.")
    .def("is_master",
      &PluginInterface::IsMaster,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Check if the plugin is a master. Wraps :cpp:func:`IsMaster`.")
    .def("is_light_master",
      &PluginInterface::IsLightMaster,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Check if the plugin is a light master. Wraps :cpp:func:`IsLightMaster`.")
    .def("is_valid_as_light_master",
      &PluginInterface::IsValidAsLightMaster,
      pybind11::call_guard<pybind11::gil_scoped_release>(),
      "Check if the plugin contains only records with FormIDs that are valid in a light master. Wraps :cpp:func:`IsValidAsLightMaster`.");
}

void bindClasses(pybind11::module& module) {
  bindMetadataClasses(module);
  bindVersionClasses(module);
  bindInterfaceClasses(module);
}

void bindFunctions(pybind11::module& module) {
  module.def("set_logging_callback", 
    &py::SetLoggingCallback, 
    arg("callback"), 
    "Set the callback function that is called when logging. Wraps :cpp:func:`loot::SetLoggingCallback`.");

  // Need to clear the stored logging callback when exiting, or Python will
  // hang because the callback pointer is still stored by libloot.
  auto atexit = pybind11::module::import("atexit");
  atexit.attr("register")(pybind11::cpp_function([]() {
    SetLoggingCallback(nullptr);
  }));

  module.def("is_compatible",
    &IsCompatible,
    pybind11::call_guard<pybind11::gil_scoped_release>(),
    "Checks for API compatibility. Wraps :cpp:func:`loot::IsCompatible`.");

  module.def("create_game_handle",
    &py::CreateGameHandle,
    arg("game"),
    arg("game_path"),
    arg("game_local_path") = "",
    pybind11::call_guard<pybind11::gil_scoped_release>(),
    "Initialise a new game handle. Wraps :cpp:func:`loot::CreateGameHandle`.");
}
}

PYBIND11_MODULE(loot, module) {
  module.doc() = "A Python module that wraps libloot, generated by pybind11.";

  loot::bindEnums(module);
  loot::bindClasses(module);
  loot::bindFunctions(module);
}
