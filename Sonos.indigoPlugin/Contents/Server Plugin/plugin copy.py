#! /usr/bin/env python
# -*- coding: utf-8 -*-
#


# imports_successful = True

# ============================== Native Imports ===============================
import os
import platform
import sys
import traceback
import time
# import aiohttp

# =================== requirements.txt imports ==================
import_errors = []
try:
    from twisted.internet import reactor
    from twisted.internet.protocol import DatagramProtocol
    from twisted.application.internet import MulticastServer
except ImportError:
    import_errors.append("twisted")

try:
    from gtts import gTTS
except ImportError:
    import_errors.append("gTTS")

try:
    import pyvona
except ImportError:
    import_errors.append("pyvona")

try:
    import boto3
except ImportError:
    import_errors.append("boto3")

try:
    from mutagen.mp3 import MP3
    from mutagen.aiff import AIFF
except ImportError:
    import_errors.append("mutagen")

try:
    import urllib
    import urllib.parse
    from urllib.request import urlopen
    import urllib.request
except ImportError:
    import_errors.append("urllib")

# ============================== Custom Imports ===============================
try:
    # noinspection PyUnresolvedReferences
    import indigo
except ImportError:
    pass

from pandora import Pandora

# ============================== Plugin Imports ===============================
from constants import *

from soco import SoCo


indiPref_plugin_stopped = """<?xml version="1.0" encoding="UTF-8"?>
<Prefs type="dict">
    <plugin_stopped type="bool">true</plugin_stopped>
</Prefs>

"""


class Plugin(indigo.PluginBase):


    ######################################################################################
    # class init & del
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

        # Initialise dictionary to store plugin Globals
        self.globals = dict()

        self.Sonos = None
        self.pluginPrefs = pluginPrefs

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
        self.logger.info("Plugin logging now started.")

        self.debug = False
        self.xmlDebug = False
        self.eventsDebug = False
        self.stateUpdatesDebug = False
        self.StopThread = False

        # ✅ Instantiate SonosPlugin here
        try:
            from Sonos import SonosPlugin
            self.Sonos = SonosPlugin(self, self.pluginPrefs)
            # plugin.py
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize SonosPlugin: {e}")
            self.Sonos = None

        self.logger.info("Plugin __init__ ended.")

        self.last_siriusxm_guid_by_dev = {}


    def __del__(self):
        indigo.PluginBase.__del__(self)

    ######################################################################################


###

    def actionSetSiriusXMChannel(self, pluginAction, dev):
        chan_id = pluginAction.props.get("channelSelector", "").strip()
        self.logger.info(f"🎧 User selected SiriusXM channel ID: '{chan_id}'")

        self.logger.debug(f"📦 Dumping {len(self.Sonos.siriusxm_channels)} SiriusXM channels from cache...")

        for idx, ch in enumerate(self.Sonos.siriusxm_channels):
            cid = ch.get("id", "")
            num = ch.get("channelNumber", "")
            name = ch.get("name", "")
            stream = ch.get("streamUrl", "—")
            self.logger.debug(f"🔎 [{idx}] id='{cid}' | number='{num}' | name='{name}' | streamUrl='{stream}'")

        self.logger.debug("🧪 Skipping channel match and playback — this is a data dump only.")




#! /usr/bin/env python
# -*- coding: utf-8 -*-
#


# imports_successful = True

# ============================== Native Imports ===============================
import os
import platform
import sys
import traceback
# import aiohttp

# =================== requirements.txt imports ==================
import_errors = []
try:
    from twisted.internet import reactor
    from twisted.internet.protocol import DatagramProtocol
    from twisted.application.internet import MulticastServer
except ImportError:
    import_errors.append("twisted")

try:
    from gtts import gTTS
except ImportError:
    import_errors.append("gTTS")

try:
    import pyvona
except ImportError:
    import_errors.append("pyvona")

try:
    import boto3
except ImportError:
    import_errors.append("boto3")

try:
    from mutagen.mp3 import MP3
    from mutagen.aiff import AIFF
except ImportError:
    import_errors.append("mutagen")

try:
    import urllib
    import urllib.parse
    from urllib.request import urlopen
    import urllib.request
except ImportError:
    import_errors.append("urllib")

# ============================== Custom Imports ===============================
try:
    # noinspection PyUnresolvedReferences
    import indigo
except ImportError:
    pass

from pandora import Pandora

# ============================== Plugin Imports ===============================
from constants import *


indiPref_plugin_stopped = """<?xml version="1.0" encoding="UTF-8"?>
<Prefs type="dict">
    <plugin_stopped type="bool">true</plugin_stopped>
</Prefs>

"""


