#! /usr/bin/env python
# -*- coding: utf-8 -*-
#


# imports_successful = True

# ============================== Native Imports ===============================
import os
import platform
import requirements
import sys
import traceback
# import aiohttp

# ============================== Custom Imports ===============================
try:
    # noinspection PyUnresolvedReferences
    import indigo
except ImportError:
    pass

# try:
#     print(f"Import: from twisted.internet import reactor")
#     from twisted.internet import reactor
#
#     print(f"Import: from twisted.internet.protocol import DatagramProtocol")
#     from twisted.internet.protocol import DatagramProtocol
#
#     print(f"Import: from twisted.application.internet import MulticastServer")
#     from twisted.application.internet import MulticastServer
#
#     print(f"Import: xmltodict")
#     import xmltodict
# except ImportError:
#     imports_successful = True
#
# print(f"Imports successful?: {imports_successful}")

# ============================== Plugin Imports ===============================
from constants import *

# if imports_successful:
#     from Sonos import Sonos


class Plugin(indigo.PluginBase):

    ######################################################################################
    # class init & del
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

        # print(f"TEST PRINT: {imports_successful}")

        # Initialise dictionary to store plugin Globals
        self.globals = dict()

        self.Sonos = None

        # Initialise Indigo plugin info
        self.globals[PLUGIN_INFO] = {}
        self.globals[PLUGIN_INFO][PLUGIN_ID] = pluginId
        self.globals[PLUGIN_INFO][PLUGIN_DISPLAY_NAME] = pluginDisplayName
        self.globals[PLUGIN_INFO][PLUGIN_VERSION] = pluginVersion
        self.globals[PLUGIN_INFO][PATH] = indigo.server.getInstallFolderPath()
        self.globals[PLUGIN_INFO][API_VERSION] = indigo.server.apiVersion
        self.globals[PLUGIN_INFO][ADDRESS] = indigo.server.address

        # Setup logging
        log_format = logging.Formatter("%(asctime)s.%(msecs)03d\t%(levelname)-12s\t%(name)s.%(funcName)-25s %(msg)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.plugin_file_handler.setFormatter(log_format)
        self.plugin_file_handler.setLevel(LOG_LEVEL_INFO)  # Logging Level for plugin log file
        self.indigo_log_handler.setLevel(LOG_LEVEL_INFO)   # Logging level for Indigo Event Log

        self.logger = logging.getLogger("Plugin.Sonos")

        # Create Plugin Packages folder if it doesn't exist
        self.globals[PLUGIN_PACKAGES_FOLDER] = f"{self.globals[PLUGIN_INFO][PATH]}/Preferences/Plugins/com.ssi.indigoplugin.Sonos.python_packages"
        if not os.path.exists(self.globals[PLUGIN_PACKAGES_FOLDER]):
            self.mkdir_with_mode(self.globals[PLUGIN_PACKAGES_FOLDER])

        # Now tell Python to search for packages in the Plugin Packages folder
        sys.path.insert(1, self.globals[PLUGIN_PACKAGES_FOLDER])

        print(sys.path)

        # # Create Plugin Resources folder if it doesn't exist
        # self.globals[PLUGIN_PACKAGES_FOLDER] = f"{self.globals[PLUGIN_INFO][PATH]}/Plugins/Sonos.indigoPlugin/Contents/Packages"
        #
        # if not os.path.exists(self.globals[PLUGIN_PACKAGES_FOLDER]):
        #     self.mkdir_with_mode(self.globals[PLUGIN_PACKAGES_FOLDER])

        # Now tell Python to search for packages in the Plugin Packages folder
        # sys.path.insert(1, self.globals[PLUGIN_PACKAGES_FOLDER])

        # Now perform imports

        imports_successful = True
        try:
            print(f"Import: from twisted.internet import reactor")
            from twisted.internet import reactor

            print(f"Import: from twisted.internet.protocol import DatagramProtocol")
            from twisted.internet.protocol import DatagramProtocol

            print(f"Import: from twisted.application.internet import MulticastServer")
            from twisted.application.internet import MulticastServer

            print(f"Import: xmltodict")
            import xmltodict

            print(f"Import: lxml")
            import lxml

            from lxml import etree as LXML
        except ImportError as exception:
            imports_successful = False
            print(f"Import failed:\n{exception}")

        print(f"Imports successful?: {imports_successful}")

        # Original Sonos plugin

        if imports_successful:
            from Sonos import Sonos

        self.optional_packages_checked = list()  # List of optional packages already checked

        print(f"Imports Successful?: {imports_successful}")
        if imports_successful:
            self.Sonos = Sonos(self, pluginPrefs)
        self.debug = False
        self.xmlDebug = False
        self.eventsDebug = False
        self.stateUpdatesDebug = False
        self.StopThread = False

        self.do_not_start_stop_devices = False  # Used in conjunction with requirements.py for Python package checking

    def __del__(self):
        indigo.PluginBase.__del__(self)

    ######################################################################################
    def display_plugin_information(self):
        try:
            def plugin_information_message():
                startup_message_ui = "Plugin Information:\n"
                startup_message_ui += f"{'':={'^'}80}\n"
                startup_message_ui += f"{'Plugin Name:':<30} {self.globals[PLUGIN_INFO][PLUGIN_DISPLAY_NAME]}\n"
                startup_message_ui += f"{'Plugin Version:':<30} {self.globals[PLUGIN_INFO][PLUGIN_VERSION]}\n"
                startup_message_ui += f"{'Plugin ID:':<30} {self.globals[PLUGIN_INFO][PLUGIN_ID]}\n"
                startup_message_ui += f"{'Indigo Version:':<30} {indigo.server.version}\n"
                startup_message_ui += f"{'Indigo License:':<30} {indigo.server.licenseStatus}\n"
                startup_message_ui += f"{'Indigo API Version:':<30} {indigo.server.apiVersion}\n"
                startup_message_ui += f"{'Architecture:':<30} {platform.machine()}\n"
                startup_message_ui += f"{'Python Version:':<30} {sys.version.split(' ')[0]}\n"
                startup_message_ui += f"{'Mac OS Version:':<30} {platform.mac_ver()[0]}\n"
                startup_message_ui += f"{'Plugin Process ID:':<30} {os.getpid()}\n"
                startup_message_ui += f"{'':={'^'}80}\n"
                return startup_message_ui

            self.logger.info(plugin_information_message())

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    def exception_handler(self, exception_error_message, log_failing_statement):
        filename, line_number, method, statement = traceback.extract_tb(sys.exc_info()[2])[-1]
        module = filename.split('/')
        log_message = f"'{exception_error_message}' in module '{module[-1]}', method '{method}'"
        if log_failing_statement:
            log_message = log_message + f"\n   Failing statement [line {line_number}]: '{statement}'"
        else:
            log_message = log_message + f" at line {line_number}"
        self.logger.error(log_message)

    ######################################################################################
    def mkdir_with_mode(self, directory):
        try:
            # Forces Read | Write on creation so that the plugin can delete the folder id required
            if not os.path.isdir(directory):
                oldmask = os.umask(000)
                os.makedirs(directory, 0o777)
                os.umask(oldmask)
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # plugin startup and shutdown

    def startup(self):
        try:
            # Create preferences packages folder if it doesn't exist
            try:
                requirements.requirements_check(self.globals[PLUGIN_INFO][PLUGIN_ID], self.logger, self.globals[PLUGIN_PACKAGES_FOLDER], self.optional_packages_checked)
            except ImportError as exception_error:
                self.logger.critical(f"PLUGIN STOPPED AS PYTHON PACKAGE(S) REQUIRE INSTALLING | UPDATING: {exception_error}")
                self.do_not_start_stop_devices = True
                self.stopPlugin()

            if not self.do_not_start_stop_devices:
                if self.Sonos != None:
                    self.Sonos.startup()

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def shutdown(self):
        try:
            self.logger.debug("Method: shutdown")
            if not self.do_not_start_stop_devices:
                self.Sonos.shutdown()

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # ConcurrentThread: Start & Stop
    def runConcurrentThread(self):
        try:
            self.sleep(5.0)  # Delay start of concurrent thread

            if not self.do_not_start_stop_devices:
                if self.Sonos != None:
                    self.Sonos.runConcurrentThread()
            else:
                self.StopThread = True

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def stopConcurrentThread(self):
        try:
            if not self.do_not_start_stop_devices:
                self.StopThread = True
                if self.Sonos != None:
                    self.Sonos.stopConcurrentThread()

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def deviceStartComm(self, dev):
        try:
            if self.do_not_start_stop_devices:  # This is set to True if Package requirements listed in requirements.txt are not met
                return

            if self.Sonos != None:
                self.Sonos.deviceStartComm (dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def deviceStopComm(self, dev):
        try:
            if self.do_not_start_stop_devices:  # This is set to True if Package requirements listed in requirements.txt are not met
                return

            if self.Sonos != None:
                self.Sonos.deviceStopComm (dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        try:
            return self.Sonos.closedPrefsConfigUi(valuesDict, userCancelled)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # Action Menthods

    def actionPlay(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Play")

    def actionTogglePlay(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "TogglePlay")

    def actionPause(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Pause")

    def actionStop(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Stop")

    def actionPrevious(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Previous")

    def actionNext(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Next")

    def actionChannelUp(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ChannelUp")

    def actionChannelDown(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ChannelDown")

    def actionMuteToggle(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "MuteToggle")

    def actionMuteOn(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "MuteOn")

    def actionMuteOff(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "MuteOff")

    def actionGroupMuteToggle(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "GroupMuteToggle")

    def actionGroupMuteOn(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "GroupMuteOn")

    def actionGroupMuteOff(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "GroupMuteOff")

    def actionVolume(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Volume")

    def actionVolumeDown(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "VolumeDown")

    def actionVolumeUp(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "VolumeUp")

    def actionGroupVolume(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "GroupVolume")

    def actionRelativeGroupVolume(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "RelativeGroupVolume")

    def actionGroupVolumeDown(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "GroupVolumeDown")

    def actionGroupVolumeUp(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "GroupVolumeUp")

    def actionNightMode(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "NightMode")

    def actionQ_Crossfade(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_Crossfade")

    def actionQ_Repeat(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_Repeat")

    def actionQ_RepeatOne(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_RepeatOne")

    def actionQ_RepeatToggle(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_RepeatToggle")

    def actionQ_Shuffle(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_Shuffle")

    def actionQ_ShuffleToggle(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_ShuffleToggle")

    def actionQ_Clear(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_Clear")

    def actionQ_Save(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "Q_Save")

    def actionCD_RemovePlaylist(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "CD_RemovePlaylist")

    def actionZP_LIST(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_LIST")

    def actionZP_LineIn(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_LineIn")

    def actionZP_Queue(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_Queue")

    def actionZP_SonosFavorites(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_SonosFavorites")

    def actionZP_RT_FavStation(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_RT_FavStation")

    def actionRadioTime(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "RadioTime")

    def actionZP_addPlayerToZone(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "addPlayerToZone")

    def actionZP_setStandalone(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "setStandalone")

    def actionZP_saveStates(self, pluginAction):
        return self.Sonos.actionStates(pluginAction, "saveStates")

    def actionZP_addPlayersToZone(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "addPlayersToZone")

    def actionZP_setStandalones(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "setStandalones")

    def actionZP_announcement(self, pluginAction):
        return self.Sonos.actionAnnouncement(pluginAction, "announcement")

    def actionZP_announcementMP3(self, pluginAction):
        return self.Sonos.actionAnnouncement(pluginAction, "announcementMP3")

    def actionZP_sleepTimer(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_sleepTimer")

    def actionZP_Pandora(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_Pandora")

    def actionZP_SiriusXM(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_SiriusXM")

    def actionZP_TV(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_TV")

    def actionZP_DumpURI(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_DumpURI")

    def actionPandora_ThumbsUp(self, pluginAction):
        return self.Sonos.actionPandoraThumbs(pluginAction, "thumbs_up")

    def actionPandora_ThumbsDown(self, pluginAction):
        return self.Sonos.actionPandoraThumbs(pluginAction, "thumbs_down")

    ######################################################################################
    # Menu Items

    ######################################################################################
    # Validations for UI

    def validatePrefsConfigUi(self, valuesDict):
        return self.Sonos.validatePrefsConfigUi(valuesDict)

    ######################################################################################
    # Lists for UI

    def getZPDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZPDeviceList(filter)

    def getZP_LIST(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_LIST()

    def getZP_LIST_PlaylistObjects(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_LIST_PlaylistObjects()

    def getZP_LineIn(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_LineIn()

    def getZP_SonosFavorites(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_SonosFavorites()

    def getZP_RT_FavStations(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_RT_FavStations()

    def getZP_Pandora(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_Pandora()

    def getZP_SiriusXM(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_SiriusXM()

    def getZP_SoundFiles(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_SoundFiles()

    def getIVONAVoices(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getIVONAVoices()

    def getPollyVoices(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getPollyVoices()

    def getAppleVoices(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getAppleVoices()

    def getMicrosoftLanguages(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getMicrosoftLanguages()