class Plugin(indigo.PluginBase):


    ######################################################################################
    # class init & del
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

        # Initialise dictionary to store plugin Globals
        self.globals = dict()

        self.Sonos = None
        self.pluginPrefs = pluginPrefs

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
        self.logger.info("Plugin logging now started.")

        self.debug = False
        self.xmlDebug = False
        self.eventsDebug = False
        self.stateUpdatesDebug = False
        self.StopThread = False


        # ✅ Instantiate SonosPlugin here
        try:
            from Sonos import SonosPlugin
            self.Sonos = SonosPlugin(self, self.pluginPrefs)
            # plugin.py
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize SonosPlugin: {e}")
            self.Sonos = None

        self.logger.info("Plugin __init__ ended.")

    def __del__(self):
        indigo.PluginBase.__del__(self)


    # plugin.py
    def getSiriusXMChannelList(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getSiriusXMChannelList(filter, valuesDict, typeId, targetId)




    def actionControlDevice(self, pluginAction, dev):
        method_name = pluginAction.pluginTypeId
        if hasattr(self.Sonos, method_name):
            getattr(self.Sonos, method_name)(pluginAction, dev)
        else:
            self.logger.warning(f"⚠️ Unknown action requested: {method_name}")



    #################################################################################################
    ### Nenu Specific Action Processing Definitions as parsed from menus.xml and called to sonos.py
    #################################################################################################

    def menuTestSiriusXMChannel(self):
        try:
            if self.Sonos is None:
                self.logger.error("❌ Sonos instance not initialized.")
                return

            # ✅ Real Sonos test device ID
            test_device_id = 261044601  # CR Sonos player

            if test_device_id in indigo.devices:
                dev = indigo.devices[test_device_id]
                self.logger.info(f"🔊 Running SiriusXM channel test on: {dev.name}")
                self.Sonos.menutestSiriusXMChannelChange(dev)
            else:
                self.logger.error(f"❌ Device ID {test_device_id} not found.")

        except Exception as e:
            self.logger.error(f"❌ Error in menuTestSiriusXMChannel: {e}")



    def menuDumpSiriusXMChannels(self):
        if not self.Sonos or not hasattr(self.Sonos, "dump_siriusxm_channels_to_log"):
            self.logger.warning("🚫 Sonos instance or dump method is missing.")
            return

        self.logger.info("📦 Invoking Sonos → dump_siriusxm_channels_to_log()...")
        self.Sonos.dump_siriusxm_channels_to_log()



    def menuDeleteandDefineSiriusXMChannels(self):
        self.logger.info("📦 Invoking Sonos → delete and define method...")
        self.Sonos.DeleteandDefine_SiriusXMCache()




    #################################################################################################
    ### End of Nenu Specific Action Defunitions
    #################################################################################################

    def display_plugin_information(self):
        try:
            import soco            
            soco_version = getattr(soco, '__version__', 'unknown')
            soco_path = getattr(soco, '__file__', 'unknown')

            def plugin_information_message():
                lines = []
                lines.append("Plugin Information:\n")
                lines.append(f"{'Plugin Name:':<30} {self.globals[PLUGIN_INFO][PLUGIN_DISPLAY_NAME]}")
                lines.append(f"{'Plugin Version:':<30} {self.globals[PLUGIN_INFO][PLUGIN_VERSION]}")
                lines.append(f"{'Plugin ID:':<30} {self.globals[PLUGIN_INFO][PLUGIN_ID]}")
                lines.append(f"{'Indigo Version:':<30} {indigo.server.version}")
                lines.append(f"{'Indigo License:':<30} {indigo.server.licenseStatus}")
                lines.append(f"{'Indigo API Version:':<30} {indigo.server.apiVersion}")
                lines.append(f"{'Architecture:':<30} {platform.machine()}")
                lines.append(f"{'Python Version:':<30} {sys.version.split(' ')[0]}")
                lines.append(f"{'Mac OS Version:':<30} {platform.mac_ver()[0]}")
                lines.append(f"{'Plugin Process ID:':<30} {os.getpid()}")
                lines.append(f"{'SoCo Version:':<30} {soco_version}")
                lines.append(f"{'SoCo Path:':<30} {soco_path}")

                max_length = max(len(line) for line in lines[1:])  # Skip header
                separator = f"{'':={'^'}{max_length}}"
                return "\n".join([lines[0], separator] + lines[1:] + [separator])

            self.logger.info(plugin_information_message())

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    def exception_handler(self, exception_error_message, log_failing_statement):
        filename, line_number, method, statement = traceback.extract_tb(sys.exc_info()[2])[-1]
        module = filename.split('/')
        log_message = f"'{exception_error_message}' in module '{module[-1]}', method '{method} [{self.globals[PLUGIN_INFO][PLUGIN_VERSION]}]'"
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
            self.logger.info("Plugin startup started.")

            if len(import_errors):
                stop_message = "Plugin startup cancelled due to one or more required plugin Python libraries missing:\n"
                for package in import_errors:
                    stop_message = f"{stop_message}      - {package}\n"
                return stop_message

            from Sonos import SonosPlugin
            self.logger.warning(f"🧪 Attempting to call deviceStartComm on object of type: {type(self.Sonos)}")
            self.logger.debug(f"🧪 Methods available: {dir(self.Sonos)}")

            self.Sonos.startup()  # ✅ <-- This was commented out
            self.display_plugin_information()
            self.logger.info("Plugin startup ended.")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement




    def shutdown(self):
        try:
            self.logger.debug("Method: shutdown")
            if self.Sonos is not None:
                self.Sonos.shutdown()

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # ConcurrentThread: Start & Stop
#    def runConcurrentThread(self):
#        try:
#            self.sleep(5.0)  # Delay start of concurrent thread
#
#            if self.Sonos is not None:
#                self.Sonos.runConcurrentThread()
#            else:
#                self.StopThread = True
#
#        except Exception as exception_error:
#            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def stopConcurrentThread(self):
        try:
            self.StopThread = True
            if self.Sonos is not None:
                self.Sonos.stopConcurrentThread()

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


    def deviceStartComm(self, dev):
        try:
            self.logger.warning(f"🧪 plugin.py deviceStartComm() CALLED for {dev.name}")
            if self.Sonos is not None:
                self.Sonos.deviceStartComm(dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)




    def deviceStopComm(self, dev):
        try:
            if self.Sonos is not None:
                self.Sonos.deviceStopComm(dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        try:
            if self.Sonos is not None:
                return self.Sonos.closedPrefsConfigUi(valuesDict, userCancelled)
            else:
                return valuesDict, userCancelled

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # UI Validation
    def validatePrefsConfigUi(self, valuesDict):
        try:
            self.logger.debug("Validating Plugin Configuration")
            errorsDict = indigo.Dict()
            if valuesDict["rootZPIP"] == "":
                errorsDict["rootZPIP"] = "Please enter a reference ZonePlayer IP Address."
            if valuesDict["EventProcessor"] == "":
                errorsDict["EventProcessor"] = "Please select an Event Processsor."
            if valuesDict["EventIP"] == "":
                errorsDict["EventIP"] = "Please select an Event Listener IP Address."
            if valuesDict["EventCheck"] == "":
                errorsDict["EventCheck"] = "Please select an Event Check Interval."
            if valuesDict["SubscriptionCheck"] == "":
                errorsDict["SubscriptionCheck"] = "Please select an Subscription Check Interval."
            if valuesDict["HTTPStreamingIP"] == "":
                errorsDict["rootZPIP"] = "Please enter an HTTP Streaming IP Address."
            if valuesDict["HTTPStreamingPort"] == "":
                errorsDict["rootZPIP"] = "Please enter an HTTP Streaming Port."
            if valuesDict["Pandora"] == "True":
                if valuesDict["PandoraEmailAddress"] == "":
                    errorsDict["PandoraEmailAddress"] = "Please enter a Pandora Email Address."
                if valuesDict["PandoraPassword"] == "":
                    errorsDict["PandoraPassword"] = "Please enter a Pandora Password."
            if valuesDict["SiriusXM"] == "True":
                if valuesDict["SiriusXMID"] == "":
                    errorsDict["SiriusXMID"] = "Please enter a SiriusXM ID."
                if valuesDict["SiriusXMPassword"] == "":
                    errorsDict["SiriusXMPassword"] = "Please enter a SiriusXM Password."
            if valuesDict["IVONA"] == "True":
                if valuesDict["IVONAaccessKey"] == "":
                    errorsDict["IVONAaccessKey"] = "Please enter an IVONA Access Key."
                if valuesDict["IVONAsecretKey"] == "":
                    errorsDict["IVONAsecretKey"] = "Please enter an IVONA Secret Key."
            if valuesDict["Polly"] == "True":
                if valuesDict["PollyaccessKey"] == "":
                    errorsDict["PollyaccessKey"] = "Please enter a Polly Access Key."
                if valuesDict["PollysecretKey"] == "":
                    errorsDict["PollysecretKey"] = "Please enter a Polly Secret Key."
            if valuesDict["MSTranslate"] == "True":
                if valuesDict["MSTranslateClientID"] == "":
                    errorsDict["MSTranslateClientID"] = "Please enter a Microsoft Translate Client ID."
                if valuesDict["MSTranslateClientSeret"] == "":
                    errorsDict["MSTranslateClientSecret"] = "Please enter an Microsoft Translate Client Secret."

            if len(errorsDict) > 0:
                self.logger.error("\t Validation Errors")
                return False, valuesDict, errorsDict
            else:
                self.logger.debug("\t Validation Succesful")
                return True, valuesDict

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################




    ###########################################################################################################
    # Action Menthods - set here to map the pannel actions with names and methods in sonos.py to be called. 
    ###########################################################################################################

    def actionZP_SiriusXM(self, pluginAction, dev):
        self.logger.info("🪪 Entered plugin.py::actionZP_SiriusXM")
        self.Sonos.actionZP_SiriusXM(pluginAction, dev)  # ✅ Delegate properly

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

    def actionVolumeUp(self, pluginAction, dev):
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

    def actionQ_Crossfade(self, pluginAction, dev):
        try:
            if self.Sonos:
                self.Sonos.handleAction_Q_Crossfade(pluginAction, dev)
            else:
                self.logger.error("❌ Sonos plugin instance not initialized.")
        except Exception as e:
            self.logger.error(f"❌ Error in actionQ_Crossfade: {e}")



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

    def actionZP_TV(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_TV")

    def actionZP_DumpURI(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "ZP_DumpURI")

    def actionPandora_ThumbsUp(self, pluginAction):
        return self.Sonos.actionPandoraThumbs(pluginAction, "thumbs_up")

    def actionPandora_ThumbsDown(self, pluginAction):
        return self.Sonos.actionPandoraThumbs(pluginAction, "thumbs_down")

    def actionTestSiriusXMChannel(self, pluginAction, dev):
        self.logger.info(f"Running testSiriusXMChannel for {dev.name}")
        self.Sonos.testSiriusXMChannelChange(dev)

    def dumpSiriusXMChannelsToLog(self):
        self.Sonos.dump_siriusxm_channels_to_log()

    def DeleteandDefineSiriusXMChannels(self):
        self.Sonos.DeleteandDefine_siriusxm_channels()

    def actionBassUp(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "BassUp")

    def actionBassDown(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "BassDown")

    def actionTrebleUp(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "TrebleUp")

    def actionTrebleDown(self, pluginAction):
        return self.Sonos.actionDirect(pluginAction, "TrebleDown")

    def menuDebugSubscriptions(self):
        try:
            if self.Sonos is not None:
                self.Sonos.diagnoseSubscriptions()
            else:
                self.logger.error("❌ Sonos instance not initialized.")
        except Exception as e:
            self.logger.error(f"❌ Error running menuDebugSubscriptions: {e}")



    def getSiriusXMChannels(self, filter="", valuesDict=None, typeId="", targetId=0):
        self.logger.warning("📥 Indigo requested SiriusXM channel list (getSiriusXMChannels called)")
        channels = getattr(self.Sonos, "siriusxm_channels", [])
        menu = []

        for ch in channels:
            try:
                name = ch["name"]
                number = str(ch["channelNumber"])
                menu.append((number, f"{number} - {name}"))
            except KeyError:
                continue

        if not menu:
            menu.append(("none", "No channels available"))

        return menu


###
    def getDeviceActionConfigUiValues(self, pluginProps, typeId, devId):
        valuesDict = indigo.Dict()
        errorsDict = indigo.Dict()

        if typeId == "ZP_SiriusXM":
            try:
                channels = self.Sonos.siriusxm_channels
                valuesDict["channelNameList"] = [ch["title"] for ch in channels]
            except Exception as e:
                self.logger.error(f"Error loading SiriusXM channel list: {e}")
                valuesDict["channelNameList"] = []
        return (valuesDict, errorsDict)

    def getSonosPlaylists(self, filter="", valuesDict=None, typeId="", targetId=0):
        try:
            import collections
            menu = []
            global Sonos_Playlists

            if not Sonos_Playlists:
                self.logger.warning("⚠️ Sonos_Playlists is empty — did getPlaylistsDirect() run?")
            else:
                self.logger.info(f"📜 Returning {len(Sonos_Playlists)} playlists for control panel dropdown")

            # Build Indigo menu entries as (value, label)
            for uri, name, id in Sonos_Playlists:
                # Normally you'd want to use id or uri — we assume id → SQ:#
                menu.append((f"SQ:{id}", name))

            if not menu:
                menu.append(("", "-- No playlists found --"))

            return collections.OrderedDict(menu)

        except Exception as e:
            self.logger.error(f"❌ getSonosPlaylists() failed: {e}")
            return [("", "Error loading playlists")]




    ###########################################################################################################
    # Action Plugin Menthods Menu Items - set here to map the plugin menu actions with names and methods
    # in sonos.py that will be called upon their selection. 
    ###########################################################################################################

    def get_channelNameList(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.Sonos.getZP_SiriusXM()



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