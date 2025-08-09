import urllib.parse
import datetime  # ✅ Needed for fallback print timestamp
import io
import sys
import os
from os import listdir
import copy
import json
import time
import html
import shutil
import logging
import threading
import http.server
import socketserver
import platform
import socket
import traceback
import ipaddress
import inspect
import base64
import ifaddr
import re
import requests
import http.server as BaseHTTPServer
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from xml.etree import ElementTree as ET
import xml.sax.saxutils as saxutils
from urllib import request, parse
from urllib.parse import urlparse

from AppKit import NSSpeechSynthesizer  # noqa
from AppKit import NSURL  # noqa

from PIL import Image
import io

try:
    import indigo
except ImportError:
    pass

import soco
import soco.core
import soco.events
import soco.config
from soco.core import SoCo
from soco import SoCo as SoCoDevice
from soco.events import event_listener
soco.config.EVENTS_MODULE = soco.events
logging.getLogger("Plugin.Sonos").info(
    f"🧪 The SoCo version used in this plugin was loaded from: {soco.__file__}"
)

try:
    from twisted.internet import reactor
    from twisted.internet.protocol import DatagramProtocol
    from twisted.application.internet import MulticastServer
except ImportError:
    pass

try:
    from gtts import gTTS
except ImportError:
    pass

try:
    import pyvona
except ImportError:
    pass

try:
    import boto3
except ImportError:
    pass

try:
    from mutagen.mp3 import MP3
    from mutagen.aiff import AIFF
except ImportError:
    pass

try:
    from pandora import Pandora
except ImportError:
    pass

# mini_http_server.py
import http.server
import socketserver


from XMhelper import SiriusXM
from sxm import SXMClient, RegionChoice, XMChannel
import language_codes
from constants import PLUGIN_INFO, PLUGIN_VERSION

print(f"Using SoCo event listener class: {type(event_listener).__name__}")

SONOS_ZonePlayer = 0
SONOS_CONNECT = 1
SONOS_CONNECTAMP = 2
SONOS_PLAY1 = 3
SONOS_PLAY3 = 4
SONOS_PLAY5 = 5
SONOS_PLAYBAR = 6
SONOS_SUB = 7
SONOS_PLAYBASE = 8
SONOS_BEAM = 9
SONOS_ERA100 = 10
SONOS_ERA300 = 11

ZP_LIST = []
Sonos_Favorites = []
Sonos_Playlists = []
Sonos_RT_Fav_Stations = []
Sonos_LineIn = []
Sonos_Pandora = []
Sonos_SiriusXM = []
SavedState = []
Sound_Files = []
ContainerUpdateID_SQ = 0
actionBusy = 0





UPNP_ERRORS = {
    '400': 'Bad Request',
    '401': 'Invalid Action',
    '402': 'Invalid Args',
    '404': 'Invalid Var',
    '412': 'Precondition Failed',
    '501': 'Action Failed',
    '600': 'Argument Value Invalid',
    '601': 'Argument Value Out of Range',
    '602': 'Optional Action Not Implemented',
    '603': 'Out of Memory',
    '604': 'Human Invtervention Required',
    '605': 'String Argument Too Long',
    '606': 'Action Not Authorized',
    '607': 'Signature Failure',
    '608': 'Signature Missing',
    '609': 'Not Encrypted',
    '610': 'Invalid Sequence',
    '611': 'Invalid Control URL',
    '612': 'No Such Session',
    '701': 'No Such Object',
    '702': 'Invalid CurrentTagValue',
    '703': 'Invalid NewTagValue',
    '704': 'RequiredTag',
    '705': 'Read Only Tag',
    '706': 'Parameter Mismatch',
    '708': 'Unsupported or Invalid Search Criteria',
    '709': 'Unsupported or Invalid Sort Criteria',
    '710': 'No Such Container',
    '711': 'Restricted Object',
    '712': 'Bad Metadata',
    '713': 'Restricted Parent Object',
    '714': 'No Such Source Resource',
    '715': 'Resource Access Denied',
    '716': 'Transfer Busy',
    '717': 'No Such File Transfer',
    '718': 'No Such Destination Resource',
    '719': 'Destination Resource Access Denied',
    '720': 'Cannot Process the Request',
    '800': 'Unable to Play the Selected Item',
    '804': 'Invalid Queue Request'
}

uri_tv = "x-sonos-htastream:"
uri_music = "x-rincon-queue:"
uri_radio = "x-sonosapi-stream:"
uri_sonos_radio = "x-sonosapi-radio:"
uri_sonos_http = "x-sonosapi-http:"
uri_pandora = "pndrradio:"
uri_siriusxm = "x-sonosapi-hls:"
uri_spotify = "x-sonos-spotify:"
uri_jffs = "file:"
uri_file = "x-file-cifs"
uri_group = "x-rincon:"
uri_playlist = "x-rincon-playlist:"
uri_mp3radio = "x-rincon-mp3radio:"
uri_container = "x-rincon-cpcontainer"

ZoneGroupStates = {
    'ZP_ALBUM', 'ZP_ARTIST', 'ZP_SOURCE', 'ZP_MUTE','ZP_CREATOR', 'ZP_TRACK', 'ZP_NALBUM',
    'ZP_NART', 'ZP_NARTIST', 'ZP_NCREATOR', 'ZP_NTRACK', 'ZP_CurrentTrack',
    'ZP_CurrentTrackURI', 'ZP_DURATION', 'ZP_RELATIVE', 'ZP_INFO',
    'ZP_STATION', 'ZP_STATE'
}

IVONAlanguages = {
    'en-US': 'English, American',
    'en-AU': 'English, Australian',
    'en-GB': 'English, British',
    'en-IN': 'English, Indian',
    'en-GB-WLS': 'English, Welsh',
    'cy-GB': 'Welsh',
    'da-DK': 'Danish',
    'nl-NL': 'Dutch',
    'fr-FR': 'French',
    'fr-CA': 'French, Canadian',
    'de-DE': 'German',
    'is-IS': 'Icelandic',
    'it-IT': 'Italian',
    'pl-PL': 'Polish',
    'pt-PT': 'Portuguese',
    'pt-BR': 'Portuguese, Brazilian',
    'ro-RO': 'Romanian',
    'ru-RU': 'Russian',
    'es-ES': 'Spanish, Castilian',
    'es-US': 'Spanish, American',
    'sv-SE': 'Swedish',
    'tr-TR': 'Turkish',
    'nb-NO': 'Norwegian'
}

IVONAVoices = []
PollyVoices = []
NSVoices = []


class Old_save_PA():
    def __init__(self, deviceId=None, props=None):
        self.deviceId = deviceId
        self.props = props


# Safe PluginAction helper (drop-in replacement)
class PA(object):
    def __init__(self, deviceId=None, props=None):
        # Always store deviceId as int when possible
        try:
            self.deviceId = int(deviceId) if deviceId is not None else 0
        except Exception:
            self.deviceId = deviceId  # fallback

        # Normalize props to a dict-like object
        norm = {}
        if isinstance(props, dict):
            norm = dict(props)  # shallow copy
        elif props is None:
            norm = {}
        else:
            # last-ditch: try to coerce to dict
            try:
                norm = dict(props)
            except Exception:
                norm = {}

        # Coerce 'setting' to str if present (prevents .split on int, etc.)
        if "setting" in norm and not isinstance(norm["setting"], str):
            try:
                norm["setting"] = str(norm["setting"])
            except Exception:
                norm["setting"] = ""

        # Prefer Indigo's Dict if available so .get() behaves like elsewhere
        try:
            d = indigo.Dict()
            for k, v in norm.items():
                d[k] = v
            self.props = d
        except Exception:
            self.props = norm







class SonosPlugin(object):

    ############################################################################################
    ### Initialize the SonosPlugin
    ############################################################################################

    # Define the class-level attribute
    #DEFAULT_ARTWORK_PATH = '/Library/Application Support/Perceptive Automation/images/Sonos/'
    DEFAULT_ARTWORK_PATH = '/Library/Application Support/Perceptive Automation/images/Sonos/default_artwork copy.jpg'    

    def __init__(self, plugin, pluginPrefs):
        import uuid
        import os
        import json
        from sxm import SXMClient, RegionChoice, XMChannel


        self.logger = logging.getLogger("Plugin.Sonos")
        self.logger.info(f"Initializing SonosPlugin... [{uuid.uuid4()}]")

        import threading

        self.plugin = plugin
        self.pluginPrefs = pluginPrefs  # ✅ Must be assigned first


        self.last_zone_group_state_hash = None
        self.zone_group_state_lock = threading.Lock()

        self.plugin = plugin
        self.pluginPrefs = pluginPrefs
        self.logger = logging.getLogger("Plugin.Sonos")
        self.soco_by_ip = {}
        self.ip_to_indigo_device = {}
        self.uuid_to_soco = {}
        self.zone_group_state_cache = {}  # ✅ ensure this exists early

        self.httpd = None
        self.httpd_thread = None


        self.targetSonosSubnet = self.pluginPrefs.get("sonosTargetSubnet", "192.168.80.0/24")

        self.logger = logging.getLogger("Plugin.Sonos")
        self.logger.info(f"Initializing SonosPlugin... [{uuid.uuid4()}]")

        # Safe access to pluginPrefs
        self.Pandora = self.pluginPrefs.get("Pandora")
        self.PandoraEmailAddress = self.pluginPrefs.get("PandoraEmailAddress")
        self.PandoraPassword = self.pluginPrefs.get("PandoraPassword")
        self.PandoraNickname = self.pluginPrefs.get("PandoraNickname")

        global Sonos_Pandora
        if self.Pandora and self.PandoraEmailAddress and self.PandoraPassword and not Sonos_Pandora:
            self.logger.info("🔁 Preloading Pandora stations at init.")
            Sonos_Pandora = []  # Clear global list to ensure fresh load
            self.getPandora(self.PandoraEmailAddress, self.PandoraPassword, self.PandoraNickname)

        # ... continue your normal init process ...


        self.globals = plugin.globals

        # Init internal structures
        self.devices = {}
        self.deviceList = []
        self.event_threads = {}
        self.soco_subs = {}
        self.soco_sub = {}
        self.event_listener_started = False
        self.ZonePlayers = []
        self.ZPTypes = []
        self.zonePlayerState = {}
        self.SoundFilePath = None
        self.ttsORfile = None
        self.first_working_stream = None

        self.control_point = None
        self.SonosDeviceID = None
        self.rootZPIP = None
        self.find_sonos_interface_ip()

        # Voice + credentials init
        self.Pandora = self.PandoraEmailAddress = self.PandoraPassword = self.PandoraNickname = None
        self.Pandora2 = self.PandoraEmailAddress2 = self.PandoraPassword2 = self.PandoraNickname2 = None
        self.SiriusXM = self.SiriusXMID = self.SiriusXMPassword = None
        self.IVONA = self.IVONAaccessKey = self.IVONAsecretKey = None
        self.Polly = self.PollyaccessKey = self.PollysecretKey = None
        self.MSTranslate = self.MSTranslateClientID = self.MSTranslateClientSecret = None
        self.MSTranslateVoices = {}
        self.myLocale = None

        self.SonArray = [{}]
        self.EventProcessor = "SoCo"
        self.EventIP = None
        self.EventCheck = None
        self.SubscriptionCheck = None
        self.HTTPStreamingIP = None
        self.HTTPStreamingPort = None
        self.HTTPStreamerOn = False
        self.HTTPServer = None
        self.httpd = None

        self.siriusxm = None
        self.siriusxm_channels = []
        self.Sonos_SiriusXM = []
        self.siriusxm_id_map = {}
        self.siriusxm_guid_map = {}
        self.last_siriusxm_guid_by_dev = {}
        self.soco_by_ip = {}
        self.soco_devices = {}
        self.ip_to_indigo_device = {}
        self.ip_to_soco_device = {}  # Maps IP -> SoCo object

        self.uuid_to_indigo_device = {}  # ✅ Required for dump_groups_to_log

        self.group_name_by_device_id = {}

        # Hardcoded fallback test entries
        self.siriusxm_guid_map.update({
            "spa73": {"guid": "66e2c540-b3f3-4934-80cd-578f30e3dbb3", "name": "Spa", "channelNumber": "73"},
            "deeptracks308": {"guid": "e3041d19-daa5-6517-8c73-41976582d1f9", "name": "Deep Tracks", "channelNumber": "308"},
            "80stop500551": {"guid": "6be4367a-f423-68eb-1a5e-76ef11a8970e", "name": "80s on 8 Top 500", "channelNumber": "551"},
            "pettyburiedtreasure711": {"guid": "f95497ef-39c0-66fd-5749-f6c7b6f768b9", "name": "Petty's Buried Treasure", "channelNumber": "711"}
        })

        # Run SiriusXM channel loading (cache or live)
        self.load_siriusxm_channel_data()

        self.sorted_siriusxm_guids = sorted(
            [chan["channelGuid"] for chan in self.siriusxm_channels if chan.get("channelGuid")],
            key=lambda g: next((int(c["channelNumber"]) for c in self.siriusxm_channels if c.get("channelGuid") == g), 9999)
        )

        # At __init__, add:
        self.device_zone_ips = {}

        self.parsed_zone_group_state_by_ip = {}


        self.device_zone_ips = {}
        self.parsed_zone_group_state_by_ip = {}


        self.soco_by_dev = {}

        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            uuid = dev.states.get("uuid", None)
            if not uuid:
                continue
            soco = self.soco_devices_by_uuid.get(uuid)
            if soco:
                self.soco_by_dev[dev.id] = soco




        # ✅ Rebuild uuid_to_indigo_device mapping
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            soco = self.soco_devices.get(dev.address)
            if soco:
                try:
                    self.uuid_to_indigo_device[soco.uid] = dev
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not map UUID for device '{dev.name}': {e}")



    ############################################################################################
    ### Ensure MP3s are visible in action dialog after reload
    ############################################################################################
    def getActionConfigUiValues(self, pluginAction, typeId, devId):
        try:
            self.logger.debug(f"🎛️ getActionConfigUiValues called for action type: {typeId}")
            self.getSoundFiles()  # Refresh MP3 list every time UI loads
            return pluginAction.props, indigo.Dict()
        except Exception as e:
            self.logger.error(f"❌ Error in getActionConfigUiValues: {e}")
            return pluginAction.props, indigo.Dict()






        self.getSoundFiles()



    def getSoundFilesList(self, filter="", valuesDict=None, typeId="", targetId=0):
        try:
            if not hasattr(self, 'Sound_Files') or not self.Sound_Files:
                self.getSoundFiles()
            return [(f, f) for f in sorted(self.Sound_Files)]
        except Exception as e:
            self.logger.error(f"❌ Error in getSoundFilesList(): {e}")
            return []


    ### End of Initialization


    ############################################################################################
    ### Actiondirect List Processing
    ############################################################################################

    def actionDirect(self, pluginAction, action_id_override=None):

        try:
            #self.logger.warning("🧪 [LOG 0] Entered actionDirect")

            # Normalize simplified override names into internal action IDs
            action_map = {
                "Play": "actionPlay",
                "TogglePlay": "actionTogglePlay",
                "Pause": "actionPause",
                "Stop": "actionStop",
                "Next": "actionNext",
                "Previous": "actionPrevious",
                "MuteToggle": "actionMuteToggle",
                "MuteOn": "actionMuteOn",
                "MuteOff": "actionMuteOff",
                "Volume": "actionVolume",
                "VolumeUp": "actionVolumeUp",
                "VolumeDown": "actionVolumeDown",
                "BassUp": "actionBassUp",
                "BassDown": "actionBassDown",
                "TrebleUp": "actionTrebleUp",
                "TrebleDown": "actionTrebleDown",
                "setStandalone": "setStandalone",
                "actionsetStandalone": "setStandalone",
                "setStandalones": "setStandalones",
                "actionsetStandalones": "setStandalones",
                "addPlayerToZone": "actionZP_addPlayerToZone",
                "GroupMuteToggle": "actionGroupMuteToggle",
                "GroupMuteOn": "actionGroupMuteOn",
                "GroupMuteOff": "actionGroupMuteOff",
                "GroupVolumeUp": "actionGroupVolumeUp",
                "GroupVolumeDown": "actionGroupVolumeDown",
                "NightMode": "actionNightMode",
                "ZP_Pandora": "actionZP_Pandora",
                "ZP_SiriusXM": "actionZP_SiriusXM",
                "ZP_TV": "actionZP_TV",
                "ZP_DumpURI": "actionZP_DumpURI",
                "ChannelUp": "actionChannelUp",
                "ChannelDown": "actionChannelDown",
                "Q_ShuffleToggle": "actionQ_ShuffleToggle",
                "Q_Shuffle": "actionQ_Shuffle",
                "ZP_SonosFavorites": "ZP_SonosFavorites",
                "ZP_SonosRadio": "ZP_SonosRadio",
                "ZP_Container": "ZP_Container",
                "Q_RepeatToggle": "actionQ_RepeatToggle",
                # allow both public and "action..." forms (reverse mappings)
                "actionGroupMuteOff": "GroupMuteOff",
                "actionGroupMuteOn": "GroupMuteOn",
                "actionGroupMuteToggle": "GroupMuteToggle",
                "actionGroupVolume": "GroupVolume",
                "actionRelativeGroupVolume": "RelativeGroupVolume",
            }

            raw_key = action_id_override or pluginAction.pluginTypeId
            #self.logger.warning(f"🧪 [LOG 1] raw_key: {raw_key}")
            action_key = action_map.get(raw_key, raw_key)
            action_id = action_key
            #self.logger.warning(f"🧪 [LOG 2] action_id resolved to: {action_id}")

            # Dispatch handler mapping (global or device-aware)
            dispatch_table = {
                "SetSiriusXMChannel":        lambda p, d, z: self.handleAction_SetSiriusXMChannel(p, d, z),
                "actionZP_SiriusXM":         lambda p, d, z: self.handleAction_ZP_SiriusXM(p, d, z),
                "actionZP_Pandora":          lambda p, d, z: self.handleAction_ZP_Pandora(p, d, z, p.props),
                "actionChannelUp":           lambda p, d, z: self.handleAction_ChannelUp(p, d, z),
                "actionChannelDown":         lambda p, d, z: self.handleAction_ChannelDown(p, d, z),
                "actionZP_addPlayerToZone":  lambda p, d, z: self.handleAction_ZP_addPlayerToZone(p, d, z),
                "actionQ_Shuffle":           lambda p, d, z: self.handleAction_Q_Shuffle(p, d, z),
                "actionQ_Crossfade":         lambda p, d, z: self.handleAction_Q_Crossfade(p, d, z),
            }

            device_id = int(pluginAction.deviceId)
            #self.logger.warning(f"🧪 [LOG 3] pluginAction.deviceId: {device_id}")

            # === Global Actions (e.g., from Control Pages) ===
            if device_id == 0:
                #self.logger.warning(f"🧪 [LOG 3.5] Global action (deviceId = 0) detected: {action_id}")

                if action_id == "setStandalones":
                    self.logger.warning(f"I am going to set standalones from a state where they are grouped")
                    zones = []
                    for x in range(1, 13):
                        ivar = f'zp{x}'
                        val = pluginAction.props.get(ivar)
                        if val and val != "00000":
                            zones.append(val)

                    for item in zones:
                        try:
                            dev = indigo.devices[int(item)]
                            self.logger.info(f"🔁 Un-grouping device: {dev.name}")
                            if dev.states.get("GROUP_Coordinator") == "true":
                                self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport",
                                              "BecomeCoordinatorOfStandaloneGroup", "")
                            self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport",
                                          "SetAVTransportURI",
                                          f"<CurrentURI>x-rincon-queue:{dev.states['ZP_LocalUID']}#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                            #DT_Test
                            self.logger.warning(f"DT_Test")
                            self.refresh_group_topology_after_plugin_zone_change()
                            self.refresh_all_group_states()
                            self.evaluate_and_update_grouped_states()
                        except Exception as e:
                            self.logger.error(f"❌ Failed to ungroup device {item}: {e}")
                    return

                else:
                    self.logger.error(f"❌ Global action_id '{action_id}' not handled")
                    return

            # === Device-Based Actions ===
            try:
                dev = indigo.devices[device_id]
                #self.logger.warning(f"🧪 [LOG 4] dev.name: {dev.name}, ID: {dev.id}")
            except KeyError:
                self.logger.error(f"❌ Device ID {device_id} not found in Indigo database")
                return

            # Determine coordinator device and IP (single calculation)
            coordinator_dev = self.getCoordinatorDevice(dev)
            coordinator_ip = coordinator_dev.pluginProps.get("address", "").strip()

            # Assign correct target IP
            zoneIP = coordinator_ip
            if coordinator_dev.id != dev.id:
                self.logger.warning(f"🔁 Redirecting control from slave {dev.name} to coordinator {coordinator_dev.name} at {zoneIP}")
            else:
                self.logger.debug(f"✅ {dev.name} is the coordinator — using direct control")

            # Seed Coordinator* vars so later branches are safe
            CoordinatorIP = coordinator_ip
            CoordinatorDev = coordinator_dev

            # Fast-path: dedicated handlers
            if action_id in dispatch_table:
                dispatch_table[action_id](pluginAction, dev, zoneIP)
                return

            # === Transport Actions ===
            if action_id in ("actionPlay", "Play"):
                self.plugin.debugLog("Sonos Action: Play")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                self.logger.info(f"▶️ Play sent to {coordinator_dev.name}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", "PLAYING")
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: PLAYING")
                return

            #DT Here  (helper must NOT chain into action dispatch)
            if dev.states["GROUP_Coordinator"] == "false":
                Coordinator = dev.states["GROUP_Name"]
                for idev in indigo.devices.iter("self.ZonePlayer"):
                    if idev.states["GROUP_Coordinator"] == "true" and idev.states["GROUP_Name"] == Coordinator:
                        CoordinatorIP = idev.pluginProps["address"]
                        CoordinatorDev = self.getCoordinatorDevice(dev)
                        break

            # === Start a NEW action dispatch chain (decoupled from the helper above) ===

            if action_id == "announcement":
                # Sanitize and normalize pluginAction.props['setting']
                raw_setting = pluginAction.props.get("setting") if pluginAction.props else None
                self.logger.debug(f"[🧪 pluginAction.props['setting']] Raw value: {raw_setting} ({type(raw_setting).__name__})")

                try:
                    if isinstance(raw_setting, int):
                        raw_setting = str(raw_setting)
                        self.logger.debug(f"[🔄] Converted integer 'setting' to string: {raw_setting}")
                    elif raw_setting is None:
                        self.logger.warning("[⚠️ WARN] pluginAction.props['setting'] is missing or None")
                        raw_setting = ""
                    elif not isinstance(raw_setting, str):
                        self.logger.warning(f"[⚠️ WARN] Unexpected 'setting' type: {type(raw_setting).__name__}")
                        raw_setting = str(raw_setting)

                    # Now split
                    if "||" in raw_setting:
                        zone_name, ip_addr = raw_setting.strip().split("||", 1)
                        self.logger.debug(f"[✅ Parsed setting] Zone = '{zone_name}', IP = '{ip_addr}'")
                    else:
                        zone_name = ip_addr = None
                        self.logger.error(f"[❌ INVALID] 'setting' does not contain expected '||' delimiter: {raw_setting}")

                except Exception as e:
                    self.logger.exception(f"[❌ Exception] Failed parsing 'setting': {e}")
                    zone_name = ip_addr = None

                # Log volume and file props
                volume = pluginAction.props.get("volume") if pluginAction.props else None
                file = pluginAction.props.get("file") if pluginAction.props else None

                self.logger.debug(f"[🔈 Volume Level] = {volume}")
                self.logger.debug(f"[🎵 File] = {file}")
                self.logger.debug(f"[🌐 Target IP] = {ip_addr}")
                return

            elif action_id in ("actionPause", "Pause"):
                self.plugin.debugLog("Sonos Action: Pause")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                self.logger.info(f"⏸ Pause sent to {coordinator_dev.name}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", "PAUSED_PLAYBACK")
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: PAUSED_PLAYBACK")
                return

            elif action_id in ("actionStop", "Stop"):
                self.plugin.debugLog("Sonos Action: Stop")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                self.logger.info(f"⏹ Stop sent to {coordinator_dev.name}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", "STOPPED")
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: STOPPED")
                return

            elif action_id in ("actionTogglePlay", "TogglePlay"):
                self.plugin.debugLog("Sonos Action: Toggle Play")
                current_state = coordinator_dev.states.get("ZP_STATE", "").upper()

                if current_state == "PLAYING":
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                    self.logger.info(f"⏸ TogglePlay → Pause sent to {coordinator_dev.name}")
                    new_state = "PAUSED_PLAYBACK"
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    self.logger.info(f"▶️ TogglePlay → Play sent to {coordinator_dev.name}")
                    new_state = "PLAYING"

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", new_state)
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: {new_state}")
                return

            # Mute Controls
            elif action_id in ("actionMuteToggle", "MuteToggle"):
                self.plugin.debugLog("Sonos Action: Mute Toggle")

                # dev.states["ZP_MUTE"] can be "0"/"1" or "true"/"false" (string) — normalize safely
                raw = dev.states.get("ZP_MUTE", 0)
                raw_s = str(raw).strip().lower()
                is_muted = raw_s in ("1", "true", "on", "yes")

                desired_mute = "0" if is_muted else "1"
                self.SOAPSend(
                    zoneIP,
                    "/MediaRenderer",
                    "/RenderingControl",
                    "SetMute",
                    f"<Channel>Master</Channel><DesiredMute>{desired_mute}</DesiredMute>"
                )

                indigo.server.log("ZonePlayer: %s, Mute %s" % (dev.name, "Off" if is_muted else "On"))
                return



            elif action_id in ("actionMuteOn", "MuteOn"):
                self.plugin.debugLog("Sonos Action: Mute On")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                indigo.server.log("ZonePlayer: %s, Mute On" % dev.name)
                return

            elif action_id in ("actionMuteOff", "MuteOff"):
                self.plugin.debugLog("Sonos Action: Mute Off")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                indigo.server.log("ZonePlayer: %s, Mute Off" % dev.name)
                return

            # Group Mute Controls
            elif action_id in ("actionGroupMuteToggle", "GroupMuteToggle"):
                self.plugin.debugLog("Sonos Action: Group Mute Toggle")

                # parseCurrentMute(...) may return "0"/"1" or "true"/"false" — normalize safely
                gmute_raw = self.parseCurrentMute(
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", "")
                )
                gmute_s = str(gmute_raw).strip().lower()
                group_is_muted = gmute_s in ("1", "true", "on", "yes")

                desired_group_mute = "0" if group_is_muted else "1"
                self.SOAPSend(
                    zoneIP,
                    "/MediaRenderer",
                    "/GroupRenderingControl",
                    "SetGroupMute",
                    f"<DesiredMute>{desired_group_mute}</DesiredMute>"
                )

                indigo.server.log("ZonePlayer Group: %s, Mute %s" % (dev.name, "Off" if group_is_muted else "On"))
                return


            elif action_id in ("actionGroupMuteOn", "GroupMuteOn"):
                self.plugin.debugLog("Sonos Action: Group Mute On")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>1</DesiredMute>")
                indigo.server.log("ZonePlayer Group: %s, Mute On" % dev.name)
                return

            elif action_id in ("actionGroupMuteOff", "GroupMuteOff"):
                self.plugin.debugLog("Sonos Action: Group Mute Off")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>0</DesiredMute>")
                indigo.server.log("ZonePlayer Group: %s, Mute Off" % dev.name)
                return

            # Group Volume Controls
            elif action_id in ("actionGroupVolume", "GroupVolume"):
                self.plugin.debugLog("Sonos Action: Group Volume")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = int(eval(self.plugin.substitute(pluginAction.props.get("setting"))))
                if new_volume < 0 or new_volume > 100:
                    new_volume = current_volume
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume", f"<DesiredVolume>{new_volume}</DesiredVolume>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionRelativeGroupVolume", "RelativeGroupVolume"):
                self.plugin.debugLog("Sonos Action: Relative Group Volume")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                adjustment = pluginAction.props.get("setting")
                try:
                    new_volume = int(current_volume) + int(adjustment)
                except Exception:
                    new_volume = current_volume
                new_volume = max(0, min(new_volume, 100))
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", f"<Adjustment>{adjustment}</Adjustment>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionGroupVolumeDown", "GroupVolumeDown"):
                self.plugin.debugLog("Sonos Action: Group Volume Down")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = max(0, int(current_volume) - 2)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>-2</Adjustment>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionGroupVolumeUp", "GroupVolumeUp"):
                self.plugin.debugLog("Sonos Action: Group Volume Up")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = min(100, int(current_volume) + 2)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>2</Adjustment>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionQ_Crossfade", "Q_Crossfade"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                mode = pluginAction.props.get("setting")
                if mode == 0:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>0</CrossfadeMode>")
                elif mode == 1:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>1</CrossfadeMode>")
                return

            elif action_id in ("actionQ_Repeat", "Q_Repeat"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat = bool(int(pluginAction.props.get("setting")))
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if repeat == True:
                    PlayMode = self.QMode(repeat, False, shuffle)
                else:
                    PlayMode = self.QMode(repeat, repeat_one, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_RepeatOne", "Q_RepeatOne"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat_one = bool(int(pluginAction.props.get("setting")))
                repeat = self.boolConv(dev.states["Q_Repeat"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if repeat_one == True:
                    PlayMode = self.QMode(False, repeat_one, shuffle)
                else:
                    PlayMode = self.QMode(repeat, repeat_one, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_RepeatToggle", "Q_RepeatToggle"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat = self.boolConv(dev.states["Q_Repeat"])
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if repeat == False and repeat_one == False:
                    PlayMode = self.QMode(True, False, shuffle)
                elif repeat == True and repeat_one == False:
                    PlayMode = self.QMode(False, True, shuffle)
                else:
                    PlayMode = self.QMode(False, False, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_Shuffle", "Q_Shuffle"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                shuffle = bool(int(pluginAction.props.get("setting")))
                repeat = self.boolConv(dev.states["Q_Repeat"])
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                PlayMode = self.QMode(repeat, repeat_one, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_ShuffleToggle", "Q_ShuffleToggle"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat = self.boolConv(dev.states["Q_Repeat"])
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if shuffle == True:
                    PlayMode = self.QMode(repeat, repeat_one, False)
                else:
                    PlayMode = self.QMode(repeat, repeat_one, True)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id == "Q_Clear":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/Queue", "RemoveAllTracks", "<QueueID>0</QueueID><UpdateID>0</UpdateID>")
                indigo.server.log("ZonePlayer: %s, Clear Queue" % dev.name)
                return

            elif action_id == "Q_Save":
                self.updateZoneTopology(dev)
                if dev.states["GROUP_Coordinator"] == "false":
                    self.plugin.debugLog("ZonePlayer: %s, Cannot Save Queue for Slave" % dev.name)
                else:
                    self.plugin.sleep(0.5)
                    PlaylistName = pluginAction.props.get("setting")
                    ZP  = self.parseBrowseNumberReturned(self.SOAPSend (zoneIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>Q:0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"))
                    if PlaylistName == "Indigo_" + dev.states['ZP_LocalUID']:
                        self.updateStateOnServer (dev, "Q_Number", ZP)
                    if int(ZP) > 0:
                        ObjectID = ""
                        for plist in Sonos_Playlists:
                            if plist[1] == PlaylistName:
                                ObjectID = plist[2]
                        AssignedObjectID = self.parseAssignedObjectID(self.SOAPSend (zoneIP, "/MediaRenderer", "/Queue", "SaveAsSonosPlaylist", "<QueueID>0</QueueID><Title>" + PlaylistName + "</Title><ObjectID>" + ObjectID + "</ObjectID>"))
                        if ObjectID == "":
                            ObjectID = AssignedObjectID
                        if PlaylistName.find(dev.states['ZP_LocalUID']) > -1:
                            self.updateStateOnServer (dev, "Q_ObjectID", ObjectID)

                        self.plugin.debugLog ("ZonePlayer: %s, Save Queue: %s" % (dev.name, PlaylistName))
                    else:
                        if PlaylistName == "Indigo_" + dev.states['ZP_LocalUID']:
                            ObjectID = ""
                            for plist in Sonos_Playlists:
                                if plist[1] == PlaylistName:
                                    ObjectID = plist[2]
                                    self.actionDirect(PA(dev.id, {"setting":ObjectID}), "CD_RemovePlaylist")
                            self.updateStateOnServer (dev, "Q_ObjectID", "")
                        self.plugin.debugLog ("ZonePlayer: %s, Nothing in Queue to Save" % dev.name)
                return

            elif action_id == "CD_RemovePlaylist":
                ObjectID = pluginAction.props.get("setting")
                for plist in Sonos_Playlists:
                    if plist[2] == ObjectID:
                        PlaylistName = plist[1]
                        self.SOAPSend (zoneIP, "/MediaServer", "/ContentDirectory", "DestroyObject", "<ObjectID>" + ObjectID + "</ObjectID>")
                indigo.server.log ("ZonePlayer: %s, Remove Playlist: %s" % (dev.name, PlaylistName))
                return

            elif action_id == "actionBassUp":
                current = int(dev.states.get("ZP_BASS", 0))
                newVal = max(min(current + 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass",
                              f"<DesiredBass>{newVal}</DesiredBass>")
                self.logger.info(f"🔊 Bass increased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionBassDown":
                current = int(dev.states.get("ZP_BASS", 0))
                newVal = max(min(current - 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass",
                              f"<DesiredBass>{newVal}</DesiredBass>")
                self.logger.info(f"🔉 Bass decreased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionTrebleUp":
                current = int(dev.states.get("ZP_TREBLE", 0))
                newVal = max(min(current + 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble",
                              f"<DesiredTreble>{newVal}</DesiredTreble>")
                self.logger.info(f"🎶 Treble increased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionTrebleDown":
                current = int(dev.states.get("ZP_TREBLE", 0))
                newVal = max(min(current - 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble",
                              f"<DesiredTreble>{newVal}</DesiredTreble>")
                self.logger.info(f"🎵 Treble decreased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return
        
            elif action_id == "actionVolume":
                self.logger.warning(f"[Debug] Received action_id: '{action_id}'")
                self.plugin.debugLog("Sonos Action: Volume")
                current_volume = dev.states["ZP_VOLUME"]
                new_volume = int(eval(self.plugin.substitute(pluginAction.props.get("setting"))))
                if new_volume < 0 or new_volume > 100:
                    new_volume = current_volume
                self.SOAPSend (zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume", "<Channel>Master</Channel><DesiredVolume>"+str(new_volume)+"</DesiredVolume>")
                indigo.server.log(u"ZonePlayer: %s, Current Volume: %s, New Volume: %s" % (dev.name, current_volume, new_volume))
                return

            elif action_id == "actionVolumeUp":
                self.safe_debug("🧪 Matched action_id == actionVolumeUp")

                # Pull volume from coordinator (not the slave!)
                current = int(coordinator_dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = min(100, current + 5)

                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")

                self.logger.info(f"🔊 Volume UP sent to {coordinator_dev.name}: {current} → {new_volume}")

                # If this was initiated from a slave, update its visible state to match
                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_VOLUME_MASTER", new_volume)
                    self.safe_debug(f"🔁 Synced ZP_VOLUME_MASTER from {coordinator_dev.name} → {dev.name}")
                return

            elif action_id == "actionVolumeDown":
                self.safe_debug("🧪 Matched action_id == actionVolumeDown")

                current = int(coordinator_dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = max(0, current - 5)

                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")

                self.logger.info(f"🔉 Volume DOWN sent to {coordinator_dev.name}: {current} → {new_volume}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_VOLUME_MASTER", new_volume)
                    self.safe_debug(f"🔁 Synced ZP_VOLUME_MASTER from {coordinator_dev.name} → {dev.name}")
                return

            elif action_id == "actionMuteToggle":
                self.safe_debug("🧪 Matched action_id == actionMuteToggle")

                # Get mute state from coordinator, not slave
                raw_state = coordinator_dev.states.get("ZP_MUTE", "unknown")
                mute_state = str(raw_state).lower() == "true"

                mute_val = "0" if mute_state else "1"
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              f"<Channel>Master</Channel><DesiredMute>{mute_val}</DesiredMute>")

                self.logger.info(f"🎚 Mute TOGGLE sent to {coordinator_dev.name}: {'Off' if mute_state else 'On'}")

                # Optionally update the slave state immediately
                if dev.id != coordinator_dev.id:
                    new_state = "false" if mute_state else "true"
                    dev.updateStateOnServer("ZP_MUTE", new_state)
                    self.safe_debug(f"🔁 Synced ZP_MUTE from {coordinator_dev.name} → {dev.name}: {new_state}")
                return

            elif action_id == "actionMuteOn":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                self.logger.info(f"🔇 Mute ON for {dev.name}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionMuteOff":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                self.logger.info(f"🔊 Mute OFF for {dev.name}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionStop":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "<InstanceID>0</InstanceID>")
                self.logger.info(f"⏹️ Stop triggered for {dev.name}")
                return

            elif action_id == "actionNext":
                uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
                self.safe_debug(f"🧪 Checking for SiriusXM stream in URI: {uri}")
                if "sirius" in uri.lower() or "x-sonosapi-" in uri.lower():
                    self.logger.info(f"📻 Detected SiriusXM stream — calling channelUpOrDown(up) for {dev.name}")
                    self.channelUpOrDown(dev, direction="up")
                    return
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Next", "<InstanceID>0</InstanceID>")
                    self.logger.info(f"⏭️ Next track for {dev.name}")
                    return

            elif action_id == "actionPrevious":
                uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
                self.safe_debug(f"🧪 Checking for SiriusXM stream in URI: {uri}")
                if "sirius" in uri.lower() or "x-sonosapi-" in uri.lower():
                    self.logger.info(f"📻 Detected SiriusXM stream — calling channelUpOrDown(down) for {dev.name}")
                    self.channelUpOrDown(dev, direction="down")
                    return
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Previous", "<InstanceID>0</InstanceID>")
                    self.logger.info(f"⏮️ Previous track for {dev.name}")
                    return

            elif action_id == "actionTogglePlay":
                state = dev.states.get("ZP_STATE", "STOPPED").upper()
                if state in ("STOPPED", "PAUSED_PLAYBACK"):
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    self.logger.info(f"▶️ Play for {dev.name}")
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "<Speed>1</Speed>")
                    self.logger.info(f"⏸ Pause for {dev.name}")
                return

            #####################################################################################################
            ### Start of action direct statements added code for action command support of favorites and volume
            #####################################################################################################

            elif action_id == "ZP_SonosFavorites":
                setting = pluginAction.props.get("setting")
                for uri in Sonos_Favorites:
                    if uri[4] == setting:
                        l2p=uri[0]
                        break
                mode = pluginAction.props.get("mode")
                if mode == "":
                    mode = "Play Now"
                    return
                if uri_radio in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p}), "ZP_RT_FavStation")
                    return
                elif uri_pandora in l2p:
                    setting = l2p[l2p.find(":")+1:l2p.find("?")]
                    self.actionDirect (PA(dev.id, {"setting":setting}), "ZP_Pandora")
                    return
                elif uri_siriusxm in l2p:
                    #setting = l2p[l2p.find("%3a")+3:l2p.find("?")]
                    setting = urllib.unquote(l2p[l2p.find(":")+1:l2p.find("?")])
                    self.actionDirect (PA(dev.id, {"setting":setting}), "ZP_SiriusXM")
                    return
                elif uri_spotify in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p, "mode":mode}), "ZP_Container")
                    return                
                elif uri_container in l2p or uri_jffs in l2p or uri_playlist in l2p or uri_file in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p, "mode":mode}), "ZP_Container")
                    return
                elif uri_sonos_radio in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p}), "ZP_SonosRadio")
                    return
                else:
                    indigo.server.log ("I do not know what to do with Favorite: %s" % l2p)
                    return

            elif action_id =="ZP_SonosRadio":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = coordinator_dev.pluginProps.get("address", "").strip()
                l2p = pluginAction.props.get("setting")
                for title in Sonos_Favorites:
                    if title[0] == l2p:
                        pTitle = self.cleanString(title[1]).encode('ascii', 'xmlcharrefreplace')
                        URI = title[3]
                        MD = title[2]
                        break
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+URI+"</CurrentURI><CurrentURIMetaData>"+MD+"</CurrentURIMetaData>")
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                indigo.server.log ("ZonePlayer: %s, Play Radio: %s" % (dev.name, pTitle))
                return

            elif action_id == "ZP_Container":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = coordinator_dev.pluginProps.get("address", "").strip()
                    dev_src_LocalUID = coordinator_dev.states['ZP_LocalUID']
                    #dev_src_LocalUID = CoordinatorDev.states['ZP_LocalUID']
                else:
                    dev_src_LocalUID = dev.states['ZP_LocalUID']                
                l2p = pluginAction.props.get("setting")
                mode = pluginAction.props.get("mode")
                #(uri_header, uri_detail) = l2p.split(':')
                for title in Sonos_Favorites:
                    if title[0] == l2p:
                        pTitle = self.cleanString(title[1]).encode('ascii', 'xmlcharrefreplace')
                        MD = title[2]
                        break

                # SONOS api change for Favorites?
                l2p = l2p.replace("&", "&amp;")

                if mode == "Play Now":
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                elif mode == "Play Next":
                    #current_track = self.parseCurrentTrack(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", ""))
                    current_track = dev.states['ZP_CurrentTrack']
                    indigo.server.log(current_track)
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>"+str(int(current_track)+1)+"</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                elif mode == "Add To Queue":
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                elif mode == "Replace Queue":
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "RemoveAllTracksFromQueue", "")
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                indigo.server.log ("ZonePlayer: %s, Play: %s" % (dev.name, pTitle))
                return

            ############################################################################################
            #### end of added code for action command support of favorites and volume
            ############################################################################################

            elif action_id == "addPlayersToZone":
                zones = []
                x = 1
                while x <= 12:
                    ivar = 'zp' + str(x)
                    if pluginAction.props.get(ivar) not in ["", None, "00000"]: 
                        zones.append(pluginAction.props.get(ivar))
                    x = x + 1

                for item in zones:
                    indigo.server.log("add zone to group: %s" % item)
                    dev_dest = indigo.devices[int(item)]
                    self.SOAPSend (dev_dest.pluginProps["address"], "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon:"+str(dev.states['ZP_LocalUID'])+"</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    self.refresh_all_group_states()

                self.refresh_all_group_states()
                self.logger.info(f"✅ tried refresh at end of add ???? ")
                return

            elif action_id == "setStandalone":
                indigo.server.log(f"🔀 Request to remove zone from group: {dev.name}")

                coordinator_dev = self.getCoordinatorDevice(dev)
                coordinator_ip = coordinator_dev.pluginProps.get("address", "").strip()
                coordinator_uid = coordinator_dev.states.get("ZP_LocalUID", "").strip()

                if not coordinator_ip or not coordinator_uid:
                    self.logger.error(f"❌ Cannot resolve IP or UID for coordinator device: {coordinator_dev.name}")
                    return

                try:
                    # Send ungrouping command
                    self.SOAPSend(
                        coordinator_ip,
                        "/MediaRenderer",
                        "/AVTransport",
                        "BecomeCoordinatorOfStandaloneGroup",
                        ""
                    )

                    time.sleep(1.0)  # Allow Sonos time to stabilize before reassigning queue

                    # Set playback queue on the appropriate device
                    target_uid = dev.states.get("ZP_LocalUID", "").strip()
                    if not target_uid:
                        self.logger.error(f"❌ Missing ZP_LocalUID for {dev.name}")
                        return

                    self.SOAPSend(
                        coordinator_ip,
                        "/MediaRenderer",
                        "/AVTransport",
                        "SetAVTransportURI",
                        f"<CurrentURI>x-rincon-queue:{target_uid}#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
                    )

                    self.refresh_all_group_states()
                    self.logger.info(f"✅ {dev.name} ungrouped and reassigned queue")

                except Exception as e:
                    self.logger.error(f"❌ Failed to set {dev.name} standalone: {e}")
                return

            elif action_id == "ZP_LIST":
                self.actionZP_LIST(pluginAction, dev)
                return

            # If it gets this far, action was not handled
            self.logger.warning(f"⚠️ Unknown or unsupported action: {action_id}")
            return

        except Exception as e:
            self.logger.error(f"❌ actionDirect exception: {e}")








    ############################################################################################
    ### Handleaction definitions
    ############################################################################################



    def handleAction_ZP_addPlayerToZone(self, pluginAction, dev, zoneIP):
        try:
            dev_dest = indigo.devices[int(pluginAction.props.get("setting"))]
            target_uid = str(dev.states.get('ZP_LocalUID', '')).strip()
            target_ip = dev_dest.pluginProps.get("address", "").strip()

            self.logger.warning(f"🔗 Requested: Add {dev.name} to group with {dev_dest.name}")
            self.logger.warning(f"🔍 UID={target_uid}, IP={target_ip}")

            if not target_uid or not target_ip:
                self.logger.error(f"❌ Missing required UID or IP for joining zone: UID={target_uid}, IP={target_ip}")
            else:
                self.logger.info(f"➕ Adding {dev.name} to group led by {dev_dest.name} @ {target_ip}")
                self.SOAPSend(
                    target_ip,
                    "/MediaRenderer",
                    "/AVTransport",
                    "SetAVTransportURI",
                    f"<CurrentURI>x-rincon:{target_uid}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
                )
            self.refresh_all_group_states()
        except Exception as e:
            self.logger.error(f"❌ actionZP_addPlayerToZone failed: {e}")





    def safe_debug(self, message):
        try:
            if self.logger.isEnabledFor(logging.DEBUG):
                try:
                    # Force the message to safe UTF-8
                    if isinstance(message, bytes):
                        message = message.decode("utf-8", errors="replace")
                    elif not isinstance(message, str):
                        message = str(message)

                    message = message.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

                    self.logger.debug(message)
                except Exception as inner_e:
                    try:
                        # Try logging something minimal if formatting fails
                        self.logger.warning(f"⚠️ Failed to log debug message safely: {inner_e}")
                    except Exception:
                        pass
        except Exception:
            pass  # Absolute last resort: don't let even logging crash



    def refresh_transport_state(self, zone_ip):
        """
        Refresh the transport state for a given zone IP by querying the current state
        and updating relevant Indigo device states (ZP_STATE, etc.).
        This helps reestablish correct state after volume or mute changes that cause Sonos to misreport sources.
        """
        try:
            speaker = self.getSoCoDeviceByIP(zone_ip)
            if not speaker:
                self.logger.warning(f"⚠️ Cannot refresh transport state — no SoCo device found for {zone_ip}")
                return

            state = speaker.get_current_transport_info().get("current_transport_state", "").upper()
            dev = next((d for d in indigo.devices.iter("self") if d.address == zone_ip), None)

            if dev:
                dev.updateStateOnServer("ZP_STATE", state)
                dev.updateStateOnServer("State", state)
                self.logger.debug(f"🔄 Refreshed transport state for {dev.name}: {state}")
            else:
                self.logger.warning(f"⚠️ No Indigo device matched to IP {zone_ip} during refresh")

        except Exception as e:
            self.logger.error(f"❌ refresh_transport_state failed for {zone_ip}: {e}")





    def handleAction_ZP_Pandora(self, pluginAction, dev, zoneIP, props):
        try:
            station_id = pluginAction.props.get("setting") or pluginAction.props.get("channelSelector")
            self.logger.debug(f"🧪 handleAction_ZP_Pandora() called — device: {dev.name} | zoneIP: {zoneIP}")
            self.logger.debug(f"🪪 Extracted Pandora station ID: {station_id}")

            if not station_id:
                self.logger.warning(f"⚠️ No Pandora station ID provided for device ID {dev.id}")
                return

            global Sonos_Pandora
            if not Sonos_Pandora:
                self.logger.warning("⚠️ Sonos_Pandora is empty — attempting fallback reload...")
                self.logger.warning(f"🔍 Pandora enabled: {self.Pandora} | Email: {self.PandoraEmailAddress} | Password: {'***' if self.PandoraPassword else '(empty)'}")
                if self.Pandora and self.PandoraEmailAddress and self.PandoraPassword:
                    Sonos_Pandora = []  # 🔄 Force clear to ensure overwrite
                    self.getPandora(self.PandoraEmailAddress, self.PandoraPassword, self.PandoraNickname)
                else:
                    self.logger.warning("⚠️ Pandora credentials incomplete — skipping reload.")

            self.safe_debug(f"🧾 Known Sonos_Pandora entries: {Sonos_Pandora}")
            self.safe_debug(f"🧾 Known Sonos_Pandora IDs: {[s[0] for s in Sonos_Pandora]}")

            # Retry lookup after fallback
            matching_station = next((s for s in Sonos_Pandora if s[0] == station_id), None)
            if not matching_station:
                self.logger.warning(f"⚠️ Unknown Pandora station ID: {station_id}")
                return

            station_name = matching_station[1]
            nickname = matching_station[3] or ""

            uri = f"x-sonosapi-radio:ST%3a{station_id}?sid=236&flags=8296&sn=1"
            metadata = f"""<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
                                       xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/"
                                       xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
                <item id="100c2068ST%3a{station_id}" parentID="10fe2064myStations" restricted="true">
                    <dc:title>{station_name}</dc:title>
                    <upnp:class>object.item.audioItem.audioBroadcast.#station</upnp:class>
                    <r:description>My Stations</r:description>
                    <desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">
                        SA_RINCON60423_X_#Svc60423-0-Token
                    </desc>
                </item>
            </DIDL-Lite>"""

            self.logger.info(f"📻 Sending {dev.name} to Pandora station: {station_name} ({station_id})")

            soco_dev = self.soco_by_ip.get(zoneIP)
            if not soco_dev:
                self.logger.warning(f"⚠️ soco_device is None for zoneIP {zoneIP}")
                return

            soco_dev.avTransport.SetAVTransportURI([
                ('InstanceID', 0),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', metadata),
            ])
            soco_dev.play()

        except Exception as e:
            self.logger.error(f"❌ handleAction_ZP_Pandora failed for device ID {dev.id}: {e}")







    def handleAction_SetSiriusXMChannel(self, pluginAction, dev, zoneIP):
        try:
            #self.safe_debug(f"🔍 This is the channelselector at handleAction_SetSiriusXMChannel: {channelSelector})")
            #self.safe_debug(f"🔍 This is the channelselector at handleAction_SetSiriusXMChannel: {channel})")
            channel_id = pluginAction.props.get("channelSelector", "")
            #self.safe_debug(f"🪪 handleAction_SetSiriusXMChannel() called for device {dev.name} at {zoneIP}")
            self.safe_debug(f"🔍 pluginAction.props: {pluginAction.props}")
            self.safe_debug(f"🔍 Extracted channel_id: '{channel_id}'")

            if not channel_id:
                self.logger.error("❌ No channel ID provided from control page (pluginAction.props[\"channelSelector\"] was empty)")
                return

            channel = self.siriusxm_id_map.get(channel_id)
            if not channel:
                self.logger.error(f"❌ Channel ID '{channel_id}' not found in siriusxm_id_map.")
                self.safe_debug(f"🧪 Current siriusxm_id_map keys: {list(self.siriusxm_id_map.keys())[:10]}... ({len(self.siriusxm_id_map)} total)")
                return

            cname = f"{channel.get('channelNumber')} - {channel.get('name')}"
            guid = channel.get("guid")

            self.logger.warning(f"📡 Sending SiriusXM channel: {cname} (GUID: {guid}) to zone: {zoneIP}")
            self.sendSiriusXMChannel(zoneIP, guid, cname)

        except Exception as e:
            self.logger.error(f"❌ handleAction_SetSiriusXMChannel() failed: {e}")


 

    def handleAction_ZP_SiriusXM(self, pluginAction, dev, zoneIP, props):
        try:
            guid = pluginAction.props.get("channelSelector")
            if not guid:
                self.logger.warning(f"⚠️ No SiriusXM GUID provided for device ID {dev.id}")
                return

            channel = self.siriusxm_guid_map.get(guid)
            if not channel:
                self.logger.warning(f"⚠️ Unknown channel GUID: {guid} — falling back to generic title")
                title = f"SiriusXM {guid}"
                album_art = None
            else:
                title = f"CH {channel.get('channel_number', '?')} - {channel.get('title', 'Unknown')}"
                album_art = channel.get("albumArtURI", None)

            uri, metadata = self.build_siriusxm_uri_and_metadata(guid, title, album_art)

            self.logger.info(f"📻 Sending {dev.name} to SiriusXM: {title} ({guid})")

            soco_dev = self.soco_by_ip.get(zoneIP)
            if not soco_dev:
                self.logger.warning(f"⚠️ soco_device is None for zoneIP {zoneIP}")
                return

            soco_dev.avTransport.SetAVTransportURI([
                ('InstanceID', 0),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', metadata),
            ])
            soco_dev.play()

            self.last_siriusxm_guid_by_dev[dev.id] = guid

        except Exception as e:
            self.logger.error(f"❌ handleAction_ZP_SiriusXM failed for device ID {dev.id}: {e}")


    def handleAction_TestHardcodedYachtRock(self, pluginAction, dev, zoneIP):
        self.sendSiriusXMChannel(zoneIP,
            "9150cc82-af5c-3be3-d170-0e81d87375a8",  # GUID
            "CH 15 - Yacht Rock Radio"
        )




    def handleAction_ZP_setStandalone(self, pluginAction, dev, zoneIP):
        try:
            self.logger.info(f"📤 Attempting to make {dev.name} standalone...")

            from soco import SoCo
            import time

            soco_dev = SoCo(zoneIP)

            # Log group composition
            group = soco_dev.group
            member_names = [m.player_name for m in group.members]
            self.logger.info(f"🧩 {dev.name} is grouped with: {member_names}")

            # If this device is the coordinator and has other members, break the group
            if soco_dev.is_coordinator and len(group.members) > 1:
                self.logger.info(f"🔁 {dev.name} is coordinator and has other members — breaking group.")
                try:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")
                    time.sleep(0.5)
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed BecomeCoordinatorOfStandaloneGroup SOAP call: {e}")
                self.logger.info(f"✅ ZonePlayer: {dev.name} is now standalone.")
                return  # ✅ Exit early to avoid SetAVTransportURI error

            # (Optional) Check URI to confirm if still grouped via x-rincon
            current_uri = dev.states.get("ZP_CurrentTrackURI", "")
            if current_uri.startswith("x-rincon:"):
                self.logger.info(f"ℹ️ {dev.name} still grouped via URI {current_uri}, skipping queue setup.")
                return

            self.logger.info(f"✅ ZonePlayer: {dev.name} is already standalone.")

        except Exception as e:
            self.logger.error(f"❌ Exception in handleAction_ZP_setStandalone: {e}")


    def handleAction_ChannelUp(self, pluginAction, dev, props):
        self.channelUpOrDown(dev, direction="up")

    def handleAction_ChannelDown(self, pluginAction, dev, props):
        self.channelUpOrDown(dev, direction="down")
 
    def handleAction_Q_Crossfade(self, pluginAction, dev):
        try:
            from soco import SoCo

            zone_ip = dev.address
            crossfade_enabled = pluginAction.props.get("setting", False)
            crossfade_bool = bool(crossfade_enabled in ["true", "True", True])

            self.logger.warning(f"🔁 Setting crossfade on {dev.name} ({zone_ip}) to {crossfade_bool}")

            speaker = SoCo(zone_ip)
            speaker.cross_fade = crossfade_bool

            self.logger.info(f"✅ Crossfade set to {crossfade_bool} on {dev.name}")

            # Optionally update Indigo state if you track it
            dev.updateStateOnServer("Q_Crossfade", "true" if crossfade_bool else "false")

        except Exception as e:
            self.logger.error(f"❌ Failed to set crossfade on {dev.name}: {e}")


    def handleAction_Q_Shuffle(self, pluginAction, dev, zoneIP):
        try:
            setting = pluginAction.props.get("setting", False)
            if isinstance(setting, str):
                setting = setting.lower() in ["true", "1", "yes"]

            play_mode = "SHUFFLE_NOREPEAT" if setting else "NORMAL"

            self.logger.warning(f"🔀 Setting shuffle on {dev.name} ({zoneIP}) to {play_mode}")

            current_uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
            self.safe_debug(f"🔍 Current URI for shuffle check: {current_uri}")

            if not self.isShuffleSupported(current_uri):
                self.logger.warning(f"⚠️ Skipping SetPlayMode on {dev.name} — unsupported stream type: {current_uri}")
                return

            try:
                self.SOAPSend(
                    zoneIP,
                    "/MediaRenderer",
                    "/AVTransport",
                    "SetPlayMode",
                    f"<InstanceID>0</InstanceID><NewPlayMode>{play_mode}</NewPlayMode>"
                )
                self.logger.info(f"✅ Shuffle set to {play_mode} on {dev.name}")
            except Exception as e:
                if "errorCode>712" in str(e):
                    self.logger.warning(f"⚠️ Shuffle not supported on current stream for {dev.name} (UPnP error 712)")
                else:
                    raise  # re-raise other errors

        except Exception as e:
            self.logger.error(f"❌ handleAction_Q_Shuffle failed for {dev.name}: {e}")



    def isShuffleSupported(self, uri):
        unsupported_prefixes = [
            "x-sonosapi-radio:",  # Pandora
            "x-sonosapi-hls:",    # SiriusXM
            "x-sonos-htastream:", # TV
            "x-rincon-mp3radio:"  # TuneIn or raw streams
        ]
        return not any(uri.startswith(pfx) for pfx in unsupported_prefixes)

    ### End of Handleaction definitions


    ############################################################################################
    ### General methods / functions  that can be called in the SonosPlugin Class
    ############################################################################################

    def actionQ_Shuffle(self, pluginAction, dev):
        try:
            setting = pluginAction.props.get("setting", False)
            if isinstance(setting, str):
                setting = setting.lower() == "true"

            zoneIP = dev.address
            self.logger.warning(f"🔀 Setting shuffle on {dev.name} ({zoneIP}) to {setting}")

            self.SOAPSend(
                zoneIP,
                "/MediaRenderer",
                "/AVTransport",
                "SetPlayMode",
                f"<NewPlayMode>{'SHUFFLE' if setting else 'NORMAL'}</NewPlayMode>"
            )

            dev.updateStateOnServer("Q_Shuffle", setting)
            self.logger.info(f"✅ Shuffle set to {setting} on {dev.name}")

        except Exception as e:
            self.logger.error(f"❌ Failed to set shuffle: {e}")



    def getZonePlayerByName(self, name):
        for zp in self.ZonePlayers:
            if zp.player_name == name:
                return zp
        self.logger.warning(f"⚠️ getZonePlayerByName(): No matching player found for name: {name}")
        return None



    def normalize_channel_dict(self, ch: XMChannel, streamUrl=None, albumArtURI=None, guidStreamValid=False):
        try:
            # Use only known-safe attributes
            chan_number_raw = getattr(ch, "channel_number", None) or ""
            chan_number_str = str(chan_number_raw).strip()

            try:
                chan_number_int = int(chan_number_str)
            except ValueError:
                self.logger.warning(f"🚫 Skipping malformed channel: {ch.name} — channel_number = '{chan_number_str}'")
                chan_number_int = None

            return {
                "id": ch.id,
                "guid": ch.guid,
                "channelNumber": chan_number_int,
                "channel_number": chan_number_int,  # for sorting
                "channel_number_str": chan_number_str,  # for diagnostics
                "name": ch.name,
                "shortDescription": ch.short_description,
                "longDescription": ch.long_description,
                "category": ch.category_name,
                "isFavorite": ch.is_favorite,
                "streamUrl": streamUrl,
                "albumArtURI": albumArtURI,
                "guidStreamValid": guidStreamValid,
                "fallbackStreamValid": bool(streamUrl),
                "channelType": getattr(ch, "channel_type", "audio"),
            }

        except Exception as e:
            self.logger.error(f"❌ normalize_channel_dict failed for channel {getattr(ch, 'name', 'UNKNOWN')}: {e}")
            return {}


    def load_siriusxm_channel_data(self):
        self.logger.info("🧪 ENTERED load_siriusxm_channel_data()")

        import os
        import json
        from sxm import SXMClient, RegionChoice, XMChannel

        def patched_from_dict(data):
            category_name = ""
            if "categories" in data and "categories" in data["categories"]:
                category_list = data["categories"]["categories"]
                if category_list and isinstance(category_list, list):
                    category_name = category_list[0].get("name", "")
            return XMChannel(
                id=data.get("id") or data.get("channelId", ""),
                name=data.get("name", ""),
                channel_number=data.get("channelNumber") or data.get("xmChannelNumber", ""),
                guid=data.get("guid") or data.get("channelGuid", ""),
                short_description=data.get("shortDescription", ""),
                long_description=data.get("longDescription", ""),
                category_name=category_name,
                is_favorite=data.get("isFavorite", False),
            )

        XMChannel.from_dict = staticmethod(patched_from_dict)

        cache_path = "/Library/Application Support/Perceptive Automation/Indigo 2024.2/Preferences/Plugins/siriusxm_channel_cache.json"
        self.logger.info("📂 Checking for SiriusXM channel cache...")

        sxm_username = self.pluginPrefs.get("SiriusXMID", "").strip()
        sxm_password = self.pluginPrefs.get("SiriusXMPassword", "").strip()

        if not sxm_username or not sxm_password:
            self.logger.warning("⚠️ SiriusXM credentials not provided in plugin preferences")
            return

        # Always initialize the client
        self.siriusxm = SXMClient(username=sxm_username, password=sxm_password, region=RegionChoice.US)

        # ✅ Load cache if present
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    self.siriusxm_channels = json.load(f)
                self.logger.info(f"📦 Loaded existing SiriusXM channel cache — {len(self.siriusxm_channels)} channels")

                # 🔍 Debug first few entries
                self.safe_debug("🧪 Dumping first 5 SiriusXM cache entries for inspection:")
                for i, ch in enumerate(self.siriusxm_channels[:5]):
                    self.safe_debug(f"  📦 [{i}] Type: {type(ch)} — Value: {repr(ch)}")

                # ✅ Validate all entries are dicts
                invalid_entries = [i for i, ch in enumerate(self.siriusxm_channels) if not isinstance(ch, dict)]
                if invalid_entries:
                    self.logger.error(f"🚨 SiriusXM cache is corrupted — invalid entries at indexes: {invalid_entries}")
                    self.siriusxm_channels = []
                    self.refreshSiriusXMChannelCache()
                    return

                self.logger.info("⏭️ Skipping live SiriusXM fetch — enriching cached data.")
                self.fetch_and_enrich_channels()
                self.logger.info("✅ EXITING load_siriusxm_channel_data() (cache mode)")
                return

            except Exception as e:
                self.logger.warning(f"⚠️ Cache exists but failed to load: {e}")
                self.logger.info("🔁 Proceeding with live fetch due to cache failure.")

        # ✅ Live fetch if no cache or failed
        try:
            if not self.siriusxm.authenticate():
                self.logger.error("❌ SiriusXM authentication failed.")
                return

            self.logger.info("✅ SiriusXM login successful — fetching channel list...")
            self.fetch_and_enrich_channels()

            # 💾 Save updated cache
            self.logger.info("💾 Saving SiriusXM channel cache...")
            try:
                with open(cache_path, "w") as f:
                    json.dump(self.siriusxm_channels, f, indent=2)
                self.logger.info(f"✅ Cache saved: {cache_path}")
            except Exception as e:
                self.logger.error(f"❌ Failed to save SiriusXM cache: {e}")

        except Exception as e:
            self.logger.error(f"💥 SiriusXM init error: {e}")

        self.logger.info("✅ EXITING load_siriusxm_channel_data() (live mode)")




    def query_siriusxm_channel(self, query):
        """
        Query channel by number (int/str), name (case-insensitive), or ID.
        Returns dict with channel info or None.
        """
        for ch in self.siriusxm_channels:
            if str(ch["channelNumber"]) == str(query):
                return ch
            if ch["name"].lower() == str(query).lower():
                return ch
            if ch["id"] == query:
                return ch
        return None



    def load_siriusxm_cache(self):
        cache_path = "/Library/Application Support/Perceptive Automation/Indigo 2024.2/Preferences/Plugins/siriusxm_channel_cache.json"

        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    self.siriusxm_channels = json.load(f)
                self.safe_debug(f"📦 Loaded SiriusXM channel cache from {cache_path} — {len(self.siriusxm_channels)} channels")
                return True
            except Exception as e:
                self.logger.error(f"❌ Failed to load SiriusXM channel cache: {e}")
                return False
        else:
            self.logger.info("📭 No SiriusXM channel cache found — will fetch live data.")
            return False



    def save_siriusxm_cache(self):
        cache_path = "/Library/Application Support/Perceptive Automation/Indigo 2024.2/Preferences/Plugins/sxm_channels_cache.json"
        try:
            with open(cache_path, "w") as f:
                json.dump(self.siriusxm_channels, f, indent=2)
            self.logger.info(f"💾 SiriusXM cache saved to {cache_path}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save SiriusXM cache: {e}")



    def load_siriusxm_cache(self):
        cache_path = "/Library/Application Support/Perceptive Automation/Indigo 2024.2/Preferences/Plugins/sxm_channels_cache.json"
        try:
            with open(cache_path, "r") as f:
                self.siriusxm_channels = json.load(f)
            self.logger.info(f"📂 Loaded SiriusXM channels from cache ({len(self.siriusxm_channels)} channels)")
            return True
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load SiriusXM cache: {e}")
            return False




    def refreshSiriusXMChannelCache(self):
        self.logger.info("🔄 Refreshing SiriusXM channel cache from API...")
        self.fetch_and_enrich_channels()
        self.save_siriusxm_cache()




    def enrich_channel_with_stream(self, channel):
        guid = channel.get("guid")
        if not guid:
            self.logger.warning("No GUID found for channel; cannot fetch stream.")
            return None

        metadata = self.get_chan_parms_by_guid(guid)
        if metadata and "stream" in metadata:
            channel["streamUrl"] = metadata["stream"]
            channel["albumArtURI"] = metadata.get("art", "")
            channel["guidStreamValid"] = True
            channel["channelType"] = "GUID"
            return channel
        else:
            channel["guidStreamValid"] = False
            return None


    ############################################################################################
    ### Nenu Specific Action Processing Methods
    ############################################################################################

    ### Nenu Specific Action - Test tuning hardcoded to the "Grateful Dead" station.

    def menutestSiriusXMChannelChange(self, valuesDict=None):
        try:
            test_device_id = 125081577  # Sonos CR device

            if test_device_id not in indigo.devices:
                self.logger.error(f"❌ Device ID {test_device_id} not found.")
                return

            dev = indigo.devices[test_device_id]
            zoneIP = dev.pluginProps.get("address", None)
            if not zoneIP:
                self.logger.error(f"❌ Device {dev.name} has no IP address.")
                return

            soco_dev = SoCoDevice(zoneIP)

            uri = "x-sonosapi-hls:channel-linear:067801cb-bb3f-1707-dd21-d77e06bb27c0?sid=37&flags=8232&sn=3"

            metadata = (
                '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" '
                'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" '
                'xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" '
                'xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">'
                '<item id="10092020" parentID="10092020" restricted="true">'
                '<dc:title>SiriusXM Channel Test</dc:title>'
                '<upnp:class>object.item.audioItem.audioBroadcast</upnp:class>'
                '<desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">'
                'SA_RINCON65031_</desc>'
                '</item>'
                '</DIDL-Lite>'
            )

            self.logger.info(f"🎯 Changing channel via GUID only...")
            self.safe_debug(f"🛰 URI: {uri}")
            self.safe_debug(f"📦 Metadata:\n{metadata}")

            soco_dev.avTransport.SetAVTransportURI([
                ('InstanceID', 0),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', metadata),
            ])
            soco_dev.play()

            self.logger.info(f"✅ Changed {dev.name} to SiriusXM test channel")

        except Exception as e:
            self.logger.error(f"❌ Channel change failed: {e}")


    ### End - Nenu Specific Action - Test tuning hardcoded to the "Grateful Dead" station.


    # ✅ Diagnostic method to verify parsed channel entries - Not real sure what this is doing ?????

    ### End - Nenu Specific Action - Diagnostic method to verify parsed channel entries

    ### Nenu Specific Action - Dump the channel cache to the log.
    def dump_siriusxm_channels_to_log(self):
        if not self.siriusxm_channels:
            self.logger.warning("📭 SiriusXM channel list is empty — nothing to dump.")
            return

        self.safe_debug(f"📦 Dumping new format {len(self.siriusxm_channels)} SiriusXM channels to log...")

        for i, ch in enumerate(self.siriusxm_channels):
            channel_number = ch.get("channelNumber", "—")
            name = ch.get("name", "—")
            cid = ch.get("id", "—")
            guid = ch.get("guid", "—")
            stream = ch.get("streamUrl", "—")
            art = ch.get("albumArtURI", "—")
            short = ch.get("shortDescription", "—")
            long_desc = ch.get("longDescription", "—")
            cat = ch.get("category", "—")
            guid_ok = ch.get("guidStreamValid", False)
            fallback_ok = ch.get("fallbackStreamValid", False)
            ch_type = ch.get("channelType", "—")
            is_fav = ch.get("isFavorite", False)

            self.logger.info(f"🔎 [{i:03}] #{channel_number:<4} | {name:<30} | ID: {cid:<10} | GUID: {guid}")
            self.logger.info(f"     ↳ Category: {cat} | Type: {ch_type} | Fav: {is_fav}")
            self.logger.info(f"     ↳ Short Desc: {short}")
            self.logger.info(f"     ↳ Stream: {stream}")
            self.logger.info(f"     ↳ Album Art: {art}")
            self.logger.info(f"     ↳ Stream OK: G={guid_ok} F={fallback_ok}")
            self.logger.info(f"     ↳ Long Desc: {long_desc}")

        self.logger.info("✅ Channel dump complete.")

    ### End - Nenu Specific Action - Dump the channel cache to the log.


    ### Nenu Specific Action - Delete and relaod the channel cache.
 
    def DeleteandDefine_SiriusXMCache(self):
        try:
            cache_path = "/Library/Application Support/Perceptive Automation/Indigo 2024.2/Preferences/Plugins/siriusxm_channel_cache.json"

            if os.path.exists(cache_path):
                os.remove(cache_path)
                self.logger.info("🗑 Deleted SiriusXM channel cache.")
            else:
                self.logger.info("🗃 SiriusXM channel cache not found — nothing to delete.")

            self.logger.info("🔄 Reloading SiriusXM channel data...")
            self.load_siriusxm_channel_data()
            self.logger.info("✅ Reloaded SiriusXM channel data.")

        except Exception as e:
            self.logger.error(f"❌ Error during SiriusXM cache reset: {e}")

    ### End - Nenu Specific Action - Delete and relaod the channel cache.

    ############################################################################################
    ### Nenu Specific Action Processing Methods
    ############################################################################################

    def get_chan_parms_3_way(self, chan):
        try:
            if not isinstance(chan, dict):
                self.logger.error(f"❌ get_chan_parms_3_way(): Expected dict, got {type(chan)} | Value: {chan}")
                return {
                    "id": None,
                    "guid": None,
                    "channelNumber": None,
                    "name": str(chan),
                    "streamUrl": None,
                    "albumArtURI": None,
                    "guidStreamValid": False,
                    "fallbackStreamValid": False,
                    "channelType": "unknown"
                }

            chan_id = str(chan.get("id", "")).strip()
            guid = str(chan.get("guid", "")).strip()
            number = str(chan.get("channelNumber", "")).strip()
            name = str(chan.get("name", "")).strip()

            self.safe_debug(f"🔍 get_chan_parms_3_way() → {name} | GUID={guid} | ID={chan_id}")

            # Ensure SiriusXM session is initialized
            if not self.siriusxm:
                self.logger.warning("🔑 Initializing SiriusXM session for stream lookup...")
                self.siriusxm = SXMClient(
                    self.pluginPrefs.get("SiriusXMID", ""),
                    self.pluginPrefs.get("SiriusXMPassword", ""),
                    region=RegionChoice.US
                )
                if not self.siriusxm.authenticate():
                    self.logger.error("❌ SiriusXM authentication failed")
                    return {
                        "id": chan_id,
                        "guid": guid,
                        "channelNumber": number,
                        "name": name,
                        "streamUrl": None,
                        "albumArtURI": None,
                        "guidStreamValid": False,
                        "fallbackStreamValid": False,
                        "channelType": chan.get("channelType", "unknown")
                    }

            # Primary: Try to get stream via GUID
            stream_url = self.siriusxm.get_playlist(guid)
            guid_valid = stream_url is not None

            # 🛡️ Sanity check: stream_url must be a proper URL
            if isinstance(stream_url, str):
                if "#EXTM3U" in stream_url or "AAC_Data/" in stream_url:
                    self.logger.warning(f"⚠️ Stream URL for '{name}' appears to be raw playlist data — skipping GUID stream")
                    stream_url = None
                    guid_valid = False
                elif len(stream_url) > 1000:
                    self.logger.warning(f"⚠️ Stream URL for '{name}' too long ({len(stream_url)} chars) — skipping GUID stream")
                    stream_url = None
                    guid_valid = False

            # Fallback: Use legacy field if GUID failed
            fallback_url = chan.get("streamUrl")
            fallback_valid = fallback_url is not None and not guid_valid
            resolved_url = stream_url or fallback_url

            # Album Art fallback: use existing or try to extract from images
            album_art = chan.get("albumArtURI")
            if not album_art and "images" in chan and isinstance(chan["images"], dict):
                images_list = chan["images"].get("images", [])
                if images_list and isinstance(images_list, list):
                    album_art = images_list[0].get("url", "")

            return {
                "id": chan_id,
                "guid": guid,
                "channelNumber": number,
                "name": name,
                "streamUrl": resolved_url,
                "albumArtURI": album_art,
                "guidStreamValid": guid_valid,
                "fallbackStreamValid": fallback_valid,
                "channelType": chan.get("channelType", "audio")
            }

        except Exception as e:
            self.logger.error(f"❌ get_chan_parms_3_way() error: {e}")
            return {
                "id": None,
                "guid": None,
                "channelNumber": None,
                "name": str(chan),
                "streamUrl": None,
                "albumArtURI": None,
                "guidStreamValid": False,
                "fallbackStreamValid": False,
                "channelType": "unknown"
            }



    def fetch_and_enrich_channels(self):
        from datetime import datetime
        from sxm import XMChannel

        start_time = datetime.now()
        self.logger.info(f"🦪 ENTERED fetch_and_enrich_channels() at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        self.Sonos_SiriusXM = []
        enriched_channels = []

        is_cache_mode = bool(self.siriusxm_channels)
        if is_cache_mode:
            self.logger.info(f"📱 Enriching {len(self.siriusxm_channels)} cached SiriusXM channels — skipping get_channels()")
            channels = [XMChannel.from_dict(ch) for ch in self.siriusxm_channels if isinstance(ch, dict)]
        else:
            self.siriusxm_channels = []
            try:
                raw_channels = self.siriusxm.get_channels() or []
                channels = [XMChannel.from_dict(ch) for ch in raw_channels if isinstance(ch, dict)]
                self.logger.info(f"📱 Retrieved {len(channels)} raw SiriusXM channels")
            except Exception as e:
                self.logger.error(f"💥 Failed to retrieve channels: {e}")
                return

        for idx, ch in enumerate(channels):
            streamUrl = None
            albumArtURI = None
            guidStreamValid = False

            chan_number_raw = ch.channel_number or ch.displayChannelNumber or ""
            chan_number_str = str(chan_number_raw).strip()

            try:
                chan_number_int = int(chan_number_str)
            except ValueError:
                self.logger.warning(f"❌ Skipping malformed channel at index {idx}: {ch.name} — channel_number = '{chan_number_str}'")
                continue

            chan = self.normalize_channel_dict(ch, streamUrl, albumArtURI, guidStreamValid)
            chan["channel_number"] = chan_number_int
            chan["channel_number_str"] = chan_number_str

            enriched_channels.append(chan)

            # ✅ Legacy-compatible format using GUID in [1]
            entry = [
                chan_number_int,                    # 0: Channel number
                chan.get("guid", ch.guid),          # 1: GUID used by Sonos stream URL
                chan.get("name", ch.name),          # 2: Display name
                chan.get("id", ch.id),              # 3: Optional ID (for reference)
                chan.get("name", ch.name)           # 4: Duplicate name (legacy compatibility)
            ]
            self.Sonos_SiriusXM.append(entry)

            if idx < 5:
                self.safe_debug(f"📦 Enriched Channel [{idx}]: {entry} (type: {type(entry)})")

        enriched_channels.sort(key=lambda c: c.get("channel_number", 9999))
        self.siriusxm_channels = enriched_channels

        self.logger.info("🔁 Building fast lookup maps for ID and GUID...")
        self.siriusxm_id_map = {c[3]: c for c in self.Sonos_SiriusXM if c[3]}   # from [3] = channel ID
        self.siriusxm_guid_map = {c[1]: c for c in self.Sonos_SiriusXM if c[1] and '-' in c[1]}  # from [1] = GUID

        # Debugging: Dump sample keys
        self.logger.debug(f"📝 Sample ID map keys: {list(self.siriusxm_id_map.keys())[:5]}")
        self.logger.debug(f"📝 Sample GUID map keys: {list(self.siriusxm_guid_map.keys())[:5]}")
        self.logger.debug(f"✅ Maps built: {len(self.siriusxm_id_map)} IDs, {len(self.siriusxm_guid_map)} GUIDs")

        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        self.logger.info(f"✅ EXITING fetch_and_enrich_channels() at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (elapsed: {elapsed:.1f} sec)")



    def getSiriusXM(self, channelInfo):
        """
        Returns full SiriusXM streaming parameters from a resolved channel dict.
        """
        if not channelInfo:
            return None

        chan_id = channelInfo.get("id")
        chan_num = channelInfo.get("channelNumber")
        name = channelInfo.get("name")
        stream_url = channelInfo.get("streamUrl")

        if not stream_url:
            self.logger.warning(f"❌ SiriusXM channel {name} (ID {chan_id}) has no stream URL.")
            return None

        return {
            "channelId": chan_id,
            "channelNumber": chan_num,
            "name": name,
            "streamUrl": stream_url
        }


    def func_switch(self, chanRef):
        """
        Looks up a SiriusXM channel by its ID and returns its metadata dict.
        """
        if not isinstance(chanRef, str):
            self.logger.error(f"❌ func_switch: Expected str channel ID, got {type(chanRef)} | Value: {chanRef}")
            return None

        chan_data = next((ch for ch in self.siriusxm_channels if ch.get("id") == chanRef), None)

        if not chan_data:
            self.logger.warning(f"🔁 func_switch: No match found for ID '{chanRef}'")
            return None

        return chan_data  # Already dict


    def getSiriusXMChannelList(self, filter="", valuesDict=None, typeId="", targetId=0):
        list_entries = []

        if not self.Sonos_SiriusXM:
            self.logger.warning("⚠️ SiriusXM channel list is empty. Cannot build UI list.")
            return []

        self.logger.warning(f"🧪 getSiriusXMChannelList CALLED with {len(self.Sonos_SiriusXM)} entries")

        for idx, entry in enumerate(self.Sonos_SiriusXM):
            try:
                channel_number = entry[0]
                channel_id = entry[1]
                channel_name = entry[2]

                if not channel_id or not channel_name:
                    self.logger.warning(f"⚠️ Skipping invalid channel entry at index {idx}: {entry}")
                    continue

                label = f"CH {channel_number} - {channel_name}"
                list_entries.append((channel_id, label))

                if idx < 5:
                    self.logger.warning(f"🧾 UI Entry [{idx}]: ID={channel_id} | Label={label}")

            except Exception as e:
                self.logger.error(f"❌ Error processing UI entry at index {idx}: {e} — Raw: {entry}")

        # Sort by channel number (first field)
        sorted_entries = sorted(list_entries, key=lambda x: int(x[1].split()[1]) if x[1].split()[1].isdigit() else 9999)
        self.logger.info(f"✅ Built {len(sorted_entries)} SiriusXM dropdown entries for Indigo UI")
        return sorted_entries
        

    def sendStreamToZone(self, zoneIP, stream_url, stream_title=""):
        try:
            zone = self.zone_by_ip.get(zoneIP)
            if not zone:
                self.logger.warning(f"Sonos: No zone found for IP {zoneIP}")
                return

            zone.play_uri(uri=stream_url, title=stream_title)
            self.logger.info(f"Sonos: Stream '{stream_title}' sent to zone {zoneIP}")

        except Exception as e:
            self.logger.error(f"Sonos: Failed to send stream to {zoneIP} - {e}")


    def actionZP_SiriusXM(self, pluginAction, dev):
        self.logger.debug("🪪 Entered plugin.py::actionZP_SiriusXM")

        props = pluginAction.props
        self.logger.debug(f"🧪 Raw pluginAction.props: {props}")

        channel_id = props.get("channelSelector") or props.get("channel", "").strip()
        self.safe_debug(f"🧪 Extracted channel ID: '{channel_id}'")

        # Lookup from legacy-format maps
        chan = self.siriusxm_guid_map.get(channel_id) or self.siriusxm_id_map.get(channel_id)

        if not chan:
            self.logger.warning(f"⚠️ SiriusXM: Channel ID '{channel_id}' not found in known maps.")
            return

        self.safe_debug(f"🔎 Channel structure: {chan} (type: {type(chan)})")

        # Legacy channel structure: [number, id, name, id, name]
        try:
            channel_guid = chan[1] if "-" in chan[1] else None  # Must be a GUID
            channel_name = chan[2]

            if not channel_guid:
                self.logger.warning(f"⚠️ Cannot send SiriusXM channel — GUID missing for ID '{channel_id}'")
                return

            zoneIP = dev.address
            self.logger.info(f"📡 Sending SiriusXM channel '{channel_name}' with GUID '{channel_guid}' to {zoneIP}")

            self.sendSiriusXMChannel(zoneIP, channel_guid, channel_name)

        except Exception as e:
            self.logger.error(f"❌ Exception during SiriusXM channel playback: {e}")


    def actionZP_LIST(self, pluginAction, dev):
        try:
            self.safe_debug(f"🧪 actionZP_LIST: pluginAction.props = {pluginAction.props}")

            # 🔍 Pull selected value from Indigo UI props
            val = pluginAction.props.get("ZP_LIST") or pluginAction.props.get("setting")

            # 🛠 Harden type of selected value
            if isinstance(val, str):
                raw_val = val.strip()
            elif isinstance(val, int):
                raw_val = str(val)
            else:
                self.logger.warning(f"[BAD PROP] ZP_LIST/setting is not string or int: {val} ({type(val).__name__})")
                return

            if not raw_val:
                self.logger.error(f"❌ actionZP_LIST: No playlist selected for {dev.name}")
                return

            # ✅ Now safe to use `raw_val` in logic (e.g., split or comparison)
            self.logger.info(f"▶️ ZP_LIST Action Triggered for {dev.name}: Selected = {raw_val}")
            # You can continue processing `raw_val` as needed here...

        except Exception as e:
            self.logger.error(f"❌ Exception in actionZP_LIST for {dev.name}: {e}")





            zoneIP = dev.pluginProps.get("address")
            if not zoneIP:
                self.logger.error(f"❌ actionZP_LIST: No IP address configured for {dev.name}")
                return

            # 🔍 Look up matching SoCo device
            soco_device = self.soco_by_ip.get(zoneIP)
            if not soco_device:
                self.logger.warning(f"⚠️ get_soco_device: IP {zoneIP} not found in soco_by_ip. Performing fallback discovery.")
                soco_device = self.get_soco_device(zoneIP)

            if not soco_device:
                self.logger.error(f"❌ actionZP_LIST: Could not locate SoCo device for IP {zoneIP}")
                return

            # 🔍 Retrieve Sonos playlist matching the selected title or ID
            playlists = soco_device.get_sonos_playlists()
            playlist_obj = None
            for pl in playlists:
                if raw_val in (pl.title, getattr(pl, "item_id", "")):
                    playlist_obj = pl
                    break

            if not playlist_obj:
                self.logger.error(f"❌ actionZP_LIST: Playlist object not found for '{raw_val}'")
                return

            self.logger.info(f"🎶 Queuing playlist '{playlist_obj.title}' on {dev.name}")

            # 🧼 Clear existing queue
            soco_device.clear_queue()

            # ➕ Add playlist to queue
            soco_device.add_to_queue(playlist_obj)

            # 🔁 Optionally enable repeat/shuffle
            soco_device.repeat = False
            soco_device.shuffle = False

            # ▶️ Start playback from beginning of queue
            soco_device.play_from_queue(0)

            self.logger.info(f"✅ Playlist '{playlist_obj.title}' started on {dev.name}")

        except Exception as e:
            self.logger.error(f"❌ actionZP_LIST: Failed to start playlist on {dev.name}: {e}")



    def get_model_name(self, soco_device):
        try:
            model_name = getattr(soco_device, "model_name", "").strip()
            if not model_name or model_name.lower() == "unknown":
                speaker_info = soco_device.get_speaker_info()
                model_name = speaker_info.get("model_name", "unknown")
            return model_name
        except Exception as e:
            self.logger.warning(f"⚠️ Could not retrieve model name: {e}")
            return "unknown"



    def reinitialize_and_rebuild_group_state(self):
        """
        Rebuild group state using logic similar to initial deviceStartComm load.
        This avoids plugin state drift after dynamic grouping/ungrouping.
        """
        self.logger.warning("🔄 Forcing reinitialization of group topology and plugin group states...")

        try:
            from soco import SoCo

            # ✅ Ensure all required plugin dictionaries are initialized
            if not hasattr(self, "zone_group_state_cache"):
                self.zone_group_state_cache = {}
            if not hasattr(self, "device_by_uuid"):
                self.device_by_uuid = {}
            if not hasattr(self, "uuid_to_soco"):
                self.uuid_to_soco = {}
            if not hasattr(self, "soco_devices"):
                self.soco_devices = {}
            if not hasattr(self, "parsed_zone_group_state_by_ip"):
                self.parsed_zone_group_state_by_ip = {}
            if not hasattr(self, "soco_by_ip"):
                self.soco_by_ip = {}
            if not hasattr(self, "ip_to_indigo_device"):
                self.ip_to_indigo_device = {}

            # 🔄 Clear all cached group state and mapping structures
            self.zone_group_state_cache.clear()
            self.device_by_uuid.clear()
            self.uuid_to_soco.clear()
            self.soco_devices.clear()
            self.parsed_zone_group_state_by_ip.clear()
            self.soco_by_ip.clear()
            self.ip_to_indigo_device.clear()

            # 🔁 Reinitialize SoCo and Indigo device bindings
            for dev in indigo.devices.iter("self"):
                ip = dev.address
                if not ip:
                    self.logger.warning(f"⚠️ Device {dev.name} has no IP — skipping")
                    continue

                try:
                    soco_device = SoCo(ip)
                    self.soco_by_ip[ip] = soco_device
                    self.ip_to_indigo_device[ip] = dev
                    self.logger.info(f"✅ Reinitialized SoCo for {dev.name} ({ip})")

                    # UID mapping
                    zp_uid = soco_device.uid
                    self.device_by_uuid[zp_uid] = dev
                    self.uuid_to_soco[zp_uid] = soco_device
                    self.soco_devices[zp_uid] = soco_device
                    self.logger.info(f"🔁 Bound {dev.name} to UUID {zp_uid}")

                except Exception as e:
                    self.logger.warning(f"❌ Failed to initialize SoCo for {dev.name} at {ip}: {e}")
                    continue

            # ⏬ Refresh zone group topology and populate group cache
            self.refresh_group_topology_after_plugin_zone_change()
            self.refresh_all_group_states()            
            self.evaluate_and_update_grouped_states()

            # 🔍 Confirm cache population
            if not self.zone_group_state_cache:
                self.logger.warning("🚫 zone_group_state_cache is still empty — group topology may not have been fetched.")
            else:
                self.logger.info(f"📊 zone_group_state_cache populated with {len(self.zone_group_state_cache)} group(s).")

            # ✅ Re-evaluate plugin logical grouped state




            self.logger.warning("✅ Reinitialization and group state rebuild complete.")

        except Exception as e:
            self.logger.error(f"❌ Failed to reinitialize group state: {e}")


    ############################################################################################
    ### Hellper methods for announce http server processing and checks
    ############################################################################################


    def getLocalIP(self):
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"


    def get_announce_http_config(self):
        """Read announcement HTTP config from prefs with safe fallbacks."""
        prefs = self.pluginPrefs or {}
        ip = (
            prefs.get("http_server") or
            prefs.get("httpServer") or
            prefs.get("httpServerIP") or
            prefs.get("http_ip") or
            ""  # empty means bind all interfaces on start; Sonos should use a reachable IP in URLs
        )

        # Port: default 8889
        try:
            port = int(prefs.get("http_port") or prefs.get("httpPort") or 8889)
        except Exception:
            port = 8889

        # Root path for announcement audio files
        root = prefs.get("SoundFilePath") or getattr(self, "SoundFilePath", "")
        if not root:
            root = indigo.server.getInstallFolderPath() + "/AudioFiles"

        return ip, port, root


    def ensure_announcement_http_server(self):
        if getattr(self, "_announce_httpd", None):
            self.logger.debug("📢 Announcement HTTP server already running")
            return True  # return True so startup can log it's running

        try:
            import http.server, socketserver, threading, os, http.client

            ip, port, root = self.get_announce_http_config()
            os.makedirs(root, exist_ok=True)

            class AnnouncementHandler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=root, **kwargs)
                def log_message(self, fmt, *args):
                    try:
                        self.server.parent_logger.debug("[ANN HTTP] " + fmt % args)
                    except Exception:
                        pass

            class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
                allow_reuse_address = True

            # Prefer the explicit IP from config; if "ALL" or empty, bind to all interfaces.
            bind_host = (ip or "").strip()
            if bind_host.upper() == "ALL":
                bind_host = ""  # INADDR_ANY

            # Create & start server
            self._announce_httpd = ThreadedTCPServer((bind_host, port), AnnouncementHandler)
            self._announce_httpd.parent_logger = self.logger

            t = threading.Thread(target=self._announce_httpd.serve_forever, daemon=True)
            t.start()
            self._announce_http_thread = t

            # Record what we actually bound (for diagnostics)
            try:
                bound_host, bound_port = self._announce_httpd.server_address  # ('0.0.0.0', 8889) or (ip, port)
            except Exception:
                bound_host, bound_port = (bind_host or "0.0.0.0", port)

            # Remember bound info
            self._announce_bound_host = bound_host
            self._announce_bound_port = bound_port
            self._announce_http_port = int(bound_port)

            # Determine a *publish* host for URIs (never loopback/0.0.0.0)
            def _is_bad(h: str) -> bool:
                return (not h) or h in ("0.0.0.0", "localhost", "::1") or str(h).startswith("127.")

            # Preference: explicit HTTPServer pref → selected interface IP → bound host if routable
            candidates = [
                (str(getattr(self, "HTTPServer", "")).strip() or None),
                (str(getattr(self, "selectedInterfaceIP", "")).strip() or None),
                (None if _is_bad(bound_host) else bound_host),
            ]
            publish_host = next((h for h in candidates if h and not _is_bad(h)), None)

            # Persist publish host for announcement URI builder
            self.announce_bind_ip = publish_host or ""

            # Log start
            self.logger.info(
                f"📢 Announcement HTTP server started on http://{bound_host or '0.0.0.0'}:{bound_port}/ serving {root}"
            )

            # Warn if we don’t yet have a safe publish host
            if not self.announce_bind_ip:
                self.logger.warning("⚠️ No safe LAN IP available to publish for announcements (loopback/0.0.0.0).")
            else:
                self.logger.info(f"✅ Announcement HTTP publish host: {self.announce_bind_ip}:{self._announce_http_port}")

                # Quick self-test (HEAD /) so we know Sonos can reach it by IP:PORT
                try:
                    conn = http.client.HTTPConnection(self.announce_bind_ip, self._announce_http_port, timeout=2.5)
                    conn.request("HEAD", "/")
                    resp = conn.getresponse()
                    self.logger.info(f"🧪 Announcement server self-test: {resp.status} {resp.reason}")
                    conn.close()
                except Exception as e:
                    self.logger.warning(
                        f"⚠️ Announcement server self-test failed on {self.announce_bind_ip}:{self._announce_http_port} → {e}"
                    )

            return True

        except OSError as e:
            self.logger.error(f"❌ Failed to start Announcement HTTP server (port in use?): {e}")
            return False
        except Exception as e:
            self.logger.exception(f"❌ Unexpected error starting Announcement HTTP server: {e}")
            return False











    ############################################################################################
    ### Dump Groups To Log by master coordinator
    ############################################################################################


    def dump_by_master(self):
        """
        Dumps the ZoneGroupState parsed group data as seen from the Sonos perspective (zone_group_state_cache).
        """
        if not hasattr(self, "zone_group_state_cache") or not self.zone_group_state_cache:
            self.logger.warning("🚫 No zone group data available to dump.")
            return

        self.logger.info("\n📦 Dumping Sonos / SOCO view of grouped devices to the log...")
        devices_in_parsed_groups = set()

        for group_id, group_data in self.zone_group_state_cache.items():
            if not isinstance(group_data, dict):
                self.logger.warning(f"⚠️ Skipping invalid group_data for '{group_id}' (expected dict, got {type(group_data)})")
                continue

            members = group_data.get("members", [])
            member_rows = []
            device_names_in_group = []

            for member in members:
                try:
                    if isinstance(member, dict):
                        name = member.get("name", "?")
                        ip = member.get("ip", "?")
                        bonded = member.get("bonded", False)
                        is_coordinator = member.get("coordinator", False)
                    elif isinstance(member, int):
                        dev = indigo.devices.get(member)
                        if dev:
                            name = dev.name
                            ip = dev.address if dev.address else "?"
                            bonded = "sub" in dev.name.lower()
                            is_coordinator = dev.states.get("GROUP_Coordinator", "false") == "true"
                        else:
                            self.logger.debug(f"⚠️ Could not resolve injected device ID {member}")
                            continue
                    else:
                        self.logger.warning(f"⚠️ Skipping invalid member in group '{group_id}': {member}")
                        continue

                    role = "Master (Coordinator)" if is_coordinator else "Slave"
                    cached_entry = self.ip_to_indigo_device.get(ip)
                    indigo_dev = indigo.devices.get(cached_entry) if isinstance(cached_entry, int) else cached_entry

                    indigo_name = indigo_dev.name if indigo_dev else "(unmapped)"
                    indigo_id = indigo_dev.id if indigo_dev else "-"
                    grouped_state = indigo_dev.states.get("Grouped", "?") if indigo_dev else "?"
                    plugin_grouped = "true" if grouped_state in (True, "true") else "false"

                    device_names_in_group.append(name)
                    if indigo_dev:
                        devices_in_parsed_groups.add(indigo_dev.id)

                    self.logger.debug(f"🔍 Adding member row: name={name}, ip={ip}, role={role}, indigo={indigo_name}, bonded={bonded}, grouped={grouped_state}, plugin_state={plugin_grouped}")

                    member_rows.append({
                        "Device Name": name,
                        "IP Address": ip,
                        "Role": role,
                        "Indigo Device": indigo_name,
                        "Indigo ID": indigo_id,
                        "Bonded": str(bonded),
                        "Grouped": str(grouped_state),
                        "Plugin State": plugin_grouped
                    })

                except Exception as e:
                    self.logger.warning(f"⚠️ Skipping invalid member in group '{group_id}': {e}")
                    continue

            col_widths = [30, 20, 25, 30, 10, 8, 8, 10]
            total_width = sum(col_widths) + len(col_widths) - 1

            self.logger.info("")
            self.logger.info(f"🧑‍💻 Devices in group (ZonePlayerUUIDsInGroup): {device_names_in_group}")
            self.logger.info("{:<30} {:<20} {:<25} {:<30} {:<10} {:<8} {:<8} {:<10}".format(
                "Device Name", "IP Address", "Role", "Indigo Device", "Indigo ID",
                "Bonded", "Grouped", "Plugin State"
            ))
            self.logger.info("=" * total_width)

            for row in member_rows:
                self.logger.info("{:<30} {:<20} {:<25} {:<30} {:<10} {:<8} {:<8} {:<10}".format(
                    row["Device Name"], row["IP Address"], row["Role"],
                    row["Indigo Device"], row["Indigo ID"], row["Bonded"],
                    row["Grouped"], row["Plugin State"]
                ))


    ############################################################################################
    ### Dump Groups To Log by logical group
    ############################################################################################


    def dump_by_logical_group(self):
        """
        Dumps the plugin-evaluated logical group state summary.
        """
        if not hasattr(self, "evaluated_group_members_by_coordinator") or not self.evaluated_group_members_by_coordinator:
            self.logger.warning("🚫 No plugin-evaluated group info available.")
            return

        self.logger.info("\n🔍 Evaluated Grouped Logic Summary (plugin-level view):")
        summary_col_widths = [32, 26, 8, 20, 20]
        summary_total_width = sum(summary_col_widths)
        header_fmt = "{:<32} {:<26} {:<8} {:<20} {:<20}"
        row_fmt = "{:<32} {:<26} {:<8} {:<20} {:<20}"

        self.logger.info("")
        self.logger.info(header_fmt.format(
            "Device Name", "Role", "Bonded", "Evaluated Grouped", "Group Name"
        ))
        self.logger.info("=" * summary_total_width)
        self.logger.info("")

        for coordinator_name, dev_list in sorted(self.evaluated_group_members_by_coordinator.items()):
            self.logger.info(f"🎧 Group: {coordinator_name}")
            self.logger.info("-" * summary_total_width)

            for indigo_dev in sorted(dev_list, key=lambda d: d.name.lower()):
                is_coord = indigo_dev.states.get("GROUP_Coordinator", "false") == "true"
                role = "Master (Coordinator)" if is_coord else "Slave"
                bonded = "sub" in indigo_dev.name.lower()
                grouped = indigo_dev.states.get("Grouped", "?")
                group_name = indigo_dev.states.get("GROUP_Name") or self.group_name_by_device_id.get(indigo_dev.id, "?")

                emoji_prefix = "🔹" if is_coord else "  "
                bonded_display = "🎯 True" if bonded else "False"
                grouped_display = (
                    "✅ true" if grouped in (True, "true") else
                    "❌ false" if grouped in (False, "false") else
                    f"❓ {grouped}"
                )

                self.logger.info(row_fmt.format(
                    emoji_prefix + indigo_dev.name.ljust(summary_col_widths[0] - 2),
                    role,
                    bonded_display,
                    grouped_display,
                    group_name
                ))

            self.logger.info("")


    ############################################################################################
    ### Dump Groups To Log by inventory
    ############################################################################################



    def dump_by_inventory(self):
        """
        Dumps a full audit of all Sonos Indigo devices including grouping, coordinator, bonded status,
        and plugin-evaluated group coordinator.
        """
        self.logger.info("\n📋 Full Indigo Device Audit Across All Indigo Registered Sonos Devices:")

        # Updated columns with Indigo ID and Group Coord
        audit_cols = [32, 15, 10, 12, 8, 14, 10, 10, 10, 32]
        audit_total_width = sum(audit_cols)
        audit_fmt = "{:<32} {:<15} {:<10} {:<12} {:<8} {:<14} {:<10} {:<10} {:<10} {:<32}"

        self.logger.info("")
        self.logger.info(audit_fmt.format(
            "Device Name", "IP Address", "Grouped", "Coordinator", "Bonded",
            "Group", "XML", "Evaluated", "Indigo ID", "Group Coord"
        ))
        self.logger.info("=" * audit_total_width)

        # Devices seen in XML-parsed group data
        devices_in_parsed_groups = set()
        if hasattr(self, "zone_group_state_cache"):
            for group in self.zone_group_state_cache.values():
                for member in group.get("members", []):
                    if isinstance(member, dict):
                        ip = member.get("ip")
                        dev = self.ip_to_indigo_device.get(ip)
                        if isinstance(dev, indigo.Device):
                            devices_in_parsed_groups.add(dev.id)
                        elif isinstance(dev, int):
                            devices_in_parsed_groups.add(dev)

        # Devices in plugin-evaluated groups
        devices_in_evaluated = set()
        coord_by_device_id = {}
        if hasattr(self, "evaluated_group_members_by_coordinator"):
            for devs in self.evaluated_group_members_by_coordinator.values():
                coordinator = None
                for dev in devs:
                    if dev.states.get("GROUP_Coordinator", "false") == "true":
                        coordinator = dev.name
                        break
                for dev in devs:
                    devices_in_evaluated.add(dev.id)
                    coord_by_device_id[dev.id] = coordinator or "(unknown)"

        # Iterate over all Indigo Sonos devices
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            name = dev.name
            ip = dev.address if hasattr(dev, "address") else dev.states.get("ip", "?")
            grouped = dev.states.get("Grouped", "?")

            # 🟢 Use live SoCo state to determine coordinator
            soco = self.ip_to_soco_device.get(ip)
            if soco:
                try:
                    coordinator = "True" if soco.is_coordinator else "False"
                except Exception as e:
                    self.logger.debug(f"Coordinator check failed for {dev.name} ({ip}): {e}")
                    coordinator = "?"
            else:
                self.logger.debug(f"No SoCo object found for {dev.name} ({ip})")
                coordinator = "?"

            group_name = dev.states.get("GROUP_Name", "?")
            bonded = "sub" in name.lower() or "surround" in name.lower() or "left" in name.lower() or "right" in name.lower()
            in_xml = "Yes" if dev.id in devices_in_parsed_groups else "No"
            in_eval = "Yes" if dev.id in devices_in_evaluated else "No"
            group_coord = coord_by_device_id.get(dev.id, "-")

            self.logger.info(audit_fmt.format(
                name, ip, str(grouped), coordinator,
                "Yes" if bonded else "No", group_name, in_xml, in_eval,
                str(dev.id), group_coord
            ))

        self.logger.info("")




 
    ############################################################################################
    ### Dump Groups To Log - All three
    ############################################################################################
    def dump_groups_to_log(self):
        """
        Wrapper method to dump full Sonos group state using all perspectives:
        1. dump_by_master()        — Sonos-derived ZoneGroupState from XML
        2. dump_by_logical_group() — Plugin-evaluated group logic
        3. dump_by_inventory()     — Full inventory audit of all Sonos Indigo devices
        """
        self.logger.info("🗂️ Starting full group state dump (Sonos + Plugin view)...")

        full_separator = "─" * 179

        self.logger.info("\n" + full_separator + "\n")
        self.dump_by_master()

        self.logger.info("\n" + full_separator + "\n")
        self.dump_by_logical_group()

        self.logger.info("\n" + full_separator + "\n")
        self.dump_by_inventory()
        self.logger.info("\n" + full_separator + "\n")

        self.logger.info("✅ Group state dump complete.")



    ############################################################################################
    ### End - Dump Groups To Log
    ############################################################################################



    def _compute_announce_publish_host(self):
        # Don’t publish loopback/any.
        def _ok(h):
            return h and h not in ("localhost", "0.0.0.0", "::1") and not str(h).startswith("127.")
        # Preference order: explicit pref → selected interface → bound host if routable
        candidates = [
            (getattr(self, "HTTPServer", "") or "").strip(),
            (getattr(self, "selectedInterfaceIP", "") or "").strip(),
            (getattr(self, "_announce_bound_host", "") or "").strip(),
        ]
        for h in candidates:
            if _ok(h):
                return h
        return ""






    def refresh_all_group_states(self):
        """
        Refresh and evaluate current Sonos zone groups using the SoCo .group property.
        """
        self.logger.warning("🔁 Entering Refresh_all_group_states")
        self.logger.warning("🔁 Forcing group topology refresh and evaluation using SoCo group objects...")

        groups = {}
        seen_members = set()

        for ip, soco in self.soco_by_ip.items():
            try:
                group = soco.group
                if not group or not group.coordinator:
                    continue

                group_id = group.coordinator.uid
                if group_id not in groups:
                    groups[group_id] = {
                        "coordinator": group.coordinator.uid,
                        "members": [],
                    }

                for member in group.members:
                    member_uuid = member.uid
                    if member_uuid in seen_members:
                        continue
                    seen_members.add(member_uuid)

                    zone_name = member.player_name.lower()
                    if "sub" in zone_name:
                        #self.logger.debug(f"🚫 Skipping bonded sub: {zone_name}")
                        continue

                    groups[group_id]["members"].append({
                        "uuid": member_uuid,
                        "location": member.ip_address,
                        "zone_name": zone_name,
                        "name": member.player_name,
                        "ip": member.ip_address,
                        "coordinator": member == group.coordinator,
                        "bonded": "sub" in zone_name  # refine if needed
                    })

            except Exception as e:
                self.logger.warning(f"⚠️ Failed to evaluate group for {ip}: {e}")

        self.zone_group_state_cache = groups
        self.logger.info(f"💾 zone_group_state_cache updated with {len(groups)} group(s)")
        self.refresh_group_topology_after_plugin_zone_change()
        self.logger.warning("🔁 Exiting Refresh_all_group_states")        
        #self.evaluate_and_update_grouped_states()








    def get_all_zone_groups(self):
        """Fetch and apply the latest zone group topology across all devices."""
        self.logger.warning("🔁 Initiating full group topology refresh...")

        updated = False
        for soco in self.soco_by_ip.values():
            try:
                #topology = soco.zoneGroupTopology
                topology = soco.zoneGroupTopology.to_xml_string()
                self.zone_group_state_cache = self.parse_zone_group_state(topology)
                self.logger.debug(f"📦 Zone group state updated from {soco.ip_address}")
                updated = True
                break  # Successfully fetched topology from one active player
            except Exception as e:
                self.logger.warning(f"⚠️ Could not fetch group topology from {soco.ip_address}: {e}")

        if not updated:
            self.logger.error("❌ Failed to update zone group state from any device")
            return

        # Re-evaluate all known Indigo devices
        self.logger.warning("🔍 Re-evaluating all Indigo Sonos devices with updated group state...")
        for dev in indigo.devices.iter("self"):
            try:
                self.refresh_group_topology_after_plugin_zone_change()
                #self.evaluate_and_update_grouped_states(dev)
            except Exception as e:
                self.logger.error(f"❌ Error re-evaluating group state for {dev.name}: {e}")

        # Optional debug dump
        if hasattr(self, "dump_groups_to_log"):
            self.dump_groups_to_log()







    def channelUpOrDown(self, dev, direction):
        import re

        self.logger.warning(f"⚠️ Determining next SiriusXM channel (using cached value)...")

        try:
            zoneIP = dev.pluginProps.get("address")
            if not zoneIP:
                self.logger.warning(f"⚠️ Device {dev.name} has no IP address configured.")
                return

            if not hasattr(self, "last_known_sxm_channel"):
                self.logger.warning(f"⚠️ No last known SiriusXM channel cache exists.")
                return

            current_channel_number = self.last_known_sxm_channel.get(zoneIP)
            if current_channel_number is None:
                self.logger.warning(f"⚠️ No cached SiriusXM channel for zone {zoneIP}. Cannot proceed.")
                return

            self.safe_debug(f"🔍 Cached current channel number: {current_channel_number}")

            # Clean, normalize, and validate channel list
            valid_channels = []
            for ch in self.siriusxm_channels:
                raw_ch_num = ch.get("channel_number")
                if raw_ch_num is None:
                    self.logger.warning(f"🚫 Skipping malformed channel (missing number): {ch.get('name')}")
                    continue
                try:
                    clean_ch_num = int(str(raw_ch_num).strip())
                    ch["channel_number"] = clean_ch_num  # Normalize in-place as int
                    valid_channels.append(ch)
                except Exception:
                    self.logger.warning(f"🚫 Skipping malformed channel: {ch.get('name')} — channel_number = {repr(raw_ch_num)}")
                    self.safe_debug(f"⤵️ Raw channel object: {ch}")

            if not valid_channels:
                self.logger.error("❌ No valid SiriusXM channels found for navigation.")
                return

            # Sort by channel_number
            sorted_channels = sorted(valid_channels, key=lambda c: c["channel_number"])

            # Log all valid channels
            self.safe_debug("📋 Dumping all known SiriusXM channels (sorted):")
            for ch in sorted_channels:
                self.safe_debug(f" - CH {ch['channel_number']} | {ch.get('name')} | GUID: {ch.get('guid')}")

            # Find current index
            current_index = next(
                (i for i, ch in enumerate(sorted_channels)
                 if ch["channel_number"] == current_channel_number),
                None
            )

            if current_index is None:
                self.logger.warning(f"⚠️ Channel number {current_channel_number} not found in sorted channel list.")
                return

            # Compute next or previous
            next_index = (current_index + 1) % len(sorted_channels) if direction == "up" else \
                         (current_index - 1 + len(sorted_channels)) % len(sorted_channels)

            next_channel = sorted_channels[next_index]
            next_guid = next_channel.get("guid")

            self.logger.info(
                f"🔀 Switching {direction} from CH {current_channel_number} to "
                f"CH {next_channel['channel_number']} - {next_channel.get('name')}"
            )

            # Send the next channel
            self.sendSiriusXMChannel(zoneIP, next_guid, next_channel.get("name"))

        except Exception as e:
            self.logger.error(f"❌ Failed to switch channel {direction} for {dev.name}: {e}")


        






    ############################################################################################
    ### SiriusXM Generic Channel Changer based on only needing a GUID
    ############################################################################################


    def SiriusXMChannelChanger(self, dev, guid):
        try:
            zoneIP = dev.pluginProps.get("address")
            if not zoneIP:
                self.logger.error(f"❌ No IP address found for device {dev.name}")
                return

            if not guid:
                self.logger.warning(f"⚠️ No SiriusXM GUID provided for device {dev.name}")
                return

            # 🔍 Lookup channel info by GUID
            channel = next((ch for ch in self.siriusxm_channels if ch.get("guid") == guid), None)
            if not channel:
                self.logger.warning(f"⚠️ No SiriusXM channel found for GUID: {guid}")
                return

            ch_number = channel.get("channel_number", "?")
            ch_name = channel.get("name", "Unknown")
            album_art = channel.get("albumArtURI", "")
            title = f"CH {ch_number} - {ch_name}"
            uri = f"x-sonosapi-hls:channel-linear:{guid}?sid=37&flags=8232&sn=3"

            metadata = (
                '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" '
                'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" '
                'xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" '
                'xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">'
                '<item id="10092020" parentID="10092020" restricted="true">'
                f'<dc:title>{title}</dc:title>'
                '<upnp:class>object.item.audioItem.audioBroadcast</upnp:class>'
                '<desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">'
                'SA_RINCON65031_</desc>'
                '</item>'
                '</DIDL-Lite>'
            )

            self.logger.info(f"📻 Switching {dev.name} to SiriusXM: {title}")
            self.safe_debug(f"🛰 URI: {uri}")
            self.safe_debug(f"📦 Metadata:\n{metadata}")

            # ✅ Use cached SoCo object
            soco_dev = self.soco_by_ip.get(zoneIP)
            if not soco_dev:
                from soco import SoCo
                soco_dev = SoCo(zoneIP)
                self.soco_by_ip[zoneIP] = soco_dev

            # 🎯 Attempt SetAVTransportURI with error handling
            try:
                soco_dev.avTransport.SetAVTransportURI([
                    ('InstanceID', 0),
                    ('CurrentURI', uri),
                    ('CurrentURIMetaData', metadata),
                ])
                time.sleep(0.5)
                soco_dev.play()

            except Exception as upnp_err:
                self.logger.error(f"❌ UPNP Error: {upnp_err}")
                self.logger.error(f"❌ Offending Command -> zoneIP: {zoneIP}, URI: {uri}")
                self.logger.error(f"📦 Metadata Sent:\n{metadata}")
                if "UPnPError" in str(upnp_err) and "402" in str(upnp_err):
                    self.logger.warning(f"⚠️ Sonos rejected the SiriusXM stream due to invalid arguments (UPnP 402). Check URI/metadata formatting.")
                return  # Skip further state updates on failure

            # ✅ Update states after success
            if "channel_number" in channel and "name" in channel:
                channel_number = channel["channel_number"]
                channel_name = channel["name"]
                dev.updateStateOnServer("ZP_STATION", f"CH {channel_number} - {channel_name}")
                self.safe_debug(f"📝 Updated ZP_STATION to CH {channel_number} - {channel_name}")

            self.logger.info(f"✅ Successfully changed {dev.name} to {title}")

            # 💾 Save last known SiriusXM channel
            if not hasattr(self, "last_known_sxm_channel"):
                self.last_known_sxm_channel = {}

            try:
                clean_ch_num = int(str(channel.get("channel_number", 0)).strip())
                self.last_known_sxm_channel[dev.id] = clean_ch_num
                self.logger.info(f"💾 Saved last known SiriusXM channel {clean_ch_num} for device {dev.name}")
            except Exception:
                self.logger.warning(f"⚠️ Could not parse and save channel_number for {dev.name}")

        except Exception as e:
            self.logger.error(f"❌ SiriusXMChannelChanger failed for {dev.name}: {e}")



            

    ############################################################################################


    def query_siriusxm_channel(self, channel_name_or_id):
        sxm_user = self.pluginPrefs.get("sirius_user", "")
        sxm_pass = self.pluginPrefs.get("sirius_pass", "")
        if not sxm_user or not sxm_pass:
            self.logger.error("SiriusXM credentials are not set in plugin preferences")
            return

        sxm = SiriusXM(username=sxm_user, password=sxm_pass, logger=self.logger)
        if not sxm.authenticate():
            self.logger.error("SiriusXM login failed")
            return

        result = sxm.get_channel(channel_name_or_id)
        if result:
            self.logger.info(f"🎵 Found SiriusXM channel: {result['name']} ({result['siriusChannelNumber']})")
        else:
            self.logger.warning(f"No matching SiriusXM channel found for: {channel_name_or_id}")


    def parse_siriusxm_guid_from_uri(self, uri):
        if not uri:
            return None

        try:
            # Decode percent-encoded parts
            decoded_uri = urllib.parse.unquote(uri)

            # Look for the pattern after 'channel-linear:'
            match = re.search(r'channel-linear:([a-f0-9\-]+)', decoded_uri, re.IGNORECASE)
            if match:
                return match.group(1)
        except Exception as e:
            self.logger.error(f"❌ Error parsing SiriusXM GUID from URI: {e}")

        return None

    def parse_siriusxm_guid_from_uri(self, uri):
        try:
            if "x-sonosapi-hls:channel-linear:" in uri:
                after_prefix = uri.split("x-sonosapi-hls:channel-linear:")[1]
                guid = after_prefix.split("?")[0]
                return guid.strip().lower()
        except Exception as e:
            self.logger.error(f"❌ Failed to parse GUID from URI: {uri} — {e}")
        return None


    def is_valid_guid(self, guid):
        import re
        return bool(re.fullmatch(
            r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
            guid, re.IGNORECASE
        ))



    def extract_siriusxm_guid(self, uri: str) -> str:
        try:
            self.safe_debug(f"🧪 extract_siriusxm_guid() input: {uri}")
            # Match both formats:
            # - x-sonosapi-hls:channel-linear:<guid>
            # - x-sonosapi-hls:<guid>
            match = re.search(
                r"x-sonosapi-hls:(?:channel-linear:)?([a-f0-9\-]{36})", uri, re.IGNORECASE
            )
            if match:
                guid = match.group(1)
                self.safe_debug(f"✅ Parsed SiriusXM GUID: {guid}")
                return guid

            self.logger.warning(f"⚠️ Could not parse SiriusXM GUID from URI: {uri}")
        except Exception as e:
            self.logger.error(f"❌ extract_siriusxm_guid() exception: {e}")
        return ""





    def sendSiriusXMChannel(self, zoneIP, channel_guid, channel_name):
        import urllib.parse

        try:
            self.logger.info("🔁 Entered sendSiriusXMChannel()")

            if not zoneIP:
                self.logger.error("❌ No zoneIP provided for sendSiriusXMChannel")
                return

            if not channel_guid:
                self.logger.warning(f"⚠️ No SiriusXM GUID provided for zone {zoneIP}")
                return

            if not channel_name:
                self.logger.warning(f"⚠️ No SiriusXM channel name provided for zone {zoneIP}")

            # Build HTML-safe encoded URI
            encoded_guid = urllib.parse.quote(channel_guid)
            uri = f"x-sonosapi-hls:channel-linear%3a{encoded_guid}?sid=37&amp;flags=8232&amp;sn=3"

            # HTML-safe metadata
            metadata = (
                '&lt;DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" '
                'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" '
                'xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" '
                'xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/"&gt;'
                f'&lt;item id="channel-linear:{channel_guid}" parentID="0" restricted="true"&gt;'
                f'&lt;dc:title&gt;{channel_name}&lt;/dc:title&gt;'
                '&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;'
                '&lt;desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/"&gt;'
                'SA_RINCON6_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;'
            )

            self.safe_debug(f"📡 Sending SiriusXM stream to {zoneIP}")
            self.safe_debug(f"🔗 CurrentURI: {uri}")
            self.safe_debug(f"🧾 CurrentURIMetaData:\n{metadata}")

            # Set the stream URI
            self.SOAPSend(
                zoneIP,
                "/MediaRenderer",
                "/AVTransport",
                "SetAVTransportURI",
                f"<CurrentURI>{uri}</CurrentURI><CurrentURIMetaData>{metadata}</CurrentURIMetaData>"
            )

            # Play the stream
            self.logger.debug("▶️ Play payload: <Speed>1</Speed>")
            self.SOAPSend(
                zoneIP,
                "/MediaRenderer",
                "/AVTransport",
                "Play",
                "<Speed>1</Speed>"
            )

            self.logger.info(f"🎶 Sent SiriusXM channel {channel_name} to {zoneIP}")

            # --- Save last known SiriusXM channel for the zoneIP ---
            if not hasattr(self, "last_known_sxm_channel"):
                self.last_known_sxm_channel = {}

            # 🔎 Find channel number if possible from self.siriusxm_channels
            matched_channel = next(
                (ch for ch in self.siriusxm_channels if ch.get("guid", "").lower().strip() == channel_guid.lower().strip()),
                None
            )

            if matched_channel:
                ch_num = matched_channel.get("channel_number")
                if ch_num:
                    try:
                        clean_ch_num = int(str(ch_num).strip())
                        # We'll track by IP address here, not dev.id (because we don't have dev in this function)
                        self.last_known_sxm_channel[zoneIP] = clean_ch_num
                        self.logger.info(f"💾 Saved last known SiriusXM channel {clean_ch_num} for zone {zoneIP}")
                    except Exception:
                        self.logger.warning(f"⚠️ Could not parse channel_number for {zoneIP}")

        except Exception as e:
            self.logger.error(f"❌ Failed to send SiriusXM channel {channel_name}: {e}")




    def actionChannelUp(self, pluginAction, dev):
        self.safe_debug(f"⚡ Action received: actionChannelUp for device ID {dev.id}")

        currentURI = dev.states.get("ZP_CurrentTrackURI", "")
        guid = self.parse_siriusxm_guid_from_uri(currentURI)

        if not guid:
            self.logger.warning(f"⚠️ Could not parse current SiriusXM content ID from URI: {currentURI}")
            return

        try:
            # Sort by numeric channelNumber
            guidList = sorted(
                self.siriusxm_guid_map.keys(),
                key=lambda g: int(self.siriusxm_guid_map[g].get("channelNumber", 9999))
            )

            currentIndex = guidList.index(guid)
            nextIndex = (currentIndex + 1) % len(guidList)
            nextGuid = guidList[nextIndex]
            nextChan = self.siriusxm_guid_map[nextGuid]
            channelNum = nextChan.get("channelNumber", "???")
            channelName = nextChan.get("title", "Unknown")

        except Exception as e:
            self.logger.warning(f"⚠️ ChannelUp lookup failed from {guid} — {e}")
            return

        self.logger.info(f"🔁 ChannelUp: {guid} → {nextGuid} ({channelNum}) - {channelName}")
        pluginAction.props["setting"] = nextGuid
        self.actionZP_SiriusXM(pluginAction, dev)
           

    def actionChannelDown(self, pluginAction, dev):
        self.safe_debug(f"⚡ Action received: actionChannelDown for device ID {dev.id}")

        currentURI = dev.states.get("ZP_CurrentTrackURI", "")
        guid = self.parse_siriusxm_guid_from_uri(currentURI)

        if not guid:
            self.logger.warning(f"⚠️ Could not parse current SiriusXM content ID from URI: {currentURI}")
            return

        try:
            # Sort by numeric channelNumber
            guidList = sorted(
                self.siriusxm_guid_map.keys(),
                key=lambda g: int(self.siriusxm_guid_map[g].get("channelNumber", 9999))
            )

            currentIndex = guidList.index(guid)
            prevIndex = (currentIndex - 1) % len(guidList)
            prevGuid = guidList[prevIndex]
            prevChan = self.siriusxm_guid_map[prevGuid]
            channelNum = prevChan.get("channelNumber", "???")
            channelName = prevChan.get("title", "Unknown")

        except Exception as e:
            self.logger.warning(f"⚠️ ChannelDown lookup failed from {guid} — {e}")
            return

        self.logger.info(f"🔁 ChannelDown: {guid} → {prevGuid} ({channelNum}) - {channelName}")
        pluginAction.props["setting"] = prevGuid
        self.actionZP_SiriusXM(pluginAction, dev)



    def get_current_uri_for_zone(self, zoneIP):
        try:
            soco_device = self.soco_by_ip.get(zoneIP)
            if soco_device is None:
                self.logger.warning(f"⚠️ soco_device is None for zoneIP {zoneIP}")
                return None

            transport_info = soco_device.avTransport.GetMediaInfo([('InstanceID', 0)])
            uri = transport_info.get('CurrentURI', None)

            if not uri:
                self.logger.warning(f"⚠️ get_current_uri_for_zone() say's - No URI available to parse for device at {zoneIP}")
            return uri

        except Exception as e:
            self.logger.error(f"❌ get_current_uri_for_zone() failed for zoneIP {zoneIP}: {e}")
            return None


    def get_next_siriusxm_guid(self, current_guid):
        if not self.sorted_siriusxm_guids:
            self.logger.warning("⚠️ SiriusXM GUID list is empty.")
            return None
        try:
            i = self.sorted_siriusxm_guids.index(current_guid)
            return self.sorted_siriusxm_guids[(i + 1) % len(self.sorted_siriusxm_guids)]
        except ValueError:
            self.logger.warning(f"⚠️ Current GUID {current_guid} not found. Returning first.")
            return self.sorted_siriusxm_guids[0]

    def get_prev_siriusxm_guid(self, current_guid):
        if not self.sorted_siriusxm_guids:
            self.logger.warning("⚠️ SiriusXM GUID list is empty.")
            return None
        try:
            i = self.sorted_siriusxm_guids.index(current_guid)
            return self.sorted_siriusxm_guids[(i - 1) % len(self.sorted_siriusxm_guids)]
        except ValueError:
            self.logger.warning(f"⚠️ Current GUID {current_guid} not found. Returning last.")
            return self.sorted_siriusxm_guids[-1]




###############################################################################################################################

    def exception_handler(self, exception_error_message, log_failing_statement):
        filename, line_number, method, statement = traceback.extract_tb(sys.exc_info()[2])[-1]
        module = filename.split('/')
        log_message = f"'{exception_error_message}' in module '{module[-1]}', method '{method} [{self.globals[PLUGIN_INFO][PLUGIN_VERSION]}]'"
        if log_failing_statement:
            log_message = log_message + f"\n   Failing statement [line {line_number}]: '{statement}'"
        else:
            log_message = log_message + f" at line {line_number}"
        self.logger.error(log_message)








############################################################################################
### Action annoucement processing
############################################################################################

    def actionAnnouncement(self, pluginAction, action):

        self.logger.info(f"[ANNOUNCE ENTRY] action={action!r} props_present={pluginAction.props is not None}")
        if pluginAction.props:
            self.logger.info(f"[ANNOUNCE PROPS] keys={sorted(pluginAction.props.keys())}")
            self.logger.info(f"[ANNOUNCE PROPS SAMPLE] ZonePlayer={pluginAction.props.get('ZonePlayer')!r} "
                             f"zp1={pluginAction.props.get('zp1')!r} "
                             f"source={pluginAction.props.get('source')!r} "
                             f"sound_file={pluginAction.props.get('sound_file')!r} "
                             f"level={pluginAction.props.get('level')!r}")

        # Comment out or early-return before doing anything
        # self.logger.warning("🔕 Skipping announcement test — isolating plugin failure.")
        # return

        indigo.server.log("did i hit 3 ????", type="Sonos PY Plugin Msg: 6778: ")
        global SavedState
        global actionBusy

        actionBusy = 1

        # ---- safer volume parse (preserves existing assignment semantics) ----
        try:
            _raw_vol = (pluginAction.props or {}).get("zp_volume")
            zp_volume = int(self.plugin.substitute(_raw_vol or "20"))
        except Exception:
            zp_volume = 20

        # Preserve existing group structure if Group Coordinator Only is selected in action
        try:
            gc_only = bool((pluginAction.props or {}).get("gc_only"))
        except Exception:
            gc_only = False

        # need this until group announcement actions are merged
        if action == "announcement":
            gc_only = False

        # --- build AnnouncementZones robustly (accepts bools or strings) ---
        AnnouncementZones = []

        def _is_true(v):
            s = str(v).strip().lower()
            return (v is True) or (s in ("true", "1", "yes", "on"))

        # helper: add zone if props value looks like a valid Indigo device id
        def _add_zone_if_valid(val):
            try:
                if val not in ("", None, "00000"):
                    dev_id = int(val)
                    _ = indigo.devices[dev_id]  # raises if invalid
                    AnnouncementZones.append(dev_id)
            except Exception as e:
                self.logger.error(f"❌ Invalid zone selection '{val}': {e}")

        # Special handling: for announcementMP3 we don't need to hunt for the group coordinator here.
        skip_gc_resolve = (action == "announcementMP3")

        if gc_only is False:
            # collect zp1..zp12
            try:
                for x in range(1, 13):
                    ivar = f"zp{x}"
                    _add_zone_if_valid((pluginAction.props or {}).get(ivar))
            except Exception as e:
                self.logger.error(f"❌ Failed building AnnouncementZones: {e}")
        else:
            # Resolve coordinator from zp1 or from bound device — unless we are skipping for announcementMP3
            dev = None

            # If skipping GC resolve (announcementMP3), just seed the list with zp1 or bound device and move on.
            if skip_gc_resolve:
                try:
                    anchor = (pluginAction.props or {}).get("zp1")
                    if anchor not in ("", None, "00000"):
                        dev = indigo.devices[int(anchor)]
                except Exception:
                    dev = None

                if dev is None:
                    try:
                        if action and hasattr(action, "deviceId") and action.deviceId:
                            dev = indigo.devices[action.deviceId]
                    except Exception:
                        dev = None

                if dev:
                    AnnouncementZones.append(dev.id)
                else:
                    self.logger.debug("[GC] announcementMP3: no zp1 or bound device to seed AnnouncementZones")
            else:
                # Original GC resolution path
                try:
                    anchor = (pluginAction.props or {}).get("zp1")
                    if anchor not in ("", None, "00000"):
                        dev = indigo.devices[int(anchor)]
                except Exception as e:
                    self.logger.error(f"❌ gc_only set but zp1 invalid: {e}")

                if dev is None:
                    # fall back to the device the action is bound to
                    try:
                        if action and hasattr(action, "deviceId") and action.deviceId:
                            dev = indigo.devices[action.deviceId]
                    except Exception:
                        pass

                if not dev:
                    self.logger.error("❌ gc_only is set but no valid zp1 or bound device was provided.")
                else:
                    if _is_true(dev.states.get("GROUP_Coordinator")):
                        AnnouncementZones.append(dev.id)
                    else:
                        # if selected ZonePlayer is not master of a group, find the master
                        coordinator_group = dev.states.get("GROUP_Name", "")
                        resolved = False
                        for idev in indigo.devices.iter("self.ZonePlayer"):
                            if _is_true(idev.states.get("GROUP_Coordinator")) and idev.states.get("GROUP_Name") == coordinator_group:
                                AnnouncementZones.append(idev.id)
                                resolved = True
                                break
                        if not resolved:
                            # Fallback: if we couldn’t resolve, at least target the chosen device so the action can run
                            # (demoted to debug to avoid noisy logs during announcements)
                            self.logger.debug(
                                f"[GC] Could not resolve group coordinator for '{dev.name}' "
                                f"(group '{coordinator_group}'). Using selected device."
                            )
                            AnnouncementZones.append(dev.id)

        self.logger.debug(f"🔎 gc_only={gc_only} | AnnouncementZones={AnnouncementZones}")



        # =========================================================================================
        # Announcement (FILE / LINE-IN) input normalization + target resolution
        # =========================================================================================
        if action == "announcement":
            try:
                props = pluginAction.props or {}

                # --- read panel fields (cover common variants) ---
                zone_sel = (
                    props.get("zp1")
                    or props.get("zoneplayer")
                    or props.get("ZonePlayer")
                    or props.get("deviceId")
                    or props.get("player")
                    or props.get("zone")
                )

                # Volume field on this dialog is "level" (fallbacks preserved)
                raw_vol = props.get("level", props.get("volume", props.get("zp_volume", 20)))
                try:
                    zp_volume = int(str(raw_vol).strip())
                except Exception:
                    self.logger.warning(f"[ANNOUNCE] Bad volume '{raw_vol}' ({type(raw_vol).__name__}); defaulting to 20")
                    zp_volume = 20

                # Source (e.g., "File" or "Line-In")
                source = props.get("source", "").strip() if isinstance(props.get("source"), str) else props.get("source")

                # Sound file name (for File source)
                file_name_prop = props.get("sound_file", props.get("file", ""))
                sound_file = file_name_prop.strip() if isinstance(file_name_prop, str) else ""

                # Line-In source device (device id string) when Source == "Line-In"
                zp_input = props.get("zp_input")

                # --- resolve target device from ZonePlayer selection (to get IP) ---
                dev_target = None
                if zone_sel not in (None, "", "00000"):
                    try:
                        dev_target = indigo.devices[int(zone_sel)]
                    except Exception:
                        # if it's not an id, try by name
                        try:
                            for d in indigo.devices.iter("self.ZonePlayer"):
                                if d.name == str(zone_sel) or d.states.get("ZP_ZoneName") == str(zone_sel):
                                    dev_target = d
                                    break
                        except Exception:
                            pass

                # Fallback: if nothing explicitly selected, use first computed AnnouncementZones entry
                if not dev_target and AnnouncementZones:
                    try:
                        dev_target = indigo.devices[int(AnnouncementZones[0])]
                    except Exception:
                        pass

                # Extract IP address from the resolved device
                zone_ip = ""
                if dev_target:
                    zone_ip = (dev_target.pluginProps.get("address") or dev_target.address or "").strip()

                # --- LOG exactly what we got/resolved ---
                self.logger.info(
                    f"[ANNOUNCE INPUT] props_keys={list(props.keys())} | "
                    f"ZoneSel={zone_sel!r} → Device={(dev_target.name if dev_target else None)!r} "
                    f"(ID={(dev_target.id if dev_target else None)!r}) IP={zone_ip!r} | "
                    f"Source={source!r} File={sound_file!r} Volume={zp_volume}"
                )

                # Guardrails: must have a target and IP
                if not dev_target or not zone_ip:
                    self.logger.error("❌ Could not resolve target ZonePlayer IP from action props. Aborting announcement.")
                    actionBusy = 0
                    return

                # ========================= NEW: snapshot only the target =========================
                try:
                    self.logger.info(f"[STATE SAVE] Snapshotting target before announcement: "
                                     f"id={dev_target.id}, ip={zone_ip}, name={dev_target.name}")
                    # Prefer filtered snapshot if your actionStates supports it:
                    self.actionStates(pluginAction, "saveStates", only_device_ids=[dev_target.id])
                except TypeError:
                    # Older signature without only_device_ids – fall back to full snapshot
                    self.logger.warning("[STATE SAVE] actionStates() has no 'only_device_ids' param; saving all devices.")
                    self.actionStates(pluginAction, "saveStates")
                except Exception as e:
                    self.logger.error(f"[STATE SAVE] Failed to snapshot target device state: {e}")
                # ======================= END NEW BLOCK (kept rest unchanged) ======================

                # -----------------------------------------------------------------------------
                # Existing FILE / LINE-IN execution logic – unchanged except for using zone_ip,
                # zp_volume, sound_file, and zp_input we normalized above.
                # -----------------------------------------------------------------------------

                # FILE-based announcement
                if str(source).lower() == "file":
                    # Validate file name early
                    if not sound_file:
                        self.logger.error("❌ Missing Sound File for File source. Aborting.")
                        actionBusy = 0
                        return

                    if not AnnouncementZones:
                        AnnouncementZones = [dev_target.id]

                    # Begin playback loop (your existing structure preserved)
                    for item in AnnouncementZones:
                        try:
                            dev = indigo.devices[int(item)]

                            # Only act on the resolved target IP
                            if dev.address and dev.address.strip() != zone_ip:
                                self.logger.debug(f"[SKIP] Device '{dev.name}' IP '{dev.address}' does not match target '{zone_ip}'")
                                continue

                            self.logger.info(f"[SEND] Sending FILE announcement '{sound_file}' to '{dev.name}' at {zone_ip}")

                            # Make standalone if required for URI change
                            if dev.states.get('GROUP_Coordinator') == "false":
                                self.logger.debug(f"[GROUP] '{dev.name}' is not coordinator — breaking from group...")
                                self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")

                            # Set volume
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                          f"<Channel>Master</Channel><DesiredVolume>{zp_volume}</DesiredVolume>")

                            # Unmute
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetMute",
                                          "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")

                            # TODO: Set AVTransportURI for your http_server + file path (your existing code)
                            # self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", ...)

                            # Play
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")

                        except Exception as e:
                            self.logger.error(f"[ERROR] Exception while sending FILE announcement to device {item}: {e}")

                # LINE-IN announcement
                elif str(source).lower() in ("line-in", "linein", "line_in"):
                    # Resolve source device (Line-In)
                    try:
                        dev_src = indigo.devices[int(zp_input)]
                        dev_src_LocalUID = dev_src.states['ZP_LocalUID']
                        self.logger.debug(f"[SOURCE] Line-In UID: {dev_src_LocalUID} ({dev_src.name})")
                    except Exception as e:
                        self.logger.error(f"❌ Invalid or missing zp_input for Line-In announcement: {e}")
                        actionBusy = 0
                        return

                    if dev_src.states.get('ZP_AIName', "") == "":
                        self.logger.warning("❌ No Line-In available on selected source device.")
                        actionBusy = 0
                        return

                    if not AnnouncementZones:
                        AnnouncementZones = [dev_target.id]

                    # Begin playback loop
                    for item in AnnouncementZones:
                        try:
                            dev = indigo.devices[int(item)]

                            # Only act on the resolved target IP
                            if dev.address and dev.address.strip() != zone_ip:
                                self.logger.debug(f"[SKIP] Device '{dev.name}' IP '{dev.address}' does not match target '{zone_ip}'")
                                continue

                            self.logger.info(f"[SEND] Sending Line-In announcement to '{dev.name}' at IP {zone_ip}")

                            # If member of group, make standalone (required for URI change)
                            if dev.states.get('GROUP_Coordinator') == "false":
                                self.logger.debug(f"[GROUP] '{dev.name}' is not coordinator — breaking from group...")
                                self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")

                            # Change to Line-In
                            self.plugin.debugLog(f"🔊 Playing LineIn: {dev_src.states.get('ZP_AIName', '[Unknown]')}")
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "SetAVTransportURI",
                                          f"<CurrentURI>x-rincon-stream:{dev_src_LocalUID}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")

                            # Set volume
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                          f"<Channel>Master</Channel><DesiredVolume>{zp_volume}</DesiredVolume>")

                            # Unmute
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetMute",
                                          "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")

                            # Play
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")

                        except Exception as e:
                            self.logger.error(f"[ERROR] Exception while sending Line-In announcement to device {item}: {e}")

                else:
                    # Unknown/unsupported source type
                    self.logger.error(f"❌ Unsupported announcement source: {source!r}")
                    actionBusy = 0
                    return

            except Exception as e:
                self.logger.error(f"[FATAL] Announcement handler crashed: {e}")
                actionBusy = 0
                return


        elif action == "announcementMP3":
            # ---- normalize props & log what the UI actually sent ----
            props = pluginAction.props or {}

            # Source (e.g., "TTS" or "File"); normalize gently
            source_raw = props.get("ttsORfile") or props.get("source")
            source = (source_raw.strip().lower() if isinstance(source_raw, str) else None)

            # Sound file (when using File source)
            sf_raw = props.get("sound_file") or props.get("file") or ""
            sound_file = sf_raw.strip() if isinstance(sf_raw, str) else ""

            # If source not provided but a file is present, assume "file"
            if not source and sound_file:
                source = "file"
            # Default to "file" if still unknown
            source = source or "file"

            # Volume (accept int or str; fall back to 20)
            raw_level = props.get("level", props.get("volume", props.get("zp_volume", 20)))
            try:
                zp_volume = int(str(raw_level).strip())
            except Exception:
                self.logger.warning(f"[WARN] Invalid volume {raw_level!r} — defaulting to 20")
                zp_volume = 20

            # Clamp volume to 0–100
            if zp_volume < 0 or zp_volume > 100:
                self.logger.warning(f"[WARN] Volume out of range ({zp_volume}); clamping to 0–100")
                zp_volume = max(0, min(100, zp_volume))

            # Log what we’ll use
            self.logger.info(
                f"[ANNOUNCE INPUT] source={source.upper()} file={sound_file!r} volume={zp_volume} "
                f"gc_only={gc_only} zp1={props.get('zp1')!r}"
            )

            # ===== build/prepare the announcement audio asset =====
            if source == "tts":
                announcement = self.plugin.substitute(props.get("setting"), validateOnly=False)
                zp_language = props.get("language")
                tts = gTTS(text=announcement, lang=zp_language)
                tts.save('announcement.mp3')
                s_announcement = "announcement.mp3"
                tts_delay = 0

            elif source == "ivona":
                announcement = self.plugin.substitute(props.get("IVONA_setting"), validateOnly=False)
                v = pyvona.pyvona.create_voice(self.IVONAaccessKey, self.IVONAsecretKey)
                v.codec = 'mp3'
                v.voice_name = IVONAVoices[int(props.get("IVONA_voice"))][1]
                v.sentence_break = int(props.get("IVONA_sentence_break"))
                v.speech_rate = props.get("IVONA_speech_rate")
                v.fetch_voice(announcement, 'announcement')
                s_announcement = "announcement.mp3"
                tts_delay = 0.5
                self.plugin.sleep(0.5)  # allow file creation

            elif source == "polly":
                announcement = self.plugin.substitute(props.get("POLLY_setting"), validateOnly=False)
                client = boto3.client('polly', aws_access_key_id=self.PollyaccessKey,
                                      aws_secret_access_key=self.PollysecretKey, region_name='us-east-1')
                response = client.synthesize_speech(OutputFormat='mp3', Text=announcement, VoiceId=props.get("POLLY_voice"))
                if "AudioStream" in response:
                    with closing(response["AudioStream"]) as stream:
                        data = stream.read()
                        with open("announcement.mp3", "wb") as f:
                            f.write(data)
                s_announcement = "announcement.mp3"
                tts_delay = 0.5

            elif source == "apple":
                announcement = self.plugin.substitute(props.get("APPLE_setting"), validateOnly=False)
                sp = NSSpeechSynthesizer.alloc().initWithVoice_(props.get("APPLE_voice"))
                ru = NSURL.fileURLWithPath_("./announcement.aiff")
                sp.startSpeakingString_toURL_(announcement, ru)
                s_announcement = "announcement.aiff"
                tts_delay = 0.5
                self.plugin.sleep(0.5)

            elif source == "microsoft":
                announcement = self.plugin.substitute(props.get("MICROSOFT_setting"), validateOnly=False)
                language = props.get("MICROSOFT_voice")
                statinfo = self.MicrosoftTranslate(announcement, language)
                s_announcement = "announcement.mp3"
                tts_delay = 0.5
                if statinfo is False:
                    self.plugin.errorLog("Microsoft Translate Error")
                    return

            else:
                # File source (default)
                fname = sound_file
                if not fname:
                    self.logger.error("❌ No sound file selected in 'sound_file'.")
                    return
                src = os.path.join(self.SoundFilePath or "", fname)
                if not os.path.isfile(src):
                    self.logger.error(f"❌ Sound file not found: {src}")
                    return
                try:
                    os.system(f'cp -pr "{src}" "announcement.mp3"')
                except Exception as e:
                    self.logger.error(f"❌ Failed to prepare announcement file: {e}")
                    return
                announcement = f"FILE [{fname}]"
                s_announcement = "announcement.mp3"
                tts_delay = 0

            indigo.server.log("Announcement: %s, Volume: %s" % (announcement, zp_volume))

            # ===== determine target device/IP from built AnnouncementZones =====
            if not AnnouncementZones:
                self.logger.error("❌ AnnouncementZones is empty — no zone selected for MP3 playback.")
                return

            try:
                GM = indigo.devices[int(AnnouncementZones[0])]
                zoneIP = GM.pluginProps.get("address", "").strip()
                if not zoneIP:
                    self.logger.error(f"❌ No IP address found in pluginProps for device {GM.name}.")
                    return
                self.logger.info(f"[ANNOUNCE TARGET] device={GM.name} id={GM.id} ip={zoneIP}")
            except Exception as e:
                self.logger.error(f"❌ Failed to resolve announcement zone device or IP: {e}")
                return

            # helper: coerce any value to an int, or None if not possible
            def _as_int(v):
                try:
                    return int(str(v).strip())
                except Exception:
                    return None

            # --- capture current playback state for quick restore (target device only) ---
            prev = {"uri": "", "meta": "", "pos": "00:00:00", "vol": None}
            try:
                self.logger.debug(f"[ANNOUNCE SAVE] snapshot begin for {GM.name} @ {zoneIP}")
                mi = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetMediaInfo", "")
                prev["meta"] = self.parseDirty(mi, "<CurrentURIMetaData>", "</CurrentURIMetaData>") or ""
                prev["uri"]  = self.parseDirty(mi, "<CurrentURI>", "</CurrentURI>") or ""
                pi = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", "")
                try:
                    prev["pos"] = self.parseRelTime(GM, pi) or "00:00:00"
                except Exception as e:
                    self.logger.debug(f"[ANNOUNCE SAVE] parseRelTime failed: {e}")
                    prev["pos"] = "00:00:00"
                try:
                    gv = self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "GetVolume",
                                       "<Channel>Master</Channel>")
                    prev["vol"] = _as_int(self.parseCurrentVolume(gv))
                except Exception as e:
                    self.logger.debug(f"[ANNOUNCE SAVE] GetVolume failed: {e}")
                    prev["vol"] = None
                self.logger.info(f"[ANNOUNCE SAVE] uri={prev['uri']!r} pos={prev['pos']} vol={prev['vol']} (type={type(prev['vol']).__name__})")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to snapshot current state prior to announcement: {e}")

            # --- capture volumes we will overwrite (per-device or group) ---
            prev["per_dev_vol"] = {}
            prev["group_vol"] = None
            prev["group_mute"] = None

            try:
                if gc_only is False:
                    # Per-device snapshot
                    snap_cnt = 0
                    for item in AnnouncementZones:
                        try:
                            _dev = indigo.devices[int(item)]
                            _ip = (_dev.pluginProps.get("address") or _dev.address or "").strip()
                            if not _ip:
                                self.logger.debug(f"[ANNOUNCE SAVE] skip {_dev.name}: no IP")
                                continue
                            gv = self.SOAPSend(_ip, "/MediaRenderer", "/RenderingControl", "GetVolume",
                                               "<Channel>Master</Channel>")
                            v_raw = self.parseCurrentVolume(gv)
                            v = _as_int(v_raw)
                            prev["per_dev_vol"][_dev.id] = v
                            snap_cnt += 1
                            self.logger.debug(f"[ANNOUNCE SAVE] captured {_dev.name} vol={v} (raw={v_raw!r})")
                        except Exception as e:
                            self.logger.debug(f"[ANNOUNCE SAVE] capture failed for device {item}: {e}")
                    self.logger.info(f"[ANNOUNCE SAVE] per-device volumes captured: {snap_cnt} → {prev['per_dev_vol']}")
                else:
                    # Group snapshot (coordinator only)
                    try:
                        gv = self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", "")
                        prev["group_vol"] = _as_int(self.parseCurrentVolume(gv))
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE SAVE] GetGroupVolume failed: {e}")
                        prev["group_vol"] = None
                    try:
                        gm = self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", "")
                        prev["group_mute"] = _as_int(self.parseCurrentMute(gm))
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE SAVE] GetGroupMute failed: {e}")
                        prev["group_mute"] = None
                    self.logger.info(f"[ANNOUNCE SAVE] group_vol={prev['group_vol']} (type={type(prev['group_vol']).__name__}) group_mute={prev['group_mute']}")
            except Exception as e:
                self.logger.debug(f"[ANNOUNCE SAVE] Volume snapshot failed (continuing): {e}")

            # ===== optional group-coordinator reads =====
            if gc_only is True:
                try:
                    gv_xml = self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", "")
                    group_volume = _as_int(self.parseCurrentVolume(gv_xml))
                    gm_xml = self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", "")
                    group_mute = _as_int(self.parseCurrentMute(gm_xml))
                    self.logger.debug(f"[ANNOUNCE INFO] gc_only=True live group_volume={group_volume} group_mute={group_mute}")
                except Exception as e:
                    self.logger.warning(f"[ANNOUNCE INFO] gc_only=True group snapshot failed (continuing): {e}")

            self.logger.debug("[ANNOUNCE STEP] snapshot complete; entering (re)group")

            # ===== (re)group if needed =====
            try:
                if gc_only is False:
                    # set standalone
                    self.plugin.debugLog("Announcement: set standalone")
                    for item in AnnouncementZones:
                        dev = indigo.devices[int(item)]
                        self.actionDirect(PA(dev.id), "setStandalone")

                    # add announcement zones to group (ensure 'setting' is a string)
                    self.plugin.debugLog("Announcement: add announcement zones to group")
                    itemcount = 0
                    for item in AnnouncementZones:
                        dev = indigo.devices[int(item)]
                        if itemcount > 0:
                            self.actionDirect(PA(GM.id, {'setting': str(dev.id)}), "addPlayerToZone")
                        itemcount += 1
                else:
                    # Nothing to split here; just ensure transport is stopped on GM
                    # (REPLACED actionDirect Stop with direct SOAP)
                    try:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                        self.logger.debug("[ANNOUNCE] Stop before announcement sent")
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE] Stop before announcement failed (continuing): {e}")
            except Exception:
                # Non-fatal: don’t abort the announcement if grouping hiccups
                self.logger.exception("❌ Announcement pre-playback grouping step failed (continuing)")

            self.logger.debug("[ANNOUNCE STEP] (re)group done; entering volume set")

            # ===== set volume (per device or group) =====
            self.plugin.debugLog("Announcement: set volume")
            if gc_only is False:
                # Per-device: set RenderingControl volume + unmute on each selected ZP
                for item in AnnouncementZones:
                    dev = indigo.devices[int(item)]
                    ip = (dev.pluginProps.get("address") or dev.address or "").strip()
                    if not ip:
                        self.logger.debug(f"[ANNOUNCE VOL] skip {dev.name}: no IP")
                        continue
                    self.logger.debug(f"[ANNOUNCE VOL] {dev.name} → {zp_volume}")
                    # Set volume
                    self.SOAPSend(ip, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                  f"<Channel>Master</Channel><DesiredVolume>{zp_volume}</DesiredVolume>")
                    # Unmute
                    self.SOAPSend(ip, "/MediaRenderer", "/RenderingControl", "SetMute",
                                  "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
            else:
                # Group: SetGroupVolume + SetGroupMute on the coordinator only
                # (REPLACED actionDirect GroupVolume/GroupMuteOff with direct SOAP)
                self.logger.debug(f"[ANNOUNCE VOL] GROUP → {zp_volume}")
                try:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume",
                                  f"<DesiredVolume>{zp_volume}</DesiredVolume>")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute",
                                  "<DesiredMute>0</DesiredMute>")
                except Exception as e:
                    self.logger.warning(f"[ANNOUNCE VOL] group volume/mute set failed (continuing): {e}")

            self.logger.debug("[ANNOUNCE STEP] volume set; entering audio probe")

            # ===== inspect the audio to time playback =====
            count = 0
            success = 0
            while count < 5 and success == 0:
                try:
                    if "mp3" in s_announcement:
                        audio = MP3("./" + s_announcement)
                    elif "aiff" in s_announcement:
                        audio = AIFF("./" + s_announcement)
                    success = 1
                except Exception as e:
                    self.logger.debug(f"[ANNOUNCE] audio probe failed (try {count+1}/5): {e}")
                    self.plugin.sleep(0.5)
                    count += 1

            if success == 1:
                indigo.server.log("Announcement Length: %s" % audio.info.length)

                # Ensure announcement URI components are valid
                try:
                    # 1) Ensure our lightweight 8889 server is up (no-ops if already started)
                    try:
                        self.ensure_announcement_http_server()
                    except Exception as _srv_e:
                        self.logger.error(f"❌ Announcement HTTP server not available: {_srv_e}")
                        return

                    # 2) Decide which host to publish to the Sonos player
                    def _usable_host(h: str) -> bool:
                        h = (h or "").strip()
                        if not h:
                            return False
                        lo = ("localhost", "127.0.0.1", "::1")
                        return h not in lo and not h.startswith("127.") and h != "0.0.0.0"

                    candidates = [
                        (self.HTTPServer or "").strip(),
                        (getattr(self, "announce_bind_ip", "") or "").strip(),
                        (getattr(self, "selectedInterfaceIP", "") or "").strip(),
                    ]
                    http_server = next((h for h in candidates if _usable_host(h)), "")
                    self.logger.debug(f"[ANNOUNCE URI] host candidates={candidates} -> chosen={http_server!r}")

                    if not http_server:
                        self.logger.error("❌ No usable HTTP server IP found (refusing to use loopback/0.0.0.0).")
                        return

                    # 3) Choose a port: prefs → actual server port → 8889
                    http_port = (str(self.HTTPStreamingPort).strip()
                                 if getattr(self, "HTTPStreamingPort", None) not in (None, "", 0)
                                 else str(getattr(self, "_announce_http_port", "") or ""))
                    if not http_port:
                        http_port = "8889"  # final fallback

                    # 4) Ensure we have a file name prepared by earlier code
                    announcement_file = s_announcement or ""
                    if not announcement_file:
                        self.logger.error("❌ Announcement file not prepared.")
                        return

                    # 5) Build and send
                    announcement_uri = f"http://{http_server}:{http_port}/{announcement_file}"
                    soap_payload = (
                        f"<CurrentURI>{announcement_uri}</CurrentURI>"
                        f"<CurrentURIMetaData></CurrentURIMetaData>"
                    )
                    self.logger.info(f"[ANNOUNCE URI] {announcement_uri}")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", soap_payload)

                except Exception as e:
                    self.logger.error(f"❌ Exception building announcement URI: {e}")
                    return

                # turn off queue repeat
                # (REPLACED actionDirect Q_Repeat with AVTransport SetPlayMode NORMAL)
                try:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>NORMAL</NewPlayMode>")
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not set play mode to NORMAL: {e}")

                self.plugin.sleep(1)

                # (REPLACED actionDirect Play with direct SOAP)
                self.logger.debug("[ANNOUNCE] Play announcement")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                self.plugin.sleep(tts_delay + audio.info.length)

                # --- restore previous playback (best-effort) ---
                try:
                    self.logger.info(f"[ANNOUNCE RESTORE] begin; gc_only={gc_only} "
                                     f"dev_vols={prev.get('per_dev_vol')} group_vol={prev.get('group_vol')} "
                                     f"uri={prev.get('uri')!r} pos={prev.get('pos')} vol={prev.get('vol')}")

                    if prev.get("uri") and "announcement." not in (prev.get("uri") or ""):
                        restore_payload = (f"<CurrentURI>{prev['uri']}</CurrentURI>"
                                           f"<CurrentURIMetaData>{prev['meta']}</CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", restore_payload)
                        self.plugin.sleep(0.3)  # settle

                        # Try to resume near the previous position if it looks valid (hh:mm:ss)
                        if prev.get("pos") and prev["pos"].count(":") == 2 and prev["pos"] != "00:00:00":
                            try:
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek",
                                              f"<Unit>REL_TIME</Unit><Target>{prev['pos']}</Target>")
                                self.logger.debug(f"[ANNOUNCE RESTORE] Seek to {prev['pos']}")
                            except Exception as e:
                                self.logger.debug(f"[ANNOUNCE RESTORE] Seek failed (continuing): {e}")

                        # ========== UNCONDITIONAL VOLUME RESTORE ==========
                        restore_vol = None
                        if gc_only:
                            gv = prev.get("group_vol")
                            pv = prev.get("vol")
                            restore_vol = gv if isinstance(gv, int) else (pv if isinstance(pv, int) else None)
                        else:
                            pv = prev.get("vol")
                            restore_vol = pv if isinstance(pv, int) else None

                        if not isinstance(restore_vol, int):
                            restore_vol = 20
                            self.logger.warning(f"[ANNOUNCE RESTORE] No saved volume found; falling back to {restore_vol}")

                        if restore_vol < 0 or restore_vol > 100:
                            self.logger.warning(f"[ANNOUNCE RESTORE] Saved volume out of range ({restore_vol}); clamping.")
                            restore_vol = max(0, min(100, restore_vol))

                        if gc_only:
                            self.logger.info(f"[ANNOUNCE RESTORE] Restoring GROUP volume → {restore_vol}")
                            try:
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume",
                                              f"<DesiredVolume>{restore_vol}</DesiredVolume>")
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute",
                                              "<DesiredMute>0</DesiredMute>")
                            except Exception as e:
                                self.logger.warning(f"[ANNOUNCE RESTORE] Group volume restore failed: {e}")
                        else:
                            self.logger.info(f"[ANNOUNCE RESTORE] Restoring device volume → {restore_vol}")
                            try:
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                              f"<Channel>Master</Channel><DesiredVolume>{restore_vol}</DesiredVolume>")
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                                              "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                            except Exception as e:
                                self.logger.warning(f"[ANNOUNCE RESTORE] Device volume restore failed: {e}")
                        # ========== /UNCONDITIONAL VOLUME RESTORE ==========

                        # Resume playback regardless
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        self.logger.info("[ANNOUNCE RESTORE] Previous stream resumed.")
                    else:
                        self.logger.info("[ANNOUNCE RESTORE] No prior URI captured; leaving device at announcement source.")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to restore previous playback after announcement: {e}")
            else:
                self.plugin.errorLog("Unable to read MP3 file.  Announcement aborted.")


                
    def MicrosoftTranslateAuth(self):
        authUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13/'
        scopeUrl = 'http://api.microsofttranslator.com'
        grantType = 'client_credentials'

        postdata = {'grant_type':grantType, 'scope':scopeUrl, 'client_id':self.MSTranslateClientID, 'client_secret':self.MSTranslateClientSecret}
        response = requests.post(authUrl, data=postdata)

        if response.status_code == 200:
            content = json.loads (response.content)
            return (content['access_token'])
        else:
            self.plugin.errorLog("[%s] Cannot authenticate to Microsoft Translate" % time.asctime())
            return (False)

    def MicrosoftTranslateLanguages(self):
        accessToken = self.MicrosoftTranslateAuth()
        if accessToken == False:
            return (False)

        scopeUrl = 'http://api.microsofttranslator.com'
        headers = {'Content-Type':'text/xml', 'Authorization':'Bearer ' + accessToken}
        url = scopeUrl + '/V2/Http.svc/GetLanguagesForSpeak'
        response = requests.get(url, headers=headers)

        langCodes = []
        Languages = ET.fromstring(response.content)
        for lang in Languages:
            langCodes.append(lang.text)
        languageCodes = str(langCodes).replace("'",'"')

        #self.myLocale = self.getLocale()
        #if self.myLocale == None:
        self.myLocale = 'en'

        url = scopeUrl + '/V2/Ajax.svc/GetLanguageNames?locale=' + self.myLocale + '&languageCodes=' + languageCodes
        response = requests.post(url, headers=headers)

        name_code = dict(zip(langCodes, eval(response.content)))
        indigo.server.log("Loaded Microsoft Translate Voices... [%s]" % len(name_code))

        return (name_code)

    def MicrosoftTranslate(self, announcement, language):
        authUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13/'
        scopeUrl = 'http://api.microsofttranslator.com'
        speakUrl = 'http://api.microsofttranslator.com/V2/Http.svc/Speak'
        grantType = 'client_credentials'

        accessToken = self.MicrosoftTranslateAuth()
        if accessToken == False:
            return (False)

        headers = {'Content-Type':'audio/mp3', 'Authorization':'Bearer ' + accessToken}
        url = speakUrl + '?text=' + announcement + '&language=' + language + '&format=audio/mp3&options=MaxQuality'

        with open ('announcement.mp3', 'wb') as handle:
            response = requests.get(url, headers=headers, stream=True)

            if response.ok:
                for block in response.iter_content(1024):
                    handle.write(block)
                return (True)
            else:
                return (False)

    def getReferencePlayerIP(self):
        return soco.discover().pop().ip_address





############################################################################################
### End - Action annoucement processing
############################################################################################



    ######################################################################################
    # Plugin Preferences
    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        try:
            if not userCancelled:
                self.safe_debug(f"[{time.asctime()}] Getting plugin preferences.")

                # ✅ Apply prefs FIRST before referencing them
                self.plugin.pluginPrefs.update(valuesDict)
                try:
                    self.plugin.debug = self.plugin.pluginPrefs["showDebugInLog"]
                except Exception as exception_error:
                    self.plugin.debug = False

                try:
                    self.plugin.xmlDebug = self.plugin.pluginPrefs["showXMLInLog"]
                except Exception as exception_error:
                    self.plugin.xmlDebug = False

                try:
                    self.plugin.eventsDebug = self.plugin.pluginPrefs["showEventsInLog"]
                except Exception as exception_error:
                    self.plugin.eventsDebug = False

                try:
                    self.plugin.stateUpdatesDebug = self.plugin.pluginPrefs["showStateUpdatesInLog"]
                except Exception as exception_error:
                    self.plugin.stateUpdatesDebug = False

                rootZPIP = self.plugin.pluginPrefs.get("rootZPIP", "auto")
                if self.rootZPIP != rootZPIP:
                    self.rootZPIP = rootZPIP
                    if self.rootZPIP == 'auto':
                        self.rootZPIP = self.getReferencePlayerIP()
                        self.logger.info(f"Using Reference ZonePlayer IP: {self.rootZPIP}")
                    if self.rootZPIP is not None:
                        self.getSonosFavorites()
                        self.getPlaylistsDirect()
                        self.getRT_FavStationsDirect()
                        # Retrieve Sonos Device ID for Music API
                        url = "http://" + self.rootZPIP + ":1400/status/zp"
                        response = requests.get(url)
                        if response.ok:
                            root = ET.fromstring(response.content)
                            self.SonosDeviceID = root.findtext('.//SerialNumber')
                        else:
                            self.logger.error(f"[{time.asctime()}] Cannot retrieve SerialNumber from Root ZonePlayer: {self.rootZPIP}")
                    else:
                        self.logger.error(f"[{time.asctime()}] Reference ZonePlayer IP address invalid.")

                try:
                    self.EventProcessor = self.plugin.pluginPrefs["EventProcessor"]
                except Exception as exception_error:
                    self.EventProcessor = "SoCo"

                try:
                    self.EventIP = self.plugin.pluginPrefs["EventIP"]
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Event Listener IP address.")

                try:
                    self.EventCheck = self.plugin.pluginPrefs["EventCheck"]
                except Exception as exception_error:
                    self.EventCheck = 60
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Event Check Interval; setting to 60 seconds.")

                try:
                    self.SubscriptionCheck = self.plugin.pluginPrefs["SubscriptionCheck"]
                except Exception as exception_error:
                    self.SubscriptionCheck = 15
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Subscription Check Interval; setting to 15 seconds.")

                try:
                    http_ip = self.plugin.pluginPrefs.get("HTTPStreamingIP")
                    http_port = self.plugin.pluginPrefs.get("HTTPStreamingPort")

                    if (self.HTTPStreamingIP != http_ip) or (self.HTTPStreamingPort != http_port):
                        self.HTTPStreamingIP = http_ip
                        self.HTTPStreamingPort = http_port
                    #if (self.HTTPStreamingIP != self.plugin.pluginPrefs["HTTPStreamingIP"]) or (self.HTTPStreamingPort != self.plugin.pluginPrefs["HTTPStreamingPort"]):
                    #    self.HTTPStreamingIP = self.plugin.pluginPrefs["HTTPStreamingIP"]
                    #    self.HTTPStreamingPort = self.plugin.pluginPrefs["HTTPStreamingPort"]

                        self.HTTPSTreamerOn = False
                        v = Thread(target=self.HTTPStreamer)
                        v.setDaemon(True)
                        v.start()
                except Exception as exception_error:
                    #self.logger.error(f"[{time.asctime()}] HTTPStreamer not functioning.")
                    import traceback
                    self.logger.error(f"[{time.asctime()}] HTTPStreamer not functioning: {exception_error}")
                    self.safe_debug(traceback.format_exc())


                try:
                    new_path = self.plugin.pluginPrefs.get("SoundFilePath", "").strip()
                    if not new_path:
                        new_path = indigo.server.getInstallFolderPath() + "/AudioFiles"

                    self.SoundFilePath = new_path
                    self.logger.info(f"🔁 Reloading sound files from: {self.SoundFilePath}")
                    self.getSoundFiles()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] ❌ Could not process SoundFilePath: {exception_error}")



                try:
                    if (self.Pandora != self.plugin.pluginPrefs['Pandora']) or \
                            (self.PandoraEmailAddress != self.plugin.pluginPrefs['PandoraEmailAddress']) or \
                            (self.PandoraPassword != self.plugin.pluginPrefs['PandoraPassword']) or \
                            (self.PandoraNickname != self.plugin.pluginPrefs['PandoraNickname']):
                        self.Pandora = self.plugin.pluginPrefs['Pandora']
                        self.PandoraEmailAddress = self.plugin.pluginPrefs['PandoraEmailAddress']
                        self.PandoraPassword = self.plugin.pluginPrefs['PandoraPassword']
                        self.PandoraNickname = self.plugin.pluginPrefs['PandoraNickname']
                        if self.Pandora:
                            self.getPandora(self.PandoraEmailAddress, self.PandoraPassword, self.PandoraNickname)
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Pandora credentials.")

                try:
                    if (self.Pandora2 != self.plugin.pluginPrefs['Pandora2']) or \
                            (self.PandoraEmailAddress2 != self.plugin.pluginPrefs['PandoraEmailAddress2']) or \
                            (self.PandoraPassword2 != self.plugin.pluginPrefs['PandoraPassword2']) or \
                            (self.PandoraNickname2 != self.plugin.pluginPrefs['PandoraNickname2']):
                        self.Pandora2 = self.plugin.pluginPrefs['Pandora2']
                        self.PandoraEmailAddress2 = self.plugin.pluginPrefs['PandoraEmailAddress2']
                        self.PandoraPassword2 = self.plugin.pluginPrefs['PandoraPassword2']
                        self.PandoraNickname2 = self.plugin.pluginPrefs['PandoraNickname2']
                        if self.Pandora2:
                            self.getPandora(self.PandoraEmailAddress2, self.PandoraPassword2, self.PandoraNickname2)
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve secondary Pandora credentials.")

                try:
                    if (self.SiriusXM != self.plugin.pluginPrefs['SiriusXM']) or \
                            (self.SiriusXMID != self.plugin.pluginPrefs['SiriusXMID']) or \
                            (self.SiriusXMPassword != self.plugin.pluginPrefs['SiriusXMPassword']):
                        self.SiriusXM = self.plugin.pluginPrefs['SiriusXM']
                        self.SiriusXMID = self.plugin.pluginPrefs['SiriusXMID']
                        self.SiriusXMPassword = self.plugin.pluginPrefs['SiriusXMPassword']
                        if self.SiriusXM:
                            self.getSiriusXM()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve SiriusXM parameters.")

                try:
                    if (self.IVONA != self.plugin.pluginPrefs['IVONA']) or \
                            (self.IVONAaccessKey != self.plugin.pluginPrefs['IVONAaccessKey']) or \
                            (self.IVONAsecretKey != self.plugin.pluginPrefs['IVONAsecretKey']):
                        self.IVONA = self.plugin.pluginPrefs['IVONA']
                        if self.IVONA:
                            self.IVONAaccessKey = self.plugin.pluginPrefs['IVONAaccessKey']
                            self.IVONAsecretKey = self.plugin.pluginPrefs['IVONAsecretKey']
                        if self.IVONA:
                            self.IVONAVoices()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve IVONA parameters.")

                try:
                    if (self.Polly != self.plugin.pluginPrefs['Polly']) or \
                            (self.PollyaccessKey != self.plugin.pluginPrefs['PollyaccessKey']) or \
                            (self.PollysecretKey != self.plugin.pluginPrefs['PollysecretKey']):
                        self.Polly = self.plugin.pluginPrefs['Polly']
                        if self.Polly:
                            self.PollyaccessKey = self.plugin.pluginPrefs['PollyaccessKey']
                            self.PollysecretKey = self.plugin.pluginPrefs['PollysecretKey']
                        if self.Polly:
                            self.PollyVoices()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Polly parameters.")

                try:
                    if (self.MSTranslate != self.plugin.pluginPrefs['MSTranslate']) or \
                            (self.MSTranslateClientID != self.plugin.pluginPrefs['MSTranslateClientID']) or \
                            (self.MSTranslateClientSecret != self.plugin.pluginPrefs['MSTranslateClientSecret']):
                        self.MSTranslate = self.plugin.pluginPrefs['MSTranslate']
                        if self.MSTranslate:
                            self.MSTranslateClientID = self.plugin.pluginPrefs['MSTranslateClientID']
                            self.MSTranslateClientSecret = self.plugin.pluginPrefs['MSTranslateClientSecret']
                        if self.MSTranslate:
                            self.MSTranslateVoices = self.MicrosoftTranslateLanguages()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve MSTranslate parameters.")

                self.logger.info(f"[{time.asctime()}] Processed plugin preferences.")
                return True

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement




###############################################################################################################################


    def getSonosFavorites(self):
        try:
            global Sonos_Favorites
            Sonos_Favorites = []
            res = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>FV:2</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"), 1)
            Favorites = ET.fromstring(res)
            for Favorite in Favorites.findall('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}item'):
                e_id = Favorite.attrib['id']
                e_res_clean = Favorite.findtext('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res')
                e_res = self.restoreString(e_res_clean, 0)
                e_title = self.restoreString(Favorite.findtext('.//{http://purl.org/dc/elements/1.1/}title'), 0)
                e_resMD = Favorite.findtext('.//{urn:schemas-rinconnetworks-com:metadata-1-0/}resMD')
                Sonos_Favorites.append((e_res, e_title, e_resMD, e_res_clean, e_id))
                self.safe_debug(f"\tSonos Favorites: {e_id}, {e_title}, {e_res}")
            self.logger.info(f"Loaded Sonos Favorites... [{len(Sonos_Favorites)}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


    ############################################################################################
    ### Define all of your action processing in this block
    ############################################################################################
        
    def actionTogglePlay(self, indigo_device):
        zoneIP = indigo_device.address
        transport_state = indigo_device.states.get("ZP_STATE", "STOPPED").upper()

        self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from Indigo): {transport_state}")

        # If ZP_STATE looks unreliable, fall back to querying SoCo directly
        if transport_state not in ("PLAYING", "PAUSED_PLAYBACK", "STOPPED"):
            soco_device = self.findDeviceByIP(zoneIP)
            if soco_device:
                try:
                    transport_info = soco_device.get_current_transport_info()
                    transport_state = transport_info.get("current_transport_state", "STOPPED").upper()
                    self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from SoCo): {transport_state}")
                except Exception as e:
                    self.logger.warning(f"⚠️ SoCo state fetch failed for {indigo_device.name}: {e}")
                    transport_state = "STOPPED"

        # Execute based on state
        if transport_state == "PLAYING":
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"⏸ Pause triggered for {indigo_device.name}")
        else:
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"▶️ Play triggered for {indigo_device.name}")

    def actionVolumeUp(self, indigo_device):
        try:
            discovered = soco.discover()
            soco_device = soco.SoCo(indigo_device.address)
            current_vol = soco_device.volume
            soco_device.volume = min(current_vol + 5, 100)
            self.logger.info(f"🔊 Volume UP for {indigo_device.name}: {current_vol} → {soco_device.volume}")
        except Exception as e:
            self.logger.error(f"❌ actionVolumeUp error for {indigo_device.name}: {e}")

    def actionVolumeDown(self, indigo_device):
        try:
            discovered = soco.discover()
            soco_device = soco.SoCo(indigo_device.address)
            current_vol = soco_device.volume
            soco_device.volume = max(current_vol - 5, 0)
            self.logger.info(f"🔉 Volume DOWN for {indigo_device.name}: {current_vol} → {soco_device.volume}")
        except Exception as e:
            self.logger.error(f"❌ actionVolumeDown error for {indigo_device.name}: {e}")


    def actionNext(self, indigo_device):
        try:
            zoneIP = indigo_device.address
            current_uri = indigo_device.states.get("ZP_CurrentTrackURI", "")

            if "x-sonosapi-hls:channel-linear" in current_uri:
                self.logger.info(f"📻 SiriusXM detected on {indigo_device.name} — calling ChannelUp directly")
                self.channelUpOrDown(indigo_device, direction="up")
            else:
                soco_device = soco.SoCo(zoneIP)
                soco_device.next()
                self.logger.info(f"⏭️ Skipped to NEXT track on {indigo_device.name}")
        except Exception as e:
            self.logger.error(f"❌ actionNext error for {indigo_device.name}: {e}")



    def actionPrevious(self, indigo_device):
        try:
            zoneIP = indigo_device.address
            current_uri = indigo_device.states.get("ZP_CurrentTrackURI", "")

            if "x-sonosapi-hls:channel-linear" in current_uri:
                self.logger.info(f"📻 SiriusXM detected on {indigo_device.name} — calling ChannelDown directly")
                self.channelUpOrDown(indigo_device, direction="down")
            else:
                soco_device = soco.SoCo(zoneIP)
                soco_device.previous()
                self.logger.info(f"⏮️ Went to PREVIOUS track on {indigo_device.name}")
        except Exception as e:
            self.logger.error(f"❌ actionPrevious error for {indigo_device.name}: {e}")

    def actionStates(self, pluginAction, action, only_device_ids=None):
        indigo.server.log("did i hit 2 ????", type="Sonos PY Plugin Msg: 6778: ")
        global SavedState

        if action == "saveStates":
            SavedState = []
            # normalize a set (or None for all)
            scope = set(only_device_ids) if only_device_ids else None

            for dev in indigo.devices.iter("self.ZonePlayer"):
                if dev.enabled and dev.pluginProps["model"] != SONOS_SUB:
                    if scope and dev.id not in scope:
                        continue  # 🔕 skip non-target devices during announcement

                    # --- these two calls were creating the UPNP noise ---
                    try:
                        ZP_CurrentURIMetaData = self.parseDirty(
                            self.SOAPSend(dev.pluginProps["address"],
                                          "/MediaRenderer", "/AVTransport",
                                          "GetMediaInfo", "", context="SAVE"),
                            "<CurrentURIMetaData>", "</CurrentURIMetaData>")
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed GetMediaInfo for {dev.name} ({dev.pluginProps['address']}): {e}")
                        ZP_CurrentURIMetaData = ""

                    try:
                        rel_time = self.parseRelTime(
                            dev,
                            self.SOAPSend(dev.pluginProps["address"],
                                          "/MediaRenderer", "/AVTransport",
                                          "GetPositionInfo", "", context="SAVE"))
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed GetPositionInfo for {dev.name} ({dev.pluginProps['address']}): {e}")
                        rel_time = "00:00:00"

                    SavedState.append((
                        dev.states['ZP_LocalUID'],
                        dev.states['Q_Crossfade'],
                        dev.states['Q_Repeat'],
                        dev.states['Q_Shuffle'],
                        dev.states['ZP_MUTE'],
                        dev.states['ZP_STATE'],
                        dev.states['ZP_VOLUME'],
                        dev.states['ZP_CurrentURI'],
                        ZP_CurrentURIMetaData,
                        dev.states['ZP_CurrentTrack'],
                        dev.states['GROUP_Coordinator'],
                        "",  # ZP (unused as before)
                        rel_time,
                        dev.states['ZonePlayerUUIDsInGroup']
                    ))

        elif action == "restoreStates":
            pass




    def actionStop(self, indigo_device):
        try:
            discovered = soco.discover()
            soco_device = soco.SoCo(indigo_device.address)
            soco_device.stop()
            self.logger.info(f"⏹️ STOPPED playback on {indigo_device.name}")
        except Exception as e:
            self.logger.error(f"❌ actionStop error for {indigo_device.name}: {e}")



    ############################### End of Action Processing Block ###############################



    def deviceStopComm(self, indigo_device):
        try:
            #self.safe_debug(f"🛑 deviceStopComm called for: {indigo_device.name} (ID: {indigo_device.id})")
            # Optional: Cleanup subscriptions or state
            if indigo_device.id in self.devices:
                del self.devices[indigo_device.id]
        except Exception as e:
            self.logger.error(f"❌ deviceStopComm error for {indigo_device.name}: {e}")



    import http.server
    import socketserver
    import threading
    import os

    def startup(self):
        self.logger.info("🔌 Sonos Plugin Starting Up...")

        # Default image path in case artwork is missing from the stream
        #DEFAULT_ARTWORK_PATH = '/Library/Application Support/Perceptive Automation/images/Sonos/default_artwork copy.jpg'

        # Ensure that the artwork folder exists for saving images
        ARTWORK_FOLDER = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        os.makedirs(ARTWORK_FOLDER, exist_ok=True)

        # check for sound file?
        self.SoundFilePath = self.pluginPrefs.get("SoundFilePath", "")
        self.logger.warning(f"🔧 Loaded SoundFilePath from prefs: {self.SoundFilePath}")

        if not self.SoundFilePath:
            self.SoundFilePath = indigo.server.getInstallFolderPath() + "/AudioFiles"
            self.logger.warning(f"⚠️ Falling back to default SoundFilePath: {self.SoundFilePath}")

        # Cleanup old art before starting the server to reduce storage size and keep things tidy
        self.cleanup_old_artwork()
        self.logger.debug(f"🖼️ Updated artwork 5")

        # Function to start the HTTP server and serve images
        def start_http_server():
            try:
                import http.server
                import socketserver
                import threading

                # Set the artwork folder to be served
                artwork_folder = "/Library/Application Support/Perceptive Automation/images/Sonos/"
                port = 8888

                # Handler class to serve files from the specified artwork folder
                class ArtworkHandler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=artwork_folder, **kwargs)

                # Pre-create a TCPServer that can reuse the socket
                class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
                    allow_reuse_address = True

                # Create and start the server
                httpd = ThreadedTCPServer(("", port), ArtworkHandler)
                server_thread = threading.Thread(target=httpd.serve_forever)
                server_thread.daemon = True
                server_thread.start()

                print(f"🚀 Mini HTTP server started on http://localhost:{port}/ serving {artwork_folder}")

            except Exception as e:
                print(f"DT - Failed to start mini HTTP server: {e}")

        # Start the HTTP server
        start_http_server()

        # start the announce http server - DT

        ip, port, root = self.get_announce_http_config()
        self.logger.info(f"📢 Announcement HTTP config → ip='{ip or 'ALL'}', port={port}, root='{root}'")

        # Ensure SoundFilePath points at the folder we intend to serve (keep your earlier choice if set)
        if not self.SoundFilePath:
            self.SoundFilePath = root
        try:
            os.makedirs(self.SoundFilePath, exist_ok=True)
        except Exception as e:
            self.logger.error(f"❌ Could not create SoundFilePath '{self.SoundFilePath}': {e}")

        # Persist the streaming port (from config; always an int)
        try:
            self.HTTPStreamingPort = int(port)
        except Exception:
            self.HTTPStreamingPort = 8889  # last-ditch default

        # --- Pick a publishable HTTP host (never loopback / 0.0.0.0) before server start ---
        def _usable_host(h: str) -> bool:
            if not h:
                return False
            h = h.strip()
            if h in ("localhost", "0.0.0.0", "::1"):
                return False
            if h.startswith("127."):
                return False
            return True

        try:
            # Candidate order:
            #  1) Existing self.HTTPServer (if safe)
            #  2) Interface on target Sonos subnet (if discoverable)
            #  3) selectedInterfaceIP from earlier discovery
            publish_host = (getattr(self, "HTTPServer", "") or "").strip()

            if not _usable_host(publish_host):
                best_on_subnet = None
                try:
                    # Reuse your subnet-aware scanner if present
                    best_on_subnet = self.find_sonos_interface_ip(getattr(self, "targetSonosSubnet", None))
                except Exception:
                    best_on_subnet = None

                if _usable_host(best_on_subnet):
                    publish_host = best_on_subnet
                else:
                    selected_ip = (str(getattr(self, "selectedInterfaceIP", "")).strip() or "")
                    if _usable_host(selected_ip):
                        publish_host = selected_ip
                    else:
                        publish_host = ""  # let ensure_announcement_http_server() bind to all; we'll re-evaluate after

            # Set (or clear) the attribute now; we may refine it after bind
            self.HTTPServer = publish_host

            if _usable_host(self.HTTPServer):
                self.logger.info(f"🌐 Using {self.HTTPServer} as HTTPServer for announcements")
            else:
                self.logger.warning("⚠️ No safe LAN IP available yet for announcements; will re-evaluate after server start.")
        except Exception as e:
            self.logger.warning(f"⚠️ Unable to normalize HTTPServer at startup: {e}")

        # Bring up the announcement server and log conclusively
        try:
            started = self.ensure_announcement_http_server()
        except Exception as e:
            started = False
            self.logger.error(f"❌ Announcement HTTP server failed to start: {e}")

        # If ensure_announcement_http_server doesn't return a boolean, infer from attribute
        if started is None:
            started = bool(getattr(self, "_announce_httpd", None))

        if started:
            # If we still don't have a safe publish host, try to use what the server actually bound (if usable)
            try:
                bound_host = (getattr(self, "announce_bind_ip", "") or "").strip()
                if not _usable_host(self.HTTPServer) and _usable_host(bound_host):
                    self.HTTPServer = bound_host
                    self.logger.info(f"🌐 Announcement publish host updated to {self.HTTPServer} after server start")
            except Exception:
                pass

            self.logger.info(
                f"✅ Announcement HTTP server is running on "
                f"{(self.HTTPServer if _usable_host(self.HTTPServer) else '0.0.0.0')}:{self.HTTPStreamingPort}"
            )
        else:
            self.logger.error("❌ Announcement HTTP server is NOT running (see errors above)")





        # 📥 Continue normal Sonos initialization
        try:
            self.sorted_siriusxm_guids = sorted(self.siriusxm_guid_map.keys())

            for device in soco.discover():
                self.soco_by_ip[device.ip_address] = device

            self.rootZPIP = self.plugin.pluginPrefs.get("rootZPIP", "auto")
            if self.rootZPIP == "auto":
                self.rootZPIP = self.getReferencePlayerIP()
                self.logger.info(f"✅ Using Reference ZonePlayer IP: {self.rootZPIP}")

            if self.rootZPIP:
                try:
                    self.getSonosFavorites()
                    self.getPlaylistsDirect()
                    self.getRT_FavStationsDirect()
                    self.safe_debug("📥 Sonos playlists, favorites, and radio stations loaded.")
                except Exception as e:
                    self.logger.error(f"❌ Failed loading playlists/favorites: {e}")
            else:
                self.logger.error("❌ rootZPIP is not set. Cannot fetch Sonos playlists.")

            self.logger.info("🕒 Deferring SiriusXM test playback for 'Office' until runConcurrentThread()")

            self.logger.info("🔧 Starting up Sonos Plugin...")
            self.build_ip_to_device_map()

            self.logger.debug("🔎 Performing post-startup audit of Sonos device group states...")

            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                self.initialize_custom_states(dev)

            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                # ✅ Ensure required states are initialized for each device
                if "Grouped" not in dev.states:
                    dev.updateStateOnServer("Grouped", False)
                if "GROUP_Name" not in dev.states:
                    dev.updateStateOnServer("GROUP_Name", "")
                if "GROUP_Coordinator" not in dev.states:
                    dev.updateStateOnServer("GROUP_Coordinator", "")

                group_coordinator = dev.states.get("GROUP_Coordinator", "n/a")
                #self.trace_me()
                group_name = dev.states.get("GROUP_Name", "n/a")
                Grouped = dev.states.get("GROUP_Grouped", "n/a")
#DT Try this for startup initial view?
                self.evaluate_and_update_grouped_states()
                self.logger.info(f"📊 Device '{dev.name}': Coordinator={group_coordinator}, Group='{group_name}', Grouped={Grouped}")


            self.getSoundFiles()

        except Exception as sonos_startup_error:
            self.logger.error(f"❌ Error during Sonos startup: {sonos_startup_error}")







    def shutdown(self):
        try:
            self.logger.info("SonosPlugin shutdown initiated.")

            # ✅ Gracefully stop mini HTTP server
            if hasattr(self, "httpd") and self.httpd:
                try:
                    self.logger.info("🛑 Shutting down mini HTTP server...")
                    try:
                        self.httpd.shutdown()
                    except Exception as shutdown_error:
                        self.logger.warning(f"⚠️ First shutdown() attempt failed: {shutdown_error} — retrying...")

                        # 🛠 Try forcing socket close manually if shutdown failed
                        if hasattr(self.httpd, "socket") and self.httpd.socket:
                            try:
                                self.httpd.socket.close()
                                self.logger.warning("🛠 Forced socket close after failed shutdown attempt.")
                            except Exception as socket_close_error:
                                self.logger.error(f"❌ Failed to close server socket manually: {socket_close_error}")

                    try:
                        self.httpd.server_close()
                    except Exception as server_close_error:
                        self.logger.warning(f"⚠️ server_close() failed: {server_close_error}")

                    self.logger.info("✅ Mini HTTP server shut down cleanly.")
                except Exception as httpd_error:
                    self.logger.error(f"❌ Error during mini HTTP server shutdown: {httpd_error}")
                finally:
                    self.httpd = None  # ✅ Explicitly clear

            if hasattr(self, "server_thread") and self.server_thread:
                try:
                    self.logger.info("🛑 Waiting for mini HTTP server thread to finish...")
                    self.server_thread.join(timeout=5.0)
                    if self.server_thread.is_alive():
                        self.logger.warning("⚠️ Server thread still alive after join timeout.")
                    else:
                        self.logger.info("✅ Mini HTTP server thread terminated.")
                except Exception as thread_error:
                    self.logger.error(f"❌ Error waiting for mini HTTP server thread: {thread_error}")
                finally:
                    self.server_thread = None  # ✅ Explicitly clear

            # ✅ Stop SoCo Event Listener
            try:
                from soco.events import event_listener
                is_running = getattr(event_listener, "is_running", None)
                if callable(is_running):
                    if is_running():
                        event_listener.stop()
                        self.logger.info("✅ SoCo Event Listener stopped.")
                elif isinstance(is_running, bool):
                    if is_running:
                        event_listener.stop()
                        self.logger.info("✅ SoCo Event Listener stopped.")
                else:
                    self.logger.warning("⚠️ SoCo Event Listener not running or invalid.")
            except Exception as event_listener_error:
                self.logger.error(f"❌ Error shutting down SoCo Event Listener: {event_listener_error}")


            # ✅ Stop announce http server - DT

            try:
                if getattr(self, "_announce_httpd", None):
                    self._announce_httpd.shutdown()
                    self._announce_httpd.server_close()
                    self._announce_httpd = None
                    self.logger.info("📢 Announcement HTTP server stopped")
            except Exception as e:
                self.logger.warning(f"Failed to stop announcement HTTP server: {e}")




        except Exception as e:
            self.logger.error(f"❌ shutdown error: {e}")






    def HTTPStreamer(self):
        try:
            HandlerClass = SimpleHTTPRequestHandler
            ServerClass = BaseHTTPServer.HTTPServer
            Protocol = "HTTP/1.0"

            if self.HTTPStreamingIP == "auto":
                try:
                    self.HTTPServer = socket.gethostbyname(socket.gethostname())
                except Exception as exception_error:
                    self.HTTPServer = None
                if self.HTTPServer is None:
                    d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    d.connect(("indigodomo.com", 80))
                    self.HTTPServer = d.getsockname()[0]
                    d.close()
            else:
                self.HTTPServer = self.HTTPStreamingIP

            server_address = ('0.0.0.0', int(self.HTTPStreamingPort))
            HandlerClass.protocol_version = Protocol
            self.httpd = ServerClass(server_address, HandlerClass)

            sa = self.httpd.socket.getsockname()
            self.logger.info(f"Serving HTTP Streamer on {self.HTTPServer} [{sa[0]}], port {sa[1]}")
            self.HTTPStreamerOn = True
            while self.HTTPStreamerOn:
                self.httpd.handle_request()

        # except Exception as e:
        #     self.logger.error(f"Cannot start HTTP Streamer on {self.HTTPServer}: {e}")
        except Exception as exception_error:
            self.exception_handler(f"Cannot start HTTP Streamer on {self.HTTPServer}: {exception_error}", True)  # Log error and display failing statement


    def _set_subscription_callback(self, sub, indigo_device, service_name):
        try:
            sub.callback = self.soco_event_handler
            self.soco_subs[indigo_device.id][service_name] = sub
            sid = getattr(sub, "sid", "no-sid")
            callback_name = getattr(sub.callback, "__name__", "no-callback")
            self.logger.info(f"🔔 Subscribed to {service_name} for {indigo_device.name} | SID: {sid}, Callback: {callback_name}")
        except Exception as e:
            self.logger.error(f"❌ Error in _set_subscription_callback for {indigo_device.name} [{service_name}]: {e}")


    def socoSubscribe(self, indigo_device, soco_device):
        from soco.events import event_listener

        self.safe_debug(f"🧪 socoSubscribe() ENTERED for {indigo_device.name} at {soco_device.ip_address}")

        # Confirm event listener status
        self.safe_debug(
            f"📡 SoCo Event Listener status: running={event_listener.is_running}, "
            f"address={getattr(event_listener, 'address', '?')}, "
            f"port={getattr(event_listener, 'port', '?')}"
        )

        # ✅ Use helper to get model name
        model_name = self.get_model_name(soco_device)
        self.logger.info(f"🧪 Model name for {indigo_device.name}: {model_name}")

        self.soco_subs[indigo_device.id] = {}
        self.soco_by_ip[indigo_device.address] = soco_device
        self.safe_debug(f"✅ soco_by_ip[{indigo_device.address}] stored with SoCo {soco_device.uid}")

        def _log_subscription_result(service_name, sub_obj):
            sid = getattr(sub_obj, "sid", None)
            if sid:
                self.logger.debug(f"🔒 {service_name} subscription confirmed for {indigo_device.name} | SID: {sid}")
            else:
                self.logger.error(f"❌ {service_name} subscription returned None SID for {indigo_device.name}")

        def _subscribe_with_retry(service_attr, service_name):
            try:
                # Determine suppression before subscribing
                is_coordinator = indigo_device.states.get("GROUP_Coordinator", False) in [True, "true", "True"]
                bonded_keywords = ["sub", "surround", "boost"]
                is_bonded = any(kw in model_name.lower() for kw in bonded_keywords)
                if not is_coordinator or is_bonded:
                    self.logger.debug(f"ℹ️ Skipping {service_name} subscription for {indigo_device.name} (bonded or non-coordinator)")
                    return

                self.logger.debug(f"🔔 Initiating subscription to {service_name} for {indigo_device.name}")
                sub_obj = getattr(soco_device, service_attr).subscribe(auto_renew=True, strict=True)
                _log_subscription_result(service_name, sub_obj)

                sid = getattr(sub_obj, "sid", None)
                if sid:
                    sub_obj.callback = self.soco_event_handler
                    self.soco_subs[indigo_device.id][service_name] = sub_obj
                    return

                # Retry once if SID is None
                self.logger.warning(f"🔁 Retrying {service_name} subscription for {indigo_device.name} after None SID...")
                sub_obj_retry = getattr(soco_device, service_attr).subscribe(auto_renew=True, strict=True)
                sid_retry = getattr(sub_obj_retry, "sid", None)
                if sid_retry:
                    self.logger.info(f"✅ {service_name} retry successful | SID: {sid_retry}")
                    sub_obj_retry.callback = self.soco_event_handler
                    self.soco_subs[indigo_device.id][service_name] = sub_obj_retry
                else:
                    self.logger.error(f"❌ Retry {service_name} still returned None SID for {indigo_device.name}")
            except Exception as e:
                self.logger.error(f"❌ Failed to subscribe to {service_name} for {indigo_device.name}: {e}")

        # AVTransport
        _subscribe_with_retry("avTransport", "AVTransport")

        # RenderingControl
        _subscribe_with_retry("renderingControl", "RenderingControl")

        # Optional AudioIn
        if model_name.lower().startswith("connect") or "port" in model_name.lower():
            try:
                self.logger.debug(f"🔔 Initiating subscription to AudioIn for {indigo_device.name}")
                ai_sub = soco_device.audioIn.subscribe(auto_renew=True, strict=True)
                _log_subscription_result("AudioIn", ai_sub)

                ai_sub.callback = self.soco_event_handler
                self.soco_subs[indigo_device.id]["AudioIn"] = ai_sub
                self.logger.info(f"✅ Subscribed to AudioIn | SID: {getattr(ai_sub, 'sid', 'N/A')}, Callback: {getattr(ai_sub.callback, '__name__', 'None')}")
            except Exception as e:
                self.logger.error(f"❌ Failed to subscribe to AudioIn: {e}")

        # ZoneGroupTopology
        try:
            self.logger.debug(f"🔔 Initiating subscription to ZoneGroupTopology for {indigo_device.name}")
            zgt_sub = soco_device.zoneGroupTopology.subscribe(auto_renew=True, strict=True)
            _log_subscription_result("ZoneGroupTopology", zgt_sub)

            zgt_sub.callback = self.soco_event_handler
            self.soco_subs[indigo_device.id]["ZoneGroupTopology"] = zgt_sub
            self.logger.info(f"✅ Subscribed to ZoneGroupTopology | SID: {getattr(zgt_sub, 'sid', 'N/A')}, Callback: {getattr(zgt_sub.callback, '__name__', 'None')}")
        except Exception as e:
            self.logger.warning(f"⚠️ ZoneGroupTopology subscription failed for {indigo_device.name}: {e}")

        # Final Listener Check
        self.logger.debug(
            f"🛰 Listener running={event_listener.is_running}, "
            f"bound to {getattr(event_listener, 'address', '?')}:{getattr(event_listener, 'port', '?')}"
        )








    ############################################################################################
    ### Start Device communications
    ############################################################################################

    def deviceStartComm(self, indigo_device):
        #self.logger.debug(f"🧪 deviceStartComm CALLED for {indigo_device.name}")

        try:
            self.logger.info(f"🔌 Starting communication with Indigo device {indigo_device.name} ({indigo_device.address})")
            self.devices[indigo_device.id] = indigo_device

            # Ensure lookup maps exist
            if not hasattr(self, "soco_by_ip"):
                self.soco_by_ip = {}
            if not hasattr(self, "ip_to_indigo_device"):
                self.ip_to_indigo_device = {}
            if not hasattr(self, "uuid_to_indigo_device"):
                self.uuid_to_indigo_device = {}

            # ✅ Ensure essential states exist before proceeding
            if "Grouped" not in indigo_device.states:
                indigo_device.updateStateOnServer("Grouped", False)
            if "GROUP_Name" not in indigo_device.states:
                indigo_device.updateStateOnServer("GROUP_Name", "")
            if "GROUP_Coordinator" not in indigo_device.states:
                indigo_device.updateStateOnServer("GROUP_Coordinator", "")

            # 🖼️ Preload ZP_ART with default placeholder if missing
            if not indigo_device.states.get("ZP_ART"):
                self.logger.debug(f"🖼️ Preloading ZP_ART with default placeholder for {indigo_device.name}")
                self.logger.debug(f"🖼️ Updated artwork 7")
                indigo_device.updateStateOnServer("ZP_ART", "/images/no_album_art.png")

            # Force plugin to use upgraded SoCo library
            import sys, os
            upgraded_path = os.path.join(os.path.dirname(__file__), "soco-upgraded")
            if upgraded_path not in sys.path:
                sys.path.insert(0, upgraded_path)

            import soco
            from soco import SoCo
            from soco.discovery import discover

            self.logger.debug(f"🧪 SoCo loaded from: {getattr(soco, '__file__', 'unknown')}")
            self.logger.debug(f"🧪 SoCo version: {getattr(soco, '__version__', 'unknown')}")

            soco_device = None

            # 🌐 First discovery attempt
            try:
                self.logger.info("🔍 Performing SoCo discovery to find matching device...")
                discovered = discover(timeout=5)
                if discovered:
                    for dev in discovered:
                        if dev.ip_address == indigo_device.address:
                            soco_device = dev
                            self.logger.info(f"✅ Found and initialized SoCo device for {indigo_device.name} at {dev.ip_address}")
                            break
                else:
                    self.logger.warning("❌ No Sonos devices discovered on the network.")
            except Exception as e:
                self.logger.error(f"❌ SoCo discovery failed: {e}")

            # 🔁 Retry discovery before fallback
            if not soco_device:
                self.logger.debug(f"🔁 Retrying SoCo discovery before fallback for {indigo_device.name}")
                try:
                    discovered_retry = discover(timeout=5)
                    if discovered_retry:
                        for dev in discovered_retry:
                            if dev.ip_address == indigo_device.address:
                                soco_device = dev
                                self.logger.warning(f"✅ Found device on retry for {indigo_device.name} at {dev.ip_address}")
                                break
                except Exception as e:
                    self.logger.error(f"❌ Retry discovery failed: {e}")

            # 🧯 Fallback if discovery still failed
            if not soco_device:
                self.logger.debug(f"⚠️ Discovery failed — falling back to direct SoCo init for {indigo_device.name}")
                try:
                    soco_device = SoCo(indigo_device.address)
                    self.logger.debug(f"✅ Fallback SoCo created for {indigo_device.name} at {indigo_device.address}")
                except Exception as e:
                    self.logger.error(f"❌ Direct SoCo init failed for {indigo_device.name}: {e}")
                    return

            # ✅ Always store in lookup maps
            self.soco_by_ip[indigo_device.address] = soco_device
            self.ip_to_indigo_device[indigo_device.address] = indigo_device
            self.safe_debug(f"✅ soco_by_ip[{indigo_device.address}] stored with SoCo {getattr(soco_device, 'uid', 'unknown')}")

            # 🆔 Update ZP_LocalUID from SoCo
            try:
                zp_uid = soco_device.uid
                indigo_device.updateStateOnServer("ZP_LocalUID", value=zp_uid)
                self.logger.debug(f"🆔 Set ZP_LocalUID for {indigo_device.name}: {zp_uid}")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to set ZP_LocalUID for {indigo_device.name}: {e}")

            # 🧠 ✅ Patch: ensure UUID maps back to Indigo device
            try:
                zp_uid = soco_device.uid
                if zp_uid:
                    self.logger.debug(f"🔁 Mapping UUID {zp_uid} to Indigo device: {indigo_device.name}")
                    self.uuid_to_indigo_device[zp_uid] = indigo_device
            except Exception as e:
                self.logger.error(f"❌ Failed to bind UUID to Indigo device in deviceStartComm: {e}")

            # 🧪 Log model name
            model_name = self.get_model_name(soco_device)
            self.logger.debug(f"🧪 Retrieved model_name for {indigo_device.name}: {model_name}")
            indigo_device.updateStateOnServer("ModelName", model_name)

            # 🚀 Start event listener if needed
            if not getattr(self, "event_listener_started", False):
                try:
                    from soco.events import event_listener
                    self.logger.info("🚀 Starting SoCo Event Listener...")
                    soco.config.EVENT_LISTENER_IP = self.find_sonos_interface_ip()
                    event_listener.start(any_zone=soco_device)
                    self.event_listener_started = True
                    self.logger.debug(f"✅ SoCo Event Listener running: {event_listener.is_running}")
                except Exception as e:
                    self.logger.error(f"❌ Failed to start SoCo Event Listener: {e}")

            # 🔔 Subscribe and update group state
            try:
                self.socoSubscribe(indigo_device, soco_device)
                self.updateZoneGroupStates(indigo_device)
            except Exception as e:
                self.logger.error(f"❌ socoSubscribe() or updateZoneGroupStates() failed for {indigo_device.name}: {e}")

            #self.initZones(indigo_device)
            self.initZones(indigo_device, soco_device)
            self.logger.debug(f"During start up - lets evaluate_and_update current grouped states - yes ????")             
            self.refresh_group_topology_after_plugin_zone_change()
            #self.evaluate_and_update_grouped_states()


            for dev in indigo.devices.iter("self"):
                ip = dev.address
                if ip:
                    try:
                        soco = SoCo(ip)
                        self.ip_to_soco_device[ip] = soco
                    except Exception as e:
                        self.logger.warning(f"Failed to initialize SoCo for {ip}: {e}")


        except Exception as e:
            self.logger.error(f"✅ Error in deviceStartComm for {indigo_device.name}: {e}")








    ############################################################################################
    ### End of General Methods that can be called in the SonosPlugin Class
    ############################################################################################








    ######################################################################################
    # UI Validation
    def validatePrefsConfigUi(self, valuesDict):
        try:
            self.safe_debug("Validating Plugin Configuration")
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
                if valuesDict["MSTranslateClientSecret"] == "":
                    errorsDict["MSTranslateClientSecret"] = "Please enter an Microsoft Translate Client Secret."

            if len(errorsDict) > 0:
                self.logger.error("\t Validation Errors")
                return False, valuesDict, errorsDict
            else:
                self.safe_debug("\t Validation Succesful")
                return True, valuesDict

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################



    def _usable_host(self, h: str) -> bool:
        try:
            if not h:
                return False
            h = h.strip()
            if h in ("localhost", "0.0.0.0", "::1"):
                return False
            if h.startswith("127."):
                return False
            return True
        except Exception:
            return False


    def choose_publish_host(self, zone_ip: str | None = None) -> str | None:
        """
        Returns a LAN-reachable host/IP to publish in the announcement URI.
        Tries (in order):
          1) self.HTTPServer (if safe)
          2) self.selectedInterfaceIP (if safe)
          3) Interface on the same /24 as the target zone_ip (if provided)
          4) self.announce_bind_ip (if safe)
        """
        # Preferred explicit setting
        cand = (getattr(self, "HTTPServer", "") or "").strip()
        if self._usable_host(cand):
            return cand

        # Indigo-selected interface
        cand = (getattr(self, "selectedInterfaceIP", "") or "").strip()
        if self._usable_host(cand):
            return cand

        # Try to match the zone's /24 (very effective in mixed-interface hosts)
        if zone_ip:
            try:
                import ipaddress
                net = ipaddress.ip_network(zone_ip.rsplit(".", 1)[0] + ".0/24", strict=False)
                ip_on_subnet = self.find_sonos_interface_ip(str(net))
                if self._usable_host(ip_on_subnet):
                    return ip_on_subnet
            except Exception:
                pass

        # Last resort: whatever we recorded from the 8889 server bind
        cand = (getattr(self, "announce_bind_ip", "") or "").strip()
        if self._usable_host(cand):
            return cand

        return None





    def find_sonos_interface_ip(self, target_subnet=None):
        """
        Attempts to locate the first local interface IP that belongs to the
        target Sonos subnet. Uses `ifaddr` to enumerate adapters.

        Args:
            target_subnet (str): Optional subnet in CIDR notation.  
                                 Falls back to self.targetSonosSubnet or 192.168.80.0/24.

        Returns:
            str or None: The matching IPv4 address as a string, or None if not found.
        """
        try:
            import ipaddress, ifaddr

            # Decide which subnet to use
            subnet_to_use = target_subnet or getattr(self, "targetSonosSubnet", None) or "192.168.80.0/24"
            try:
                target_net = ipaddress.IPv4Network(subnet_to_use, strict=False)
            except Exception as e:
                self.logger.error(f"❌ Invalid subnet format '{subnet_to_use}': {e}")
                return None

            self.logger.info(f"🔍 Searching for interface IP on subnet {target_net}...")

            found_ip = None
            adapters = ifaddr.get_adapters()
            for adapter in adapters:
                for ip_obj in adapter.ips:
                    ip = ip_obj.ip
                    # Skip IPv6 or tuple addresses
                    if isinstance(ip, (list, tuple)):
                        continue
                    try:
                        ip_addr = ipaddress.IPv4Address(ip)
                    except ipaddress.AddressValueError:
                        continue

                    self.logger.debug(f"   🧪 Interface {adapter.nice_name} → IP {ip_addr}")
                    if ip_addr in target_net:
                        self.logger.info(f"   ✅ Selected interface '{adapter.nice_name}' with IP {ip_addr} (matches target subnet)")
                        found_ip = str(ip_addr)
                        return found_ip  # Return immediately on first match

            if not found_ip:
                self.logger.warning(f"❌ No interface found on target Sonos subnet {target_net}")

            return found_ip

        except Exception as e:
            self.logger.exception(f"❌ Exception in find_sonos_interface_ip: {e}")
            return None



            



#############################################################################################################################################################################################################
### Event Handler to process player controls and soco state changes and maintain current dynamic state updates
#############################################################################################################################################################################################################
    def soco_event_handler(self, event_obj):

        ## The first try block here can set variables and or log various things that need to be defined or checked ahead of the event processing loop
        try:
            soco_ip = getattr(getattr(event_obj, "soco", None), "ip_address", "(no soco)")
            soco_ref = getattr(event_obj, "soco", None)
            zone_ip = getattr(soco_ref, "ip_address", None)
            #self.logger.warning("📥 Raw Event Object Received:")
            #self.logger.warning(f"   ⤷ service: {getattr(event_obj.service, 'service_type', '?')}")
            #self.logger.warning(f"   ⤷ sid: {getattr(event_obj, 'sid', '?')}")
            #self.logger.warning(f"   ⤷ soco.ip: {soco_ip}")
            #self.logger.warning(f"   ⤷ variables: {event_obj.variables}")
            service_type = getattr(event_obj.service, "service_type", "").lower()
            # 👇 keep a lowercased copy ONLY for string checks; DO NOT use it for lookups
            sid_lc = (getattr(event_obj, "sid", "") or "").lower()
            sid_orig = getattr(event_obj, "sid", "")  # preserve original casing for mapping later
            zone_ip = getattr(getattr(event_obj, "soco", None), "ip_address", None)
        except Exception as log_err:
            self.logger.error(f"❌ Failed to log raw event object: {log_err}")



    #        # the following is a dectection and log event only to see if we can isolate
    #        if not zone_ip:
    #            self.logger.info(f"🔎 ZGT event with no source IP — likely a Sonos response to a command or an unsolicted subscription song change, subscription renewal or other Sonos system or app event.")
    #            #return
    #        else:
    #            self.logger.info(f"🔎 New check - ZoneGroupTopology event triggered by {zone_ip}")


        ######################################################################################################################################################################################################
        ### Zone Group Topology (ZGT) processing
        ######################################################################################################################################################################################################

        is_zgt_event = (
            "zonegrouptopology" in service_type or
            "zonegrouptopology" in sid_lc or
            "zone_group_state" in event_obj.variables or
            "ZoneGroupState" in event_obj.variables
        )

        if is_zgt_event:
    #            self.logger.info(f"🔎 This is from - (if is_zgt_event) - logic - ZoneGroupTopology event from {zone_ip} missing ZoneGroupState")
    #            self.logger.info(f"🧪 9999 zgt event detected entering the event logic now...")
    #            self.logger.info(f"🔎 ZoneGroupTopology event triggered by {zone_ip}")
            zone_state_xml = (
                event_obj.variables.get("zone_group_state") or
                event_obj.variables.get("ZoneGroupState") or
                ""
            )

            if not zone_state_xml:
                self.logger.debug(f"🔎 This is from - (if not zone_state_xml) - logic - ZoneGroupTopology event from {zone_ip} missing ZoneGroupState")
            else:
                # Ensure XML is string, not bytes
                if isinstance(zone_state_xml, bytes):
                    try:
                        zone_state_xml = zone_state_xml.decode("utf-8", errors="replace")
                        self.logger.debug("🔧 zone_state_xml was bytes, decoded to UTF-8.")
                    except Exception as decode_err:
                        self.logger.error(f"❌ Failed to decode zone_group_state XML bytes: {decode_err}")
                        return

                try:
                    self.logger.debug(f"🧪 zgt event was detected entering the phase 2 try event logic now...")
                    parsed_groups = self.parse_zone_group_state(zone_state_xml)
                    if not parsed_groups:
                        self.logger.warning("⚠️ Parsed zone group data was empty.")
                    else:
                        #self.logger.warning(f"🧪 Parsed {len(parsed_groups)} group(s) from XML. Evaluating cache...")

                        def _normalized_group_snapshot(group_dict):
                            return json.dumps(group_dict, sort_keys=True)

                        incoming_snapshot = _normalized_group_snapshot(parsed_groups)
                        with self.zone_group_state_lock:
                            current_snapshot = _normalized_group_snapshot(self.zone_group_state_cache)

                            if incoming_snapshot == current_snapshot:
                                self.logger.debug("⏩ No group topology change detected — skipping re-evaluation.")
                                return

                            self.zone_group_state_cache = copy.deepcopy(parsed_groups)
                            self.logger.info(f"💾 zone_group_state_cache updated with {len(parsed_groups)} group(s)")

                        for group_id, data in parsed_groups.items():
                            for m in data["members"]:
                                bonded_flag = " (Bonded)" if m["bonded"] else ""
                                coord_flag = " (Coordinator)" if m["coordinator"] else ""
                                # self.logger.warning(f"   → {m['name']} @ {m['ip']}{bonded_flag}{coord_flag}")

                        #self.logger.info("📣 Calling evaluate_and_update_grouped_states() after ZoneGroupTopology change...")
                        self.refresh_group_topology_after_plugin_zone_change()
                        #self.evaluate_and_update_grouped_states()

                        self.logger.debug("📣 Propagating updated Grouped states to all devices...")
                        for dev in indigo.devices.iter("self"):
                            self.updateZoneGroupStates(dev)

                except Exception as e:
                    self.logger.error(f"❌ Failed to parse ZoneGroupState XML: {e}")
    #            self.logger.info(f"🧪 zgt event detected EXITING the event logic now...")


        try:
            service_type = getattr(event_obj.service, "service_type", "UNKNOWN")
            # 👇 keep the original SID here (no .lower()) so mapping by SID works
            sid = getattr(event_obj, "sid", "N/A")
            zone_ip = getattr(event_obj, "zone_ip", None)

            #self.logger.warning(f"📥 RAW EVENT RECEIVED — service: {service_type} | sid: {sid}")

            if not zone_ip and hasattr(event_obj, "soco"):
                zone_ip = getattr(event_obj.soco, "ip_address", None)

            indigo_device = None
            dev_id = None

            for dev_lookup_id, subs in self.soco_subs.items():
                if any(sub.sid == sid for sub in subs.values()):
                    indigo_device = indigo.devices[int(dev_lookup_id)]
                    dev_id = indigo_device.id
                    if not zone_ip:
                        zone_ip = indigo_device.address
                    break

            if not indigo_device:
                self.logger.debug(f"⚠️ Event received with unknown SID {sid}. Cannot map to Indigo device.")
                return

            #self.logger.debug(f"📡 Event received from {zone_ip} — SID={sid} | Service={service_type}")
            #self.logger.debug(f"📦 Event variables: {getattr(event_obj, 'variables', {})}")

            # 👇 Only treat GroupStateChanged as a ZGT hint; do NOT return here so other services still process.
            vars_dict = getattr(event_obj, "variables", {}) or {}
            if ("GroupStateChanged" in vars_dict or "groupstatechanged" in vars_dict) and "ZoneGroupTopology" in service_type:
                self.logger.info("🔄 GroupStateChanged (ZGT) present — triggering group state refresh (no early return)…")
                # optional: self.refresh_group_topology_after_plugin_zone_change()
                # fall through to allow transport/rendering updates to be handled

            if not zone_ip:
                zone_ip = "unknown"

            state_updates = {}

            self.safe_debug(f"🧪 Event handler fired! SID={getattr(event_obj, 'sid', 'N/A')} zone_ip={zone_ip} Type={type(event_obj)}")
            self.safe_debug(f"🧑‍💻 Full event variables: {getattr(event_obj, 'variables', {})}")



        ######################################################################################################################################################################################################
        ### Transport State processing
        ######################################################################################################################################################################################################

            def safe_call(val):
                try:
                    return val() if callable(val) else val
                except Exception:
                    return ""


            if "transport_state" in event_obj.variables:
                transport_state = event_obj.variables["transport_state"]
                transport_state_upper = transport_state.upper()
                state_updates["ZP_STATE"] = transport_state_upper
                indigo_device.updateStateOnServer(key="State", value=transport_state_upper)
                indigo_device.updateStateOnServer(key="ZP_STATE", value=transport_state_upper)
                self.logger.debug(f"🔄 Updated State and ZP_STATE from event: {transport_state_upper}")

            if not hasattr(self, "last_siriusxm_track_by_dev"):
                self.last_siriusxm_track_by_dev = {}
            if not hasattr(self, "last_siriusxm_artist_by_dev"):
                self.last_siriusxm_artist_by_dev = {}


            current_uri = (
                event_obj.variables.get("current_track_uri") or
                event_obj.variables.get("enqueued_transport_uri") or
                event_obj.variables.get("av_transport_uri")
            )

            uri_priority = [
                ("enqueued_transport_uri", event_obj.variables.get("enqueued_transport_uri", "")),
                ("av_transport_uri", event_obj.variables.get("av_transport_uri", "")),
                ("current_track_uri", event_obj.variables.get("current_track_uri", ""))
            ]

            if "volume" in event_obj.variables:
                vol = event_obj.variables["volume"]
                state_updates["ZP_VOLUME_MASTER"] = int(vol.get("Master", 0))
                state_updates["ZP_VOLUME_LF"] = int(vol.get("LF", 0))
                state_updates["ZP_VOLUME_RF"] = int(vol.get("RF", 0))
                state_updates["ZP_VOLUME"] = str(vol)

            if "mute" in event_obj.variables:
                mute_val = event_obj.variables["mute"]
                mute_state = mute_val.get("Master") if isinstance(mute_val, dict) else mute_val
                state_updates["ZP_MUTE"] = "true" if str(mute_state).strip() == "1" else "false"

            if "bass" in event_obj.variables:
                try:
                    state_updates["ZP_BASS"] = int(event_obj.variables["bass"])
                except Exception as e:
                    self.logger.warning(f"⚠️ Invalid bass value: {event_obj.variables['bass']} — {e}")

            if "treble" in event_obj.variables:
                try:
                    state_updates["ZP_TREBLE"] = int(event_obj.variables["treble"])
                except Exception as e:
                    self.logger.warning(f"⚠️ Invalid treble value: {event_obj.variables['treble']} — {e}")

            if state_updates:
                for k, v in state_updates.items():
                    self.safe_debug(f"🔄 Lightweight update → {k}: {v}")
                    indigo_device.updateStateOnServer(key=k, value=v)


        ######################################################################################################################################################################################################
        ### Refresh Group Membership - only if there are any_grouped = any
        ######################################################################################################################################################################################################


            try:
                any_grouped = any(
                    str(dev.states.get("Grouped", "")).lower() == "true"
                    for dev in indigo.devices.iter("self")
                    if dev.enabled
                )
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to evaluate 'Grouped' status across devices: {e}")
                any_grouped = False

            if any_grouped:
                soco_device = self.getSoCoDeviceByIP(indigo_device.address)
                if soco_device:
                    self.refresh_group_membership(indigo_device, soco_device)
                    self.logger.info(f"🔁 Active group detected — forcing master/slave state updates for {indigo_device.name}")      
                    self.refresh_group_topology_after_plugin_zone_change()
                    #self.evaluate_and_update_grouped_states()
                else:
                    self.logger.warning(f"⚠️ Could not refresh group membership: No SoCo device for {indigo_device.name}")
            else:
                self.logger.debug("⏩ No active groups (Grouped=true) detected — skipping group refresh/state sync")



        ######################################################################################################################################################################################################
        ### Customized State Processing for things like SiriusXM, Pandora, Sonos, Apple, Etc.
        ######################################################################################################################################################################################################


            # Initialize helpers and flags early
            is_siriusxm = False
            is_pandora = False
            is_apple_music = False
            is_sonos_radio = False
            is_sonos = False
            detected_source = "Sonos"  # default fallback

            for name, uri in uri_priority:
                if "x-sonosapi-hls:channel-linear" in uri:
                    detected_source = "SiriusXM"
                    is_siriusxm = True
                    break
                elif "x-sonosapi-radio" in uri or "VC1%3a%3aST%3a%3aST%3a" in uri:
                    detected_source = "Pandora"
                    is_pandora = True
                    break
                elif "x-apple-music" in uri:
                    detected_source = "Apple Music"
                    is_apple_music = True
                    break
                elif "x-sonosapi-stream" in uri:
                    detected_source = "Sonos Radio"
                    is_sonos_radio = True
                    break
                elif "x-sonos-http:librarytrack" in uri:
                    detected_source = "Sonos"
                    is_apple_music = True
                    break

            if detected_source == "Sonos":
                is_sonos = True

            self.safe_debug(f"✅ Detected source: {detected_source}")
            state_updates["ZP_SOURCE"] = detected_source

            # === SiriusXM handling ===
            if is_siriusxm:
                meta = event_obj.variables.get("enqueued_transport_uri_meta_data") or event_obj.variables.get("av_transport_uri_meta_data")
                if meta:
                    try:
                        title_raw = safe_call(getattr(meta, "title", ""))
                        self.safe_debug(f"🔍 Raw SiriusXM title string: '{title_raw}'")

                        ch_part, name_part = "", ""
                        if " - " in title_raw:
                            ch_part, name_part = title_raw.split(" - ", 1)
                            ch_part = ch_part.strip()
                            name_part = name_part.strip()
                        else:
                            ch_part = title_raw.strip()
                            name_part = ""

                        state_updates["ZP_TRACK"] = ch_part or "Unknown Channel"
                        state_updates["ZP_STATION"] = ch_part or "Unknown Station"
                        state_updates["ZP_ARTIST"] = name_part or "Unknown Artist"
                        state_updates["ZP_ALBUM"] = ""

                        self.safe_debug(f"🎶 SiriusXM parsed → TRACK: '{state_updates['ZP_TRACK']}', ARTIST: '{state_updates['ZP_ARTIST']}', STATION: '{state_updates['ZP_STATION']}'")

                        self.last_siriusxm_track_by_dev[dev_id] = state_updates["ZP_TRACK"]
                        self.last_siriusxm_artist_by_dev[dev_id] = state_updates["ZP_ARTIST"]

                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to parse SiriusXM metadata: {e}")
                        fallback_track = self.last_siriusxm_track_by_dev.get(dev_id, "Unknown Channel")
                        fallback_artist = self.last_siriusxm_artist_by_dev.get(dev_id, "Unknown Artist")
                        state_updates["ZP_TRACK"] = fallback_track
                        state_updates["ZP_STATION"] = fallback_track
                        state_updates["ZP_ARTIST"] = fallback_artist
                        state_updates["ZP_ALBUM"] = ""

            # === Pandora handling ===
            if is_pandora and "enqueued_transport_uri_meta_data" in event_obj.variables:
                meta = event_obj.variables["enqueued_transport_uri_meta_data"]
                try:
                    station_title = safe_call(getattr(meta, "title", ""))
                    if station_title.endswith(" (My Station)"):
                        station_title = station_title.replace(" (My Station)", "").strip()
                    if station_title:
                        state_updates["ZP_STATION"] = station_title
                        self.safe_debug(f"📻 Extracted Pandora station name: {station_title}")

                    station_creator = safe_call(getattr(meta, "creator", ""))
                    if station_creator:
                        state_updates["ZP_CREATOR"] = station_creator
                        if "ZP_ARTIST" not in state_updates or not state_updates["ZP_ARTIST"]:
                            state_updates["ZP_ARTIST"] = station_creator
                        self.safe_debug(f"🎨 Extracted Pandora creator: {station_creator}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to parse Pandora metadata: {e}")

            #################################################################################################
            ### Is everything here and after a drop through that fires everytime? 
            #################################################################################################

            #################################################################################################
            ### Is everything here and after a drop through that fires everytime? 
            ### this refresh_group_mambership below seems to be the only call to refresh group membership - 
            ### perhaps we need to wrap this with test logic to only call if group is changed, seems to 
            ### happen now on every group trigger? This would also remove the extra art save.
            #################################################################################################

#            self.logger.info("Trapping here what fires after drop through from all other states assesment events")    

            # === General metadata ===
            if "current_track_meta_data" in event_obj.variables:
                meta = event_obj.variables["current_track_meta_data"]
                try:
                    meta_dict = meta.to_dict()
                    track_title = meta_dict.get("title", "")
                    track_album = meta_dict.get("album", "")
                    track_artist = meta_dict.get("artist", "")
                    track_creator = meta_dict.get("creator", "")

                    if track_title:
                        state_updates["ZP_TRACK"] = track_title
                    if track_album:
                        state_updates["ZP_ALBUM"] = track_album
                    if track_artist:
                        state_updates["ZP_ARTIST"] = track_artist
                    elif track_creator:
                        state_updates["ZP_ARTIST"] = track_creator
                    if track_creator:
                        state_updates["ZP_CREATOR"] = track_creator

                    # ✅ NEW: Capture and store all relevant URIs
                    current_uri = event_obj.variables.get("current_track_uri", "")
                    av_transport_uri = event_obj.variables.get("av_transport_uri", "")
                    enqueued_uri = event_obj.variables.get("enqueued_transport_uri", "")

                    state_updates["ZP_CurrentTrackURI"] = current_uri
                    state_updates["ZP_AVTransportURI"] = av_transport_uri
                    state_updates["ZP_EnqueuedURI"] = enqueued_uri

                    self.safe_debug(f"📡 Captured URIs — current: {current_uri}, av: {av_transport_uri}, enqueued: {enqueued_uri}")

                    self.safe_debug(f"🎵 General metadata parsed: title={track_title}, artist={track_artist}, creator={track_creator}, album={track_album}")

                except Exception as e:
                    self.logger.debug(f"⚠️ Failed to extract general metadata: {e}")

            # === Apply all collected state updates ===
            if state_updates:
                for k, v in state_updates.items():
                    self.safe_debug(f"🔄 Heavyweight update → {k}: {v}")
                    indigo_device.updateStateOnServer(key=k, value=v)


#### Do I need thois if it is firing from controller? Seems to fire with both if on but neither when off?

            # === Artwork block — moved here for coordination after states ===
            try:
                indigo_device = self.getIndigoDeviceFromEvent(event_obj)
                if indigo_device:
                    self.update_album_artwork(
                        event_obj=event_obj,
                        dev=indigo_device,
                        zone_ip=indigo_device.address.strip()
                    )
                    #self.logger.info(f"🖼️ Standalone - I am updating artwork here for {zone_ip} — after drop through from all other states assesment events")    
                else:
                    self.logger.warning("⚠️ Skipping artwork update — Indigo device could not be resolved from event")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to update album artwork: {e}")


            # === Coordinator logic ===
            is_master = False
            if indigo_device:
                try:
                    coordinator = self.getCoordinatorDevice(indigo_device)
                    is_master = (coordinator.address == indigo_device.address)
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not determine coordinator for {indigo_device.name}: {e}")
            else:
                self.logger.warning("⚠️ Skipping coordinator check — indigo_device is None")


            if is_master:
                self.updateStateOnSlaves(indigo_device)
                #self.evaluate_and_update_grouped_states()            

        except Exception as e:
            self.logger.error(f"❌ Error in soco_event_handler: {e}")


#################################################################################################
### End of Event Handler
#################################################################################################





    def getSoCoDeviceByIP(self, ip_address):
        try:
            if not hasattr(self, "soco_device_cache"):
                self.soco_device_cache = {}

            #self.safe_debug(f"🔍 getSoCoDeviceByIP called for {ip_address}")

            if ip_address in self.soco_device_cache:
                self.safe_debug(f"✅ Found {ip_address} in soco_device_cache")
                return self.soco_device_cache[ip_address]

            # Try to discover devices
            from soco import discover, SoCo
            devices = discover()
            if devices:
                self.safe_debug(f"🔍 Discovered devices: {[dev.ip_address for dev in devices]}")
                for dev in devices:
                    self.soco_device_cache[dev.ip_address] = dev

                if ip_address in self.soco_device_cache:
                    self.safe_debug(f"✅ Found {ip_address} after discovery")
                    return self.soco_device_cache[ip_address]
                else:
                    self.logger.debug(f"⚠️ IP {ip_address} not found in discovered devices")
            else:
                self.logger.warning("⚠️ No SoCo devices discovered")

            # 🔁 NEW: fallback to direct SoCo init
            self.logger.debug(f"⚠️ getSoCoDeviceByIP({ip_address}) returned None — attempting fallback init...")
            try:
                fallback_device = SoCo(ip_address)
                self.soco_device_cache[ip_address] = fallback_device
                self.logger.debug(f"✅ Fallback SoCo added to soco_device_cache[{ip_address}]")
                return fallback_device
            except Exception as fallback_error:
                self.logger.error(f"❌ Fallback SoCo init failed in getSoCoDeviceByIP: {fallback_error}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error in getSoCoDeviceByIP: {e}")
            return None


        
    def getCoordinatorDevice(self, device):
        """
        Given an Indigo device, return the Indigo device object representing
        the group coordinator (master) for that device's group.
        If the device is the master or resolution fails, returns itself.
        """
        try:
            if not device:
                self.logger.error("❌ getCoordinatorDevice: device argument is None")
                return None

            zone_ip = device.address
            if not zone_ip:
                self.logger.error(f"❌ getCoordinatorDevice: device {device.name} has no IP address set")
                return device

            self.logger.debug(f"🔍 Looking up SoCo device for IP: {zone_ip}")
            soco_device = self.getSoCoDeviceByIP(zone_ip)

            if not soco_device:
                self.logger.warning(f"⚠️ getSoCoDeviceByIP({zone_ip}) returned None — treating {device.name} as its own coordinator.")
                if hasattr(self, "soco_device_cache"):
                    self.logger.debug(f"📋 Cached SoCo devices: {list(self.soco_device_cache.keys())}")
                else:
                    self.logger.debug("📋 No soco_device_cache attribute present.")
                return device  # fallback

            # Confirm group/coordinator exists
            group = getattr(soco_device, "group", None)
            if not group or not hasattr(group, "coordinator"):
                self.logger.warning(f"⚠️ SoCo device {zone_ip} has no group or coordinator info — using self.")
                return device

            coordinator = group.coordinator
            coordinator_ip = getattr(coordinator, "ip_address", None)
            if not coordinator_ip:
                self.logger.warning(f"⚠️ Coordinator IP is missing — falling back to self.")
                return device

            self.logger.debug(f"✅ Group coordinator IP for {device.name}: {coordinator_ip}")

            # Match to Indigo device
            for dev in indigo.devices.iter("self"):
                if dev.address == coordinator_ip:
                    self.logger.debug(f"✅ Found Indigo device for coordinator: {dev.name} ({coordinator_ip})")
                    return dev

            self.logger.warning(f"⚠️ No Indigo device matches coordinator IP {coordinator_ip}; defaulting to self.")
            return device

        except Exception as e:
            self.logger.error(f"❌ Exception in getCoordinatorDevice: {e}")
            return device





    def clear_device_states(self, indigo_device):
        try:
            state_defaults = {
                "ModelName": "",
                "SerialNumber": "",
                "ZP_INFO": "",
                "ZP_STATION": "",
                "ZP_VOLUME": "",
                "ZP_VOLUME_MASTER": 0,
                "ZP_VOLUME_LF": 0,
                "ZP_VOLUME_RF": 0,
                "ZP_MUTE": "false",
                "ZP_BASS": "0",
                "ZP_TREBLE": "0",
                "ZP_STATE": "",
                "ZP_ART": "",
                "ZP_TRACK": "",
                "ZP_DURATION": "",
                "ZP_RELATIVE": "",
                "ZP_ALBUM": "",
                "ZP_ARTIST": "",
                "ZP_SOURCE": "",                
                "ZP_CREATOR": "",
                "ZP_AIName": "",
                "ZP_AIPath": "",
                "ZP_CurrentURI": "",
                "ZP_ZoneName": "",
                "ZP_LocalUID": "",
                "ZP_NALBUM": "",
                "ZP_NARTIST": "",
                "ZP_NCREATOR": "",
                "ZP_NART": "",
                "ZP_NTRACK": "",
                "Q_Crossfade": False,
                "Q_Repeat": False,
                "Q_RepeatOne": False,
                "Q_Shuffle": False,
                "Q_Number": "",
                "Q_ObjectID": "",
                "GROUP_Coordinator": False,
                "GROUP_Name": "",
                "ZP_CurrentTrack": "",
                "ZP_CurrentTrackURI": "",
                "ZoneGroupID": "",
                "ZoneGroupName": "",
                "ZonePlayerUUIDsInGroup": "",
                "bootseq": 0,
                "alive": "",
            }

            for state_id, default_value in state_defaults.items():
                indigo_device.updateStateOnServer(state_id, default_value)

            self.logger.info(f"✅ Cleared all states for device '{indigo_device.name}'")

        except Exception as e:
            self.logger.error(f"❌ Failed to clear states for device '{indigo_device.name}': {e}")





    def soco_discover_and_subscribe(self):
        try:
            self.logger.info("🔍 Discovering Sonos devices on the network...")

            devices = soco.discover(timeout=5)  # Add a timeout to avoid blocking forever
            if not devices:
                self.logger.warning("❌ No Sonos devices discovered.")
                return

            self.logger.info(f"✅ Found {len(devices)} Sonos device(s). Subscribing to events...")

            # Clear and rebuild the device cache
            self.soco_by_ip = {}

            for device in devices:
                ip = device.ip_address
                name = device.player_name
                self.logger.info(f"   📻 Discovered {name} @ {ip}")

                # Cache the SoCo device by IP for later lookup
                self.soco_by_ip[ip] = device

                # Try to match to an Indigo device by IP
                matched_device = None
                for dev in indigo.devices.iter("self"):
                    if dev.address == ip:
                        matched_device = dev
                        break

                if matched_device:
                    self.safe_debug(f"   🔗 Matched to Indigo device {matched_device.name} (ID: {matched_device.id})")
                    self.socoSubscribe(matched_device, device)
                else:
                    self.logger.warning(f"⚠️ No Indigo device found matching IP {ip}")

        except Exception as e:
            self.logger.exception("❌ Error during Sonos device discovery and subscription")

            

    ######################################################################################
    # Utiliies






    def build_ip_to_device_map(self):
        self.ip_to_indigo_device = {
            dev.address.strip(): dev
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos")
        }



    PORT = 8888
    IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

    class SimpleImageHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=IMAGES_DIR, **kwargs)

    if __name__ == "__main__":
        with socketserver.TCPServer(("", PORT), SimpleImageHandler) as httpd:
            print(f"🎵 Mini Sonos Art Server serving at http://localhost:{PORT}")
            httpd.serve_forever()



    def cleanString(self, in_string):
        try:
            in_string = in_string.replace("&", "&amp;amp;")
            in_string = in_string.replace("'", "&apos;")
            return in_string

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def restoreString(self, in_string, filter):
        try:
            in_string = in_string.replace("&amp;apos;", "\'")
            if filter == 0:
                in_string = in_string.replace("&amp;amp;", "&")
                in_string = in_string.replace("&amp;", "&")
            in_string = in_string.replace("&quot;", "\"")
            in_string = in_string.replace("&lt;", "<")
            in_string = in_string.replace("&gt;", ">")
            in_string = in_string.replace("&apos;", "'")
            return in_string

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def logSep(self, debug):
        try:
            if debug:
                self.safe_debug("---------------------------------------------")
            else:
                self.logger.info("---------------------------------------------")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement



#    def restoreString(self, in_string):
#        if in_string:
#            return in_string
#        return ""


    def shit_save_restoreString(self, in_string, _unused=None):
        if not in_string:
            self.logger.warning("⚠️ restoreString called with None or empty input.")
            return ""
        try:
            return in_string.replace("&amp;apos;", "'").replace("&amp;quot;", '"')
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to clean metadata string: {e}")
            return in_string










    def updateZoneGroupStates(self, dev):
        try:
            device_ip = dev.address.strip()
            soco_device = self.soco_by_ip.get(device_ip)
            if not soco_device:
                self.logger.warning(f"⚠️ No SoCo device found for IP {device_ip}")
                return

            group = soco_device.group
            coordinator = group.coordinator
            group_members = group.members

            group_id = group.uid
            #self.trace_me()               
            group_name = coordinator.player_name or "Unknown Group"
            member_uuids = [member.uid for member in group_members]

            bonded_model_types = ["sub", "surround", "sl"]
            coordinator_ip = coordinator.ip_address.strip()
            coord_indigo = self.ip_to_indigo_device.get(coordinator_ip)

            if not coord_indigo:
                self.logger.debug(f"⚠️ Could not resolve Indigo device for coordinator: {coordinator.player_name} ({coordinator_ip})")
                return

            # Get coordinator's actual grouped state from Indigo
            coord_grouped_state = str(coord_indigo.states.get("Grouped", "")).lower()
            is_grouped = (coord_grouped_state == "true")

            for member in group_members:
                member_ip = member.ip_address.strip()
                member_name = member.player_name or ""

                indigo_device = self.ip_to_indigo_device.get(member_ip)
                if not indigo_device:
                    self.logger.debug(f"Skipping update: No Indigo device found for IP {member_ip} ({member_name})")
                    continue

                is_coordinator = (coordinator_ip == member_ip)

                # Lookup model_name from cache to determine bonding
                cached_soco = self.soco_by_ip.get(member_ip)
                model_name = getattr(cached_soco, "model_name", "").lower() if cached_soco else ""
                is_bonded = any(bonded_type in model_name for bonded_type in bonded_model_types)

                # Apply coordinator's grouped state to all members
                new_grouped_state = "true" if is_grouped else "false"

                # Update Indigo states
                #self.trace_me()
                indigo_device.updateStateOnServer("ZP_ZoneName", member_name)
                indigo_device.updateStateOnServer("ZoneGroupID", group_id)
                indigo_device.updateStateOnServer("ZoneGroupName", group_name)
                indigo_device.updateStateOnServer("ZonePlayerUUIDsInGroup", ", ".join(member_uuids))

                if "GROUP_Coordinator" in indigo_device.states:
                    indigo_device.updateStateOnServer("GROUP_Coordinator", str(is_coordinator).lower())
                else:
                    self.logger.warning(f"⚠️ Device '{indigo_device.name}' missing 'GROUP_Coordinator' state — skipping.")

                if "GROUP_Name" in indigo_device.states:
                    indigo_device.updateStateOnServer("GROUP_Name", group_name)
                else:
                    self.logger.warning(f"⚠️ Device '{indigo_device.name}' missing 'GROUP_Name' state — skipping.")

                if "Grouped" in indigo_device.states:
                    indigo_device.updateStateOnServer("Grouped", new_grouped_state)
                else:
                    self.logger.warning(f"⚠️ Device '{indigo_device.name}' missing 'Grouped' state — skipping.")

                #self.logger.info(f"✅ Updated {indigo_device.name}: Coordinator={is_coordinator}, Grouped={new_grouped_state}, Bonded={is_bonded}")

        except Exception as e:
            self.logger.error(f"❌ Error updating zone group states for {dev.name}: {e}")







    def get_soco_by_uuid(self, uuid):
        for ip, soco in self.soco_by_ip.items():
            try:
                if soco.uid == uuid:
                    return soco
            except Exception as e:
                self.logger.warning(f"⚠️ Could not retrieve UID from SoCo at {ip}: {e}")
        self.logger.debug(f"🔍 No SoCo found for UUID {uuid}")
        return None





    def parse_zone_group_state(self, xml_data):
        import xml.etree.ElementTree as ET
        group_dict = {}

        #self.logger.warning("🛠 ENTERED parse_zone_group_state()")

        # Ensure xml_data is a str (not bytes)
        if isinstance(xml_data, bytes):
            try:
                xml_data = xml_data.decode("utf-8", errors="replace")
                self.logger.debug("🔧 XML data was bytes, decoded to UTF-8.")
            except Exception as decode_err:
                self.logger.error(f"❌ Failed to decode XML data: {decode_err}")
                return {}

        #self.logger.warning(f"📨 Incoming XML data length: {len(xml_data)}")
        #self.logger.warning(f"🔎 First 200 chars: {xml_data[:200]}")

        try:
            root = ET.fromstring(xml_data)
            for zg in root.findall(".//ZoneGroup"):
                coordinator = zg.get("Coordinator")
                group_id = zg.get("ID", coordinator)  # fallback to UUID if ID is missing
                members = []

                for member in zg.findall("ZoneGroupMember"):
                    zone_name = member.get("ZoneName", "")
                    if "sub" in zone_name.lower():
                        #self.logger.warning(f"🚫 Skipping bonded sub: {zone_name}")
                        continue  # skip Sub devices

                    uuid = member.get("UUID")
                    location = member.get("Location", "")
                    try:
                        ip = location.split("//")[1].split(":")[0] if location else "?"
                    except Exception:
                        ip = "?"

                    bonded = member.get("Invisible", "0") == "1"
                    members.append({
                        "uuid": uuid,
                        "name": zone_name,
                        "ip": ip,
                        "bonded": bonded,
                        "coordinator": (uuid == coordinator)
                    })

                if members:
                    group_dict[group_id] = {
                        "coordinator": coordinator,
                        "members": members
                    }

            #self.logger.warning(f"✅ Parsed {len(group_dict)} group(s) from ZoneGroupState.")
            for gid, group in group_dict.items():
                for m in group["members"]:
                    bonded = " (Bonded)" if m["bonded"] else ""
                    coordinator = " (Coordinator)" if m["coordinator"] else ""
                    #self.logger.warning(f"   → {m['name']} @ {m['ip']}{bonded}{coordinator}")

        except Exception as e:
            self.logger.error(f"❌ Failed to parse ZoneGroupState XML: {e}")
            return {}

        return group_dict






    def fetch_live_topology(self, ip):
        import xml.etree.ElementTree as ET
        import requests

        try:
            url = f"http://{ip}:1400/status/topology"
            resp = requests.get(url, timeout=3)
            resp.raise_for_status()
            tree = ET.fromstring(resp.content)

            groups = {}
            for zp in tree.findall(".//ZonePlayer"):
                uuid = zp.text.strip().replace("uuid:", "")
                name = zp.attrib.get("zoneName", "Unknown")
                coord = zp.attrib.get("coordinator", "false").lower() == "true"
                group = zp.attrib.get("group", "Unknown")
                ip = zp.attrib.get("location", "").split("//")[-1].split(":")[0]
                groups[uuid] = {
                    "name": name,
                    "ip": ip,
                    "group": group,
                    "is_coordinator": coord
                }

            return groups

        except Exception as e:
            self.logger.error(f"❌ fetch_live_topology({ip}) failed: {e}")
            return {}



    def rebuild_ip_to_device_map(self):
        #self.logger.warning("🔁 Rebuilding IP-to-Indigo device map...")
        self.ip_to_indigo_device = {}
        for dev in indigo.devices.iter("self"):
            ip = dev.pluginProps.get("address", "").strip()
            if ip:
                self.ip_to_indigo_device[ip] = dev


    def initialize_custom_states(self, dev):
        if dev is None:
            self.logger.warning("🚫 initialize_custom_states called with None device!")
            return

        required_keys = [
            "Grouped",
            "GROUP_Coordinator",
            "GROUP_Name",
            "ZonePlayerUUIDsInGroup",
            "ZP_LocalUID",
        ]

        created_keys = []

        for key in required_keys:
            if key not in dev.states:
                self.logger.warning(f"🔧 Initializing missing state '{key}' on device: {dev.name}")
                dev.updateStateOnServer(key, "")
                created_keys.append(key)
            else:
                self.logger.debug(f"✅ State key '{key}' already present on device: {dev.name}")

        if created_keys:
            self.logger.info(f"🛠 Initialized missing states on {dev.name}: {', '.join(created_keys)}")





#################################################################################################
### Evaluate_and_update_grouped_states
#################################################################################################


    def evaluate_and_update_grouped_states(self, dev=None):
        now = time.time()
        if hasattr(self, "_last_group_eval") and now - self._last_group_eval < 3.0:
            return
        self._last_group_eval = now

        # Initialize required custom states
        if dev:
            if dev is not None:
                self.logger.debug(f"⚙️ Evaluating group state for device: {dev.name}")
                self.initialize_custom_states(dev)
            else:
                self.logger.warning("🚫 Received 'None' for dev argument — skipping initialize_custom_states()")
        else:
            self.logger.debug("⚙️ Evaluating group state for all Sonos devices...")
            for d in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if d is not None:
                    self.initialize_custom_states(d)
                else:
                    self.logger.warning("🚫 Encountered None in device list — skipping.")

        bonded_names = ["sub"]
        seen_groups = set()

        self.logger.info("🔄 Evaluating current group states for all Sonos devices...")

        # 🧠 Reset evaluated group tracking cache
        self.evaluated_group_members_by_coordinator = {}

        for group_uid, group_data in self.zone_group_state_cache.items():
            coordinator_entry = group_data.get("coordinator")
            member_entries = group_data.get("members", [])

            self.logger.debug(f"🧪 Group ID: {group_uid} | Coordinator: {coordinator_entry} | Members: {len(member_entries)}")

            if group_uid in seen_groups:
                continue
            seen_groups.add(group_uid)

            coordinator_uuid = coordinator_entry.get("uuid") if isinstance(coordinator_entry, dict) else coordinator_entry
            coordinator = self.get_soco_by_uuid(coordinator_uuid)

            if not coordinator:
                self.logger.debug(f"⚠️ 1st Could not resolve SoCo coordinator for UUID: {coordinator_uuid}")
                continue

            members = []
            for entry in member_entries:
                member_uuid = entry.get("uuid") if isinstance(entry, dict) else entry
                soco_dev = self.get_soco_by_uuid(member_uuid)
                if soco_dev:
                    members.append(soco_dev)
                else:
                    self.logger.debug(f"⚠️ Could not resolve SoCo device for UUID: {entry}")

            if not members:
                self.logger.warning(f"⚠️ Group {group_uid} has no resolvable members — skipping.")
                continue

            # 🔍 Evaluate non-bonded members
            non_bonded_members = [
                m for m in members
                if not any(b in m.player_name.lower() for b in bonded_names)
            ]
            unique_names = set(m.player_name.lower() for m in non_bonded_members)

            # ✅ Determine grouped status — TRUE only if more than one *non-bonded* member
            is_grouped = len(unique_names) > 1

            if not is_grouped:
                self.logger.debug(f"🧩 Not grouped: {coordinator.player_name} — fewer than 2 unique non-bonded members")

            group_name = coordinator.player_name if is_grouped else members[0].player_name

            # 🧠 Initialize tracking for this group
            if group_name not in self.evaluated_group_members_by_coordinator:
                self.logger.debug(f"📦 Initializing group entry for '{group_name}' in evaluated_group_members_by_coordinator")
                self.evaluated_group_members_by_coordinator[group_name] = []

            for member in members:
                member_ip = member.ip_address.strip()
                indigo_device = self.ip_to_indigo_device.get(member_ip)
                if not indigo_device:
                    self.logger.warning(f"⚠️ No Indigo device found for {member.player_name} ({member_ip}) — skipping")
                    continue

                if dev and dev.id != indigo_device.id:
                    self.logger.debug(f"⏭ Skipping {indigo_device.name} due to dev filter (looking for ID {dev.id})")
                    continue

                expected_grouped = "true" if is_grouped else "false"
                expected_coord = "true" if member == coordinator else "false"

                grouped_val = indigo_device.states.get("Grouped", "undefined")
                coord_val = indigo_device.states.get("GROUP_Coordinator", "undefined")
                name_val = indigo_device.states.get("GROUP_Name", "")

                # Update plugin-evaluated Grouped flag
                if str(grouped_val).lower() != expected_grouped:
                    self.logger.info(f"🆙 Updating 'Grouped' state for {indigo_device.name} → {expected_grouped}")
                    self.updateStateOnServer(indigo_device, "Grouped", expected_grouped)

                # Update plugin-evaluated coordinator flag
                if str(coord_val).lower() != expected_coord:
                    self.logger.info(f"🧭 Updating 'GROUP_Coordinator' state for {indigo_device.name} → {expected_coord}")
                    self.updateStateOnServer(indigo_device, "GROUP_Coordinator", expected_coord)

                # Explicit Group_Name update using indigo_device, not dev
                old_group_name = indigo_device.states.get("GROUP_Name", "Unavailable")
                if group_name != old_group_name:
                    caller = inspect.stack()[1].function
                    self.logger.debug(f"🧭 TRACE: Group_Name has changed — invoked from: {caller} — will write new value: {group_name}")
                    try:
                        indigo_device.updateStateOnServer("GROUP_Name", group_name)
                    except Exception as e:
                        self.logger.error(f"❌ Failed to write GROUP_Name='{group_name}' to {indigo_device.name}: {e}")

                # Fallback update if not already handled
                if "GROUP_Name" not in indigo_device.states:
                    self.logger.error(f"❌ Cannot update GROUP_Name for {indigo_device.name} — state key not defined!")
                elif group_name and group_name != name_val:
                    self.logger.info(f"🧩 Updating 'GROUP_Name' for {indigo_device.name} → '{group_name}' (previous: {name_val})")
                    self.updateStateOnServer(indigo_device, "GROUP_Name", group_name)

                # ✅ Add to plugin-evaluated group tracking dict
                self.logger.debug(f"✅ Adding {indigo_device.name} to evaluated group '{group_name}'")
                self.evaluated_group_members_by_coordinator[group_name].append(indigo_device)

        # ✅ Consolidated bonded device injection to ensure visibility in dump_groups_to_log()
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if not dev or "GROUP_Name" not in dev.states:
                continue

            group_name = dev.states.get("GROUP_Name")
            if (
                not group_name
                or group_name == "Unavailable"
                or group_name.startswith("RINCON")
            ):
                continue

            dev_id = dev.id
            dev_name_lower = dev.name.lower()

            # Identify bonded devices by name patterns
            is_bonded = any(x in dev_name_lower for x in ("left", "right", "sub", "surround"))
            if not is_bonded:
                continue

            # ✅ Ensure evaluated_group_members_by_coordinator[group_name] exists
            if group_name not in self.evaluated_group_members_by_coordinator:
                self.logger.debug(f"🧰 1st Creating missing evaluated_group_members_by_coordinator['{group_name}'] for bonded injection")
                self.evaluated_group_members_by_coordinator[group_name] = []

            # 🧠 Prevent duplicates in evaluated group member list
            if all(d.id != dev_id for d in self.evaluated_group_members_by_coordinator[group_name]):
                self.logger.debug(f"➕ 1st Injecting bonded device '{dev.name}' into evaluated group '{group_name}' (fallback)")
                self.evaluated_group_members_by_coordinator[group_name].append(dev)

            # ✅ Ensure zone_group_state_cache[group_name]['members'] exists
            if group_name not in self.zone_group_state_cache:
                self.logger.debug(f"🧰 2nd Creating missing zone_group_state_cache['{group_name}'] for bonded injection")
                self.zone_group_state_cache[group_name] = {"members": []}

            if dev_id not in self.zone_group_state_cache[group_name]["members"]:
                self.logger.debug(
                    f"➕ 2nd Injecting bonded device '{dev.name}' (ID {dev_id}) into zone_group_state_cache['{group_name}']['members'] for logging"
                )
                self.zone_group_state_cache[group_name]["members"].append(dev_id)

        # 🎯 Post-pass to align bonded Sub grouped flag with its coordinator
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if not dev or "sub" not in dev.name.lower():
                continue

            sub_group = dev.states.get("GROUP_Name", "")
            if not sub_group or sub_group == "Unavailable":
                continue

            # Attempt to find coordinator for this sub's group
            coordinator = None
            for member in self.evaluated_group_members_by_coordinator.get(sub_group, []):
                if member.states.get("GROUP_Coordinator", "false") == "true":
                    coordinator = member
                    break

            if not coordinator:
                self.logger.debug(f"⚠️ Could not find coordinator for Sub device '{dev.name}' in group '{sub_group}'")
                continue

            coord_grouped = coordinator.states.get("Grouped", "false")
            sub_grouped = dev.states.get("Grouped", "false")

            if sub_grouped != coord_grouped:
                self.logger.info(f"🔁 Syncing Sub '{dev.name}' Grouped flag → {coord_grouped} (match coordinator '{coordinator.name}')")
                self.updateStateOnServer(dev, "Grouped", coord_grouped)

        # ✅ 🔄 Final fix: post-pass to reassign group names and flags for bonded devices missing or showing raw RINCON names
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if not dev:
                continue

            name_lower = dev.name.lower()
            if not any(x in name_lower for x in ("left", "right", "sub", "surround")):
                continue

            group_name = dev.states.get("GROUP_Name", "")
            if not group_name or group_name.startswith("RINCON") or group_name == "Unavailable":
                # Try to infer from evaluated groups
                for eval_group, members in self.evaluated_group_members_by_coordinator.items():
                    for m in members:
                        if m.id == dev.id:
                            group_name = eval_group
                            break
                    if group_name != "" and not group_name.startswith("RINCON"):
                        break

                if not group_name or group_name.startswith("RINCON"):
                    #self.logger.warning(f"🔍 Could not infer clean group name for bonded device '{dev.name}' — skipping post-fix")
                    continue

                self.logger.info(f"🛠 Rewriting invalid or missing GROUP_Name for bonded '{dev.name}' → '{group_name}'")
                self.updateStateOnServer(dev, "GROUP_Name", group_name)

            # Align grouped flag with group coordinator
            coordinator = None
            for m in self.evaluated_group_members_by_coordinator.get(group_name, []):
                if m.states.get("GROUP_Coordinator", "false") == "true":
                    coordinator = m
                    break

            if not coordinator:
                self.logger.debug(f"⚠️ Could not resolve coordinator for bonded '{dev.name}' in group '{group_name}'")
                continue

            coord_grouped = coordinator.states.get("Grouped", "false")
            dev_grouped = dev.states.get("Grouped", "false")
            if dev_grouped != coord_grouped:
                self.logger.info(f"🔁 Syncing bonded '{dev.name}' Grouped flag → {coord_grouped} (match coordinator '{coordinator.name}')")
                self.updateStateOnServer(dev, "Grouped", coord_grouped)

            if dev.states.get("GROUP_Coordinator", "true") == "true":
                #self.logger.info(f"🔄 Setting bonded '{dev.name}' as non-coordinator")
                self.updateStateOnServer(dev, "GROUP_Coordinator", "false")












    def old_2_evaluate_and_update_grouped_states(self, dev=None):
        now = time.time()
        if hasattr(self, "_last_group_eval") and now - self._last_group_eval < 3.0:
            return
        self._last_group_eval = now

        # Initialize required custom states
        if dev:
            if dev is not None:
                self.logger.debug(f"⚙️ Evaluating group state for device: {dev.name}")
                self.initialize_custom_states(dev)
            else:
                self.logger.warning("🚫 Received 'None' for dev argument — skipping initialize_custom_states()")
        else:
            self.logger.debug("⚙️ Evaluating group state for all Sonos devices...")
            for d in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if d is not None:
                    self.initialize_custom_states(d)
                else:
                    self.logger.warning("🚫 Encountered None in device list — skipping.")

        bonded_names = ["sub"]
        seen_groups = set()

        self.logger.info("🔄 Evaluating current group states for all Sonos devices...")

        # 🧠 Reset evaluated group tracking cache
        self.evaluated_group_members_by_coordinator = {}

        for group_uid, group_data in self.zone_group_state_cache.items():
            coordinator_entry = group_data.get("coordinator")
            member_entries = group_data.get("members", [])

            self.logger.debug(f"🧪 Group ID: {group_uid} | Coordinator: {coordinator_entry} | Members: {len(member_entries)}")

            if group_uid in seen_groups:
                continue
            seen_groups.add(group_uid)

            coordinator_uuid = coordinator_entry.get("uuid") if isinstance(coordinator_entry, dict) else coordinator_entry
            coordinator = self.get_soco_by_uuid(coordinator_uuid)

            if not coordinator:
                self.logger.debug(f"⚠️ 2nd Could not resolve SoCo coordinator for UUID: {coordinator_uuid}")
                continue

            members = []
            for entry in member_entries:
                member_uuid = entry.get("uuid") if isinstance(entry, dict) else entry
                soco_dev = self.get_soco_by_uuid(member_uuid)
                if soco_dev:
                    members.append(soco_dev)
                else:
                    self.logger.debug(f"⚠️ Could not resolve SoCo device for UUID: {entry}")

            if not members:
                self.logger.warning(f"⚠️ Group {group_uid} has no resolvable members — skipping.")
                continue

            # 🔍 Evaluate non-bonded members
            non_bonded_members = [
                m for m in members
                if not any(b in m.player_name.lower() for b in bonded_names)
            ]
            unique_names = set(m.player_name.lower() for m in non_bonded_members)

            # ✅ Determine grouped status — TRUE only if more than one *non-bonded* member
            is_grouped = len(unique_names) > 1

            if not is_grouped:
                self.logger.debug(f"🧩 Not grouped: {coordinator.player_name} — fewer than 2 unique non-bonded members")

            group_name = coordinator.player_name if is_grouped else members[0].player_name

            # 🧠 Initialize tracking for this group
            if group_name not in self.evaluated_group_members_by_coordinator:
                self.logger.debug(f"📦 Initializing group entry for '{group_name}' in evaluated_group_members_by_coordinator")
                self.evaluated_group_members_by_coordinator[group_name] = []

            for member in members:
                member_ip = member.ip_address.strip()
                indigo_device = self.ip_to_indigo_device.get(member_ip)
                if not indigo_device:
                    self.logger.warning(f"⚠️ No Indigo device found for {member.player_name} ({member_ip}) — skipping")
                    continue

                if dev and dev.id != indigo_device.id:
                    self.logger.debug(f"⏭ Skipping {indigo_device.name} due to dev filter (looking for ID {dev.id})")
                    continue

                expected_grouped = "true" if is_grouped else "false"
                expected_coord = "true" if member == coordinator else "false"

                grouped_val = indigo_device.states.get("Grouped", "undefined")
                coord_val = indigo_device.states.get("GROUP_Coordinator", "undefined")
                name_val = indigo_device.states.get("GROUP_Name", "")

                # Update plugin-evaluated Grouped flag
                if str(grouped_val).lower() != expected_grouped:
                    self.logger.info(f"🆙 Updating 'Grouped' state for {indigo_device.name} → {expected_grouped}")
                    self.updateStateOnServer(indigo_device, "Grouped", expected_grouped)

                # Update plugin-evaluated coordinator flag
                if str(coord_val).lower() != expected_coord:
                    self.logger.info(f"🧭 Updating 'GROUP_Coordinator' state for {indigo_device.name} → {expected_coord}")
                    self.updateStateOnServer(indigo_device, "GROUP_Coordinator", expected_coord)

                # Explicit Group_Name update using indigo_device, not dev
                old_group_name = indigo_device.states.get("GROUP_Name", "Unavailable")
                if group_name != old_group_name:
                    caller = inspect.stack()[1].function
                    self.logger.debug(f"🧭 TRACE: Group_Name has changed — invoked from: {caller} — will write new value: {group_name}")
                    try:
                        indigo_device.updateStateOnServer("GROUP_Name", group_name)
                    except Exception as e:
                        self.logger.error(f"❌ Failed to write GROUP_Name='{group_name}' to {indigo_device.name}: {e}")

                # Fallback update if not already handled
                if "GROUP_Name" not in indigo_device.states:
                    self.logger.error(f"❌ Cannot update GROUP_Name for {indigo_device.name} — state key not defined!")
                elif group_name and group_name != name_val:
                    self.logger.info(f"🧩 Updating 'GROUP_Name' for {indigo_device.name} → '{group_name}' (previous: {name_val})")
                    self.updateStateOnServer(indigo_device, "GROUP_Name", group_name)

                # ✅ Add to plugin-evaluated group tracking dict
                self.logger.debug(f"✅ Adding {indigo_device.name} to evaluated group '{group_name}'")
                self.evaluated_group_members_by_coordinator[group_name].append(indigo_device)

        # ✅ Consolidated bonded device injection to ensure visibility in dump_groups_to_log()

        # ✅ Consolidated bonded device injection to ensure visibility in dump_groups_to_log()
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if not dev or "GROUP_Name" not in dev.states:
                continue

            group_name = dev.states.get("GROUP_Name")
            if (
                not group_name
                or group_name == "Unavailable"
                or group_name.startswith("RINCON")
            ):
                continue

            dev_id = dev.id
            dev_name_lower = dev.name.lower()

            # Identify bonded devices by name patterns
            is_bonded = any(x in dev_name_lower for x in ("left", "right", "sub", "surround"))
            if not is_bonded:
                continue

            # ✅ Ensure evaluated_group_members_by_coordinator[group_name] exists
            if group_name not in self.evaluated_group_members_by_coordinator:
                self.logger.warning(f"🧰 3rd Creating missing evaluated_group_members_by_coordinator['{group_name}'] for bonded injection")
                self.evaluated_group_members_by_coordinator[group_name] = []

            # 🧠 Prevent duplicates in evaluated group member list
            if all(d.id != dev_id for d in self.evaluated_group_members_by_coordinator[group_name]):
                self.logger.debug(f"➕ 3rd Injecting bonded device '{dev.name}' into evaluated group '{group_name}' (fallback)")
                self.evaluated_group_members_by_coordinator[group_name].append(dev)

            # ✅ Ensure zone_group_state_cache[group_name]['members'] exists
            if group_name not in self.zone_group_state_cache:
                self.logger.warning(f"🧰 4th Creating missing zone_group_state_cache['{group_name}'] for bonded injection")
                self.zone_group_state_cache[group_name] = {"members": []}

            if dev_id not in self.zone_group_state_cache[group_name]["members"]:
                self.logger.debug(
                    f"➕ 4th Injecting bonded device '{dev.name}' (ID {dev_id}) into zone_group_state_cache['{group_name}']['members'] for logging"
                )
                self.zone_group_state_cache[group_name]["members"].append(dev_id)

            # 🎯 Post-pass to align bonded Sub grouped flag with its coordinator
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if not dev or "sub" not in dev.name.lower():
                    continue

                sub_group = dev.states.get("GROUP_Name", "")
                if not sub_group or sub_group == "Unavailable":
                    continue

                # Attempt to find coordinator for this sub's group
                coordinator = None
                for member in self.evaluated_group_members_by_coordinator.get(sub_group, []):
                    if member.states.get("GROUP_Coordinator", "false") == "true":
                        coordinator = member
                        break

                if not coordinator:
                    self.logger.debug(f"⚠️ Could not find coordinator for Sub device '{dev.name}' in group '{sub_group}'")
                    continue

                coord_grouped = coordinator.states.get("Grouped", "false")
                sub_grouped = dev.states.get("Grouped", "false")

                if sub_grouped != coord_grouped:
                    self.logger.info(f"🔁 Syncing Sub '{dev.name}' Grouped flag → {coord_grouped} (match coordinator '{coordinator.name}')")
                    self.updateStateOnServer(dev, "Grouped", coord_grouped)



#################################################################################################
### End - Evaluate_and_update_grouped_states
#################################################################################################



    def saved_patio_working_evaluate_and_update_grouped_states(self, dev=None):
        now = time.time()
        if hasattr(self, "_last_group_eval") and now - self._last_group_eval < 3.0:
            return
        self._last_group_eval = now

        # Initialize required custom states
        if dev:
            if dev is not None:
                self.logger.debug(f"⚙️ Evaluating group state for device: {dev.name}")
                self.initialize_custom_states(dev)
            else:
                self.logger.warning("🚫 Received 'None' for dev argument — skipping initialize_custom_states()")
        else:
            self.logger.debug("⚙️ Evaluating group state for all Sonos devices...")
            for d in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if d is not None:
                    self.initialize_custom_states(d)
                else:
                    self.logger.warning("🚫 Encountered None in device list — skipping.")

        bonded_names = ["sub"]
        seen_groups = set()

        self.logger.info("🔄 Evaluating current group states for all Sonos devices...")

        # 🧠 Reset evaluated group tracking cache
        self.evaluated_group_members_by_coordinator = {}

        for group_uid, group_data in self.zone_group_state_cache.items():
            coordinator_entry = group_data.get("coordinator")
            member_entries = group_data.get("members", [])

            self.logger.debug(f"🧪 Group ID: {group_uid} | Coordinator: {coordinator_entry} | Members: {len(member_entries)}")

            if group_uid in seen_groups:
                continue
            seen_groups.add(group_uid)

            coordinator_uuid = coordinator_entry.get("uuid") if isinstance(coordinator_entry, dict) else coordinator_entry
            coordinator = self.get_soco_by_uuid(coordinator_uuid)

            if not coordinator:
                self.logger.debug(f"⚠️ 3rd Could not resolve SoCo coordinator for UUID: {coordinator_uuid}")
                continue

            members = []
            for entry in member_entries:
                member_uuid = entry.get("uuid") if isinstance(entry, dict) else entry
                soco_dev = self.get_soco_by_uuid(member_uuid)
                if soco_dev:
                    members.append(soco_dev)
                else:
                    self.logger.debug(f"⚠️ Could not resolve SoCo device for UUID: {entry}")

            if not members:
                self.logger.warning(f"⚠️ Group {group_uid} has no resolvable members — skipping.")
                continue

            # 🔍 Evaluate non-bonded members
            non_bonded_members = [
                m for m in members
                if not any(b in m.player_name.lower() for b in bonded_names)
            ]
            unique_names = set(m.player_name.lower() for m in non_bonded_members)

            # ✅ Determine grouped status — TRUE only if more than one *non-bonded* member
            is_grouped = len(unique_names) > 1

            if not is_grouped:
                self.logger.debug(f"🧩 Not grouped: {coordinator.player_name} — fewer than 2 unique non-bonded members")

            group_name = coordinator.player_name if is_grouped else members[0].player_name

            # 🧠 Initialize tracking for this group
            if group_name not in self.evaluated_group_members_by_coordinator:
                self.logger.debug(f"📦 Initializing group entry for '{group_name}' in evaluated_group_members_by_coordinator")
                self.evaluated_group_members_by_coordinator[group_name] = []

            for member in members:
                member_ip = member.ip_address.strip()
                indigo_device = self.ip_to_indigo_device.get(member_ip)
                if not indigo_device:
                    self.logger.warning(f"⚠️ No Indigo device found for {member.player_name} ({member_ip}) — skipping")
                    continue

                if dev and dev.id != indigo_device.id:
                    self.logger.debug(f"⏭ Skipping {indigo_device.name} due to dev filter (looking for ID {dev.id})")
                    continue

                expected_grouped = "true" if is_grouped else "false"
                expected_coord = "true" if member == coordinator else "false"

                grouped_val = indigo_device.states.get("Grouped", "undefined")
                coord_val = indigo_device.states.get("GROUP_Coordinator", "undefined")
                name_val = indigo_device.states.get("GROUP_Name", "")

                # Update plugin-evaluated Grouped flag
                if str(grouped_val).lower() != expected_grouped:
                    self.logger.info(f"🆙 Updating 'Grouped' state for {indigo_device.name} → {expected_grouped}")
                    self.updateStateOnServer(indigo_device, "Grouped", expected_grouped)

                # Update plugin-evaluated coordinator flag
                if str(coord_val).lower() != expected_coord:
                    self.logger.info(f"🧭 Updating 'GROUP_Coordinator' state for {indigo_device.name} → {expected_coord}")
                    self.updateStateOnServer(indigo_device, "GROUP_Coordinator", expected_coord)

                # Explicit Group_Name update using indigo_device, not dev
                old_group_name = indigo_device.states.get("GROUP_Name", "Unavailable")
                if group_name != old_group_name:
                    caller = inspect.stack()[1].function
                    self.logger.debug(f"🧭 TRACE: Group_Name has changed — invoked from: {caller} — will write new value: {group_name}")
                    try:
                        indigo_device.updateStateOnServer("GROUP_Name", group_name)
                    except Exception as e:
                        self.logger.error(f"❌ Failed to write GROUP_Name='{group_name}' to {indigo_device.name}: {e}")

                # Fallback update if not already handled
                if "GROUP_Name" not in indigo_device.states:
                    self.logger.error(f"❌ Cannot update GROUP_Name for {indigo_device.name} — state key not defined!")
                elif group_name and group_name != name_val:
                    self.logger.info(f"🧩 Updating 'GROUP_Name' for {indigo_device.name} → '{group_name}' (previous: {name_val})")
                    self.updateStateOnServer(indigo_device, "GROUP_Name", group_name)

                # ✅ Add to plugin-evaluated group tracking dict
                self.logger.debug(f"✅ Adding {indigo_device.name} to evaluated group '{group_name}'")
                self.evaluated_group_members_by_coordinator[group_name].append(indigo_device)




                    

    def refresh_group_topology_after_plugin_zone_change(self):
        #self.logger.warning("🔁 Manually refreshing group topology after plugin-initiated zone change...")

        try:
            import http.client as httplib
            import xml.etree.ElementTree as ET

            def get_zone_group_state_from_player(ip):
                try:
                    conn = httplib.HTTPConnection(ip, 1400, timeout=5)
                    conn.request("GET", "/status/zp")
                    response = conn.getresponse()
                    if response.status == 200:
                        return response.read()
                    else:
                        self.logger.warning(f"⚠️ Failed HTTP ZGT fetch from {ip}: status {response.status}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Exception fetching ZGT from {ip}: {e}")
                return None

            def parse_zone_group_state(xml_data):
                groups = {}
                try:
                    if isinstance(xml_data, bytes):
                        xml_data = xml_data.decode("utf-8", errors="ignore")
                    elif not isinstance(xml_data, str):
                        xml_data = str(xml_data)

                    xml_data = xml_data.strip()
                    if not xml_data.startswith("<"):
                        raise ValueError("XML does not start with expected '<'")

                    #self.logger.warning("🛠 ENTERED parse_zone_group_state()")
                    #self.logger.warning(f"📨 Incoming XML data length: {len(xml_data)}")
                    #self.logger.warning(f"🔎 First 200 chars: {xml_data[:200]}")

                    root = ET.fromstring(xml_data)
                    for group in root.findall(".//ZoneGroup"):
                        group_id = group.get("ID")
                        coordinator_uuid = group.get("Coordinator")
                        members = []

                        for member in group.findall("ZoneGroupMember"):
                            zone_name = member.get("ZoneName", "").strip().lower()
                            uuid = member.get("UUID", "").strip()
                            location = member.get("Location", "").strip()

                            if zone_name == "sub":
                                #self.logger.warning(f"🚫 Skipping bonded sub: {zone_name}")
                                continue

                            members.append({
                                "uuid": uuid,
                                "location": location,
                                "zone_name": zone_name,
                            })

                        groups[group_id] = {
                            "coordinator": coordinator_uuid,
                            "members": members,
                        }

                    #self.logger.warning(f"🧪 Parsed {len(groups)} group(s) from XML.")
                except Exception as e:
                    self.logger.error(f"❌ XML parse error in zone group topology: {e}")
                return groups

            #for ip in self.soco_by_ip.keys():
            for ip in list(self.soco_by_ip.keys()):                
                raw_xml = get_zone_group_state_from_player(ip)
                if raw_xml:
                    parsed = parse_zone_group_state(raw_xml)
                    if parsed:
                        self.zone_group_state_cache = parsed
                        self.logger.info(f"💾 zone_group_state_cache updated with {len(parsed)} group(s)")
                        break

            # 🔄 Rebuild critical mappings before group state evaluation
            if hasattr(self, "rebuild_ip_to_device_map"):
                self.rebuild_ip_to_device_map()
            if hasattr(self, "rebuild_uuid_maps_from_soco"):
                self.rebuild_uuid_maps_from_soco()
                self.logger.warning(f"📌 DEBUG: uuid_to_indigo_device now contains {len(self.uuid_to_indigo_device)} entries")

            #self.logger.info("📣 Calling evaluate_and_update_grouped_states() after ZoneGroupTopology change...")
            self.evaluate_and_update_grouped_states()

        except Exception as e:
            self.logger.error(f"❌ Exception in refresh_group_topology_after_plugin_zone_change: {e}")











    def refresh_group_membership(self, indigo_device, soco_device):
        try:
            group = soco_device.group
            coordinator = group.coordinator
            devices_in_group = group.members

            coordinator_ip = coordinator.ip_address.strip()
            is_coordinator = (coordinator_ip == indigo_device.address.strip())
            #self.trace_me(indigo_device)
            current_group_name = coordinator.player_name or ""

            # Update coordinator and group name state
            indigo_device.updateStateOnServer("GROUP_Coordinator", str(is_coordinator).lower())
            indigo_device.updateStateOnServer("GROUP_Name", current_group_name)
            self.safe_debug(f"🔄 Updated {indigo_device.name} → GROUP_Coordinator: {is_coordinator}, GROUP_Name: {current_group_name}")

            # === Centralized album art handling ===
            try:
                if indigo_device:
                    self.update_album_artwork(dev=indigo_device, zone_ip=indigo_device.address.strip())
                else:
                    self.logger.warning("⚠️ Skipping artwork update — Indigo device is undefined")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to update album artwork for {indigo_device.name if indigo_device else 'Unknown'}: {e}")

            # === Playback state refresh for coordinator ===
            if is_coordinator:
                current_track_info = soco_device.get_current_track_info()
                transport_info = soco_device.get_current_transport_info()

                zp_state = transport_info.get('current_transport_state', 'STOPPED').upper()
                current_track_uri = current_track_info.get('uri', '')
                current_title = current_track_info.get('title', '')
                current_artist = current_track_info.get('artist', '')
                current_creator = current_track_info.get('creator', '')                

                indigo_device.updateStateOnServer("ZP_STATE", zp_state)
                indigo_device.updateStateOnServer("ZP_TRACK", current_title or "")
                indigo_device.updateStateOnServer("ZP_ARTIST", current_artist or "")
                indigo_device.updateStateOnServer("ZP_CREATOR", current_creator or "")                
                indigo_device.updateStateOnServer("ZP_CurrentTrackURI", current_track_uri or "")

                # Derive and update ZP_SOURCE
                try:
                    source = self.determineSource(indigo_device, soco_device, transport_info, current_track_info)
                    indigo_device.updateStateOnServer("ZP_SOURCE", source)
                    self.safe_debug(f"🛰️ Set {indigo_device.name} ZP_SOURCE → {source}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to determine ZP_SOURCE for {indigo_device.name}: {e}")

                self.safe_debug(f"🔄 Refreshed standalone states for {indigo_device.name} → State: {zp_state}, Track: {current_title}, Artist: {current_artist}")

            else:
                # === Sync slave states from coordinator device ===
                master_dev = next(
                    (dev for dev in indigo.devices if dev.address.strip() == coordinator_ip),
                    None
                )

                if master_dev:
                    for state_key in ["ZP_STATE", "ZP_TRACK", "ZP_ARTIST", "ZP_CREATOR", "ZP_SOURCE", "ZP_MUTE","ZP_CurrentTrackURI", "ZP_ART"]:
                        master_value = master_dev.states.get(state_key, "")
                        indigo_device.updateStateOnServer(state_key, master_value)
                        self.safe_debug(f"🔄 Synced slave {indigo_device.name} {state_key} → {master_value}")
                else:
                    self.logger.warning(f"⚠️ Could not find master device {coordinator_ip} to sync states for slave {indigo_device.name}")

        except Exception as e:
            self.logger.error(f"❌ Exception in refresh_group_membership for {indigo_device.name}: {e}")


    def determineSource(self, indigo_device, soco_device, transport_info, track_info):
        try:
            uri = track_info.get("uri", "") or ""
            if "x-sonosapi-stream" in uri:
                return "SiriusXM"
            elif "pandora.com" in uri:
                return "Pandora"
            elif "spotify" in uri:
                return "Spotify"
            elif "tunein" in uri:
                return "TuneIn"
            elif "airplay" in uri:
                return "AirPlay"
            elif uri.startswith("x-rincon-mp3radio:"):
                return "Internet Radio"
            elif uri.startswith("x-rincon-queue:"):
                return "Queue"
            else:
                return "Unknown"
        except Exception as e:
            self.logger.warning(f"⚠️ determineSource failed for {indigo_device.name}: {e}")
            return "Unknown"












    def getIndigoDeviceFromEvent(self, event_obj):
        sid = getattr(event_obj, "sid", "")
        for dev_id, subs in self.soco_subs.items():
            if any(sub.sid == sid for sub in subs.values()):
                return indigo.devices[int(dev_id)]
        return None




    def update_album_artwork(self, event_obj=None, dev=None, zone_ip=None):
        import requests, shutil, io, filecmp, time
        from PIL import Image

        ARTWORK_FOLDER = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        DEFAULT_ART_PATH = ARTWORK_FOLDER + "default_artwork.jpg"
        DEFAULT_ART_SRC = "/Library/Application Support/Perceptive Automation/Indigo 2024.2/Plugins/Sonos.indigoPlugin/Contents/Server Plugin/default_artwork.jpg"
        MAX_DOWNLOAD_ATTEMPTS = 3

        os.makedirs(ARTWORK_FOLDER, exist_ok=True)
        if not os.path.exists(DEFAULT_ART_PATH):
            try:
                shutil.copy(DEFAULT_ART_SRC, DEFAULT_ART_PATH)
                self.logger.info(f"✅ Default artwork copied to {DEFAULT_ART_PATH}")
            except Exception as e:
                self.logger.error(f"❌ Failed to copy default artwork: {e}")
                return

        # ✅ Step 1: Infer zone_ip from dev if not provided
        if not zone_ip and dev:
            try:
                zone_ip = dev.address.strip()
                if not zone_ip:
                    self.logger.warning(f"⚠️ dev.address is empty for {dev.name}")
                    zone_ip = None
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to extract IP from dev: {e}")
                zone_ip = None

        # ✅ Step 2: Try resolving zone_ip from event if not yet available
        if not zone_ip and event_obj:
            zone_ip = getattr(getattr(event_obj, "soco", None), "ip_address", None)

        # ✅ Step 3: Infer dev from event if not passed
        if not dev and event_obj:
            dev = self.getIndigoDeviceFromEvent(event_obj)

        # 🚫 Final guard: require both dev and zone_ip
        if not dev or not zone_ip:
            self.logger.debug(f"⚠️ Could not resolve device or IP for album art update — dev: {getattr(dev, 'name', '?')} | zone_ip: {zone_ip}")
            return

        self.logger.debug(f"🎯 Art update entry → dev={dev}, zone_ip={zone_ip}, event_meta={getattr(event_obj, 'variables', {}).get('current_track_meta_data', None)}")

        # ✅ Step 4: Locate SoCo device and group info
        soco_device = self.getSoCoDeviceByIP(zone_ip)
        if not soco_device:
            self.logger.warning(f"⚠️ No SoCo device found for IP {zone_ip}")
            return

        try:
            group = soco_device.group
            coordinator = group.coordinator
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to access group or coordinator for {zone_ip}: {e}")
            return

        is_master = (coordinator.ip_address.strip() == zone_ip)
        coordinator_dev = self.ip_to_indigo_device.get(coordinator.ip_address.strip())

        master_artwork_path = f"{ARTWORK_FOLDER}sonos_art_{coordinator.ip_address}.jpg"
        art_url = None

        # === Coordinator logic: fetch and save artwork ===
        if is_master and event_obj:
            meta = event_obj.variables.get("current_track_meta_data", None)
            album_art_uri = getattr(meta, "album_art_uri", "") if meta else ""

            if album_art_uri.startswith("/"):
                album_art_uri = f"http://{zone_ip}:1400{album_art_uri}"

            if album_art_uri:
                for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
                    try:
                        self.logger.debug(f"🎨 Attempting album art fetch from {album_art_uri} (attempt {attempt})")
                        response = requests.get(album_art_uri, timeout=5)
                        if response.status_code == 200:
                            image = Image.open(io.BytesIO(response.content))
                            image.thumbnail((500, 500))
                            image = image.convert("RGB")
                            image.save(master_artwork_path, format="JPEG", quality=75)
                            art_url = f"http://localhost:8888/sonos_art_{coordinator.ip_address}.jpg"
                            #self.logger.info(f"🖼️ Coordinator Album art saved for {coordinator.player_name}")
                            break
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to fetch album art: {e}")
                        time.sleep(0.5)

            if not os.path.exists(master_artwork_path):
                shutil.copyfile(DEFAULT_ART_PATH, master_artwork_path)
                art_url = f"http://localhost:8888/default_artwork.jpg"
                self.logger.info("🖼️ Used default artwork due to fetch failure")

            if coordinator_dev:
                coordinator_dev.updateStateOnServer("ZP_ART", art_url)

        # 🛡️ Prevent slave copy if coordinator is not grouped
        if not coordinator_dev or coordinator_dev.states.get("Grouped", "false") != "true":
            self.logger.debug(f"⛔ Skipping artwork propagation — {coordinator_dev.name if coordinator_dev else 'Unknown'} is not grouped")
            return

        # === Slave devices: copy master art ===
        for member in group.members:
            member_ip = member.ip_address.strip()
            if member_ip == coordinator.ip_address.strip():
                continue

            slave_dev = self.ip_to_indigo_device.get(member_ip)
            if not slave_dev:
                self.logger.warning(f"⚠️ No Indigo device for slave {member.player_name} ({member_ip})")
                continue

            slave_art_path = f"{ARTWORK_FOLDER}sonos_art_{member_ip}.jpg"
            try:
                if not os.path.exists(slave_art_path) or not filecmp.cmp(master_artwork_path, slave_art_path, shallow=False):
                    shutil.copyfile(master_artwork_path, slave_art_path)
                    self.logger.info(f"🖼️ Copied artwork to slave {slave_dev.name}")
            except Exception as e:
                self.logger.error(f"❌ Failed copying art to {slave_dev.name}: {e}")
                slave_art_path = DEFAULT_ART_PATH

            slave_dev.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{member_ip}.jpg")

        # === Standalone player handling if no event and not a coordinator ===
        if not is_master and not event_obj:
            dev.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{zone_ip}.jpg")

        
    def updateStateOnServer(self, dev, state, value):
        if state not in dev.states:
            self.plugin.logger.error(f"❌ Tried to update undefined state '{state}' on device '{dev.name}'")
            return

        if self.plugin.stateUpdatesDebug:
            self.plugin.debugLog(u"\t Updating Device: %s, State: %s, Value: %s" % (dev.name, state, value))

        GROUP_Coordinator = dev.states.get('GROUP_Coordinator', "false")
        if GROUP_Coordinator == "false" and state in ZoneGroupStates:
            return

        # Encode and update
        val = "" if value in [None, "None"] else value.encode('utf-8')
        dev.updateStateOnServer(state, val)

        # 🧠 Store in internal dict for reliable GROUP_Name tracking
        if state == "GROUP_Name":
            if hasattr(self.plugin, "group_name_by_device_id"):
                self.plugin.group_name_by_device_id[dev.id] = val
            else:
                self.plugin.logger.debug(f"⚠️ GROUP_Name fallback cache not initialized for device '{dev.name}'")


        # 🔍 Post-write verification (re-fetch the device from Indigo to confirm persistence)
        try:
            refreshed = indigo.devices[dev.id]
            confirmed_val = refreshed.states.get(state, "<missing>")
            #self.plugin.logger.info(f"🧪 POST-WRITE REFETCH: {refreshed.name} {state} = {confirmed_val}")
        except Exception as e:
            self.plugin.logger.warning(f"⚠️ Post-write re-fetch failed for {dev.name}: {e}")

        # Propagate to slaves
        if (
            state in ZoneGroupStates and
            GROUP_Coordinator == "true" and
            dev.states.get('ZonePlayerUUIDsInGroup', "").find(",") != -1
        ):

            self.plugin.debugLog("Replicate state to slave ZonePlayers...")

            # Normalize zone_list into list of strings
            try:
                if zone_list is None:
                    ZonePlayerUUIDsInGroup = []
                elif isinstance(zone_list, str):
                    ZonePlayerUUIDsInGroup = zone_list.split(",")
                elif isinstance(zone_list, list):
                    ZonePlayerUUIDsInGroup = [str(uid) for uid in zone_list]
                elif isinstance(zone_list, int):
                    ZonePlayerUUIDsInGroup = [str(zone_list)]
                else:
                    self.plugin.logger.error(f"❌ Unexpected type for zone_list: {type(zone_list).__name__}")
                    ZonePlayerUUIDsInGroup = []
            except Exception as e:
                self.plugin.logger.error(f"❌ Failed to parse ZonePlayerUUIDsInGroup from zone_list={zone_list} — {e}")
                ZonePlayerUUIDsInGroup = []

            # Proceed with update
            for rdev in indigo.devices.iter("self.ZonePlayer"):
                SlaveUID = rdev.states.get('ZP_LocalUID')
                if (
                    SlaveUID != dev.states['ZP_LocalUID']
                    and rdev.states.get('GROUP_Coordinator') == "false"
                    and SlaveUID in ZonePlayerUUIDsInGroup
                ):
                    slave_val = "" if value in [None, "None"] else value.encode('utf-8')
                    if state == "ZP_CurrentURI":
                        slave_val = uri_group + dev.states['ZP_LocalUID']
                    if self.plugin.stateUpdatesDebug:
                        self.plugin.debugLog(u"\t Updating Device: %s, State: %s, Value: %s" % (rdev.name, state, slave_val))
                    rdev.updateStateOnServer(state, slave_val)












    def updateStateOnSlaves(self, dev):
            self.plugin.debugLog("Update all states to slave ZonePlayers...")
            ZonePlayerUUIDsInGroup = dev.states['ZonePlayerUUIDsInGroup']
            for rdev in indigo.devices.iter("self.ZonePlayer"):
                SlaveUID = rdev.states['ZP_LocalUID']
                GROUP_Coordinator = rdev.states['GROUP_Coordinator']
                # Do not update if you are yourself, not a slave, and not in the group
                if SlaveUID != dev.states['ZP_LocalUID'] and GROUP_Coordinator == "false" and SlaveUID in ZonePlayerUUIDsInGroup:
                    for state in list(ZoneGroupStates):
                        if state == "ZP_CurrentURI":
                            value = uri_group + dev.states['ZP_LocalUID']
                        else:
                            value = dev.states[state]
                        if self.plugin.stateUpdatesDebug:
                            self.plugin.debugLog(u"\t Updating Slave Device: %s, State: %s, Value: %s" % (rdev.name, state, value))
                        rdev.updateStateOnServer(state, value)
                    rdev.updateStateOnServer("ZP_ART", dev.states['ZP_ART'])
                    try:
                        shutil.copy2("/Library/Application Support/Perceptive Automation/images/Sonos/"+dev.states['ZP_ZoneName']+"_art.jpg", \
                            "/Library/Application Support/Perceptive Automation/images/Sonos/"+rdev.states['ZP_ZoneName']+"_art.jpg")
                    except:
                        pass

    def copyStateFromMaster(self, dev):
        self.plugin.debugLog("Copy states from master ZonePlayer...")

        group_name = dev.states.get("GROUP_Name", "")
        if not isinstance(group_name, str):
            self.logger.error(f"❌ GROUP_Name is not a string: {group_name!r} (type: {type(group_name).__name__})")
            return

        if ":" not in group_name:
            self.logger.error(f"❌ GROUP_Name is malformed (no ':'): {group_name!r}")
            return

        try:
            MasterUID, x = group_name.split(":")
        except Exception as e:
            self.logger.error(f"❌ Failed to split GROUP_Name '{group_name}': {e}")
            return

        for mdev in indigo.devices.iter("self.ZonePlayer"):
            if mdev.states['ZP_LocalUID'] == MasterUID:
                for state in list(ZoneGroupStates):
                    if state == "ZP_CurrentURI":
                        value = uri_group + mdev.states['ZP_LocalUID']
                    else:
                        value = mdev.states[state]
                    if self.plugin.stateUpdatesDebug:
                        self.plugin.debugLog(u"\t Updating Slave Device: %s, State: %s, Value: %s" % (dev.name, state, value))
                    dev.updateStateOnServer(state, value)

                dev.updateStateOnServer("ZP_ART", mdev.states['ZP_ART'])

                try:
                    shutil.copy2(
                        f"/Library/Application Support/Perceptive Automation/images/Sonos/{mdev.states['ZP_ZoneName']}_art.jpg",
                        f"/Library/Application Support/Perceptive Automation/images/Sonos/{dev.states['ZP_ZoneName']}_art.jpg"
                    )
                except Exception as e:
                    self.logger.warning(f"⚠️ Artwork copy failed: {e}")






# Check for messages
    #def initZones(self, dev):
    def initZones(self, dev, soco_device=None):        
        MyzonePlayerID='120169368'
        zoneIP = dev.pluginProps["address"]
        self.plugin.debugLog(u"Resetting States for zone: %s" % zoneIP)
        self.updateStateOnServer (dev, "ZP_ALBUM", "")
        self.updateStateOnServer (dev, "ZP_ART", "")
        self.updateStateOnServer (dev, "ZP_ARTIST", "")
        self.updateStateOnServer (dev, "ZP_SOURCE", "")        
        self.updateStateOnServer (dev, "ZP_CREATOR", "")
        self.updateStateOnServer (dev, "ZP_CurrentURI", "")
        self.updateStateOnServer (dev, "ZP_DURATION", "")
        self.updateStateOnServer (dev, "ZP_RELATIVE", "")
        self.updateStateOnServer (dev, "ZP_INFO", "")
        self.updateStateOnServer (dev, "ZP_MUTE", "")
        self.updateStateOnServer (dev, "ZP_STATE", "")
        self.updateStateOnServer (dev, "ZP_STATION", "")
        self.updateStateOnServer (dev, "ZP_TRACK", "")
        self.updateStateOnServer (dev, "ZP_VOLUME", "")
        self.updateStateOnServer (dev, "ZP_VOLUME_FIXED", "")
        self.updateStateOnServer (dev, "ZP_BASS", "")
        self.updateStateOnServer (dev, "ZP_TREBLE", "")
        self.updateStateOnServer (dev, "ZP_ZoneName", "")
        self.updateStateOnServer (dev, "ZP_LocalUID", "")
        self.updateStateOnServer (dev, "ZP_AIName", "")
        self.updateStateOnServer (dev, "ZP_AIPath", "")
        self.updateStateOnServer (dev, "ZP_NALBUM", "")
        self.updateStateOnServer (dev, "ZP_NART", "")
        self.updateStateOnServer (dev, "ZP_NARTIST", "")
        self.updateStateOnServer (dev, "ZP_NCREATOR", "")       
        self.updateStateOnServer (dev, "ZP_NTRACK", "")
        self.updateStateOnServer (dev, "Q_Crossfade", "off")
        self.updateStateOnServer (dev, "Q_Repeat", "off")
        self.updateStateOnServer (dev, "Q_RepeatOne", "off")
        self.updateStateOnServer (dev, "Q_Shuffle", "off")
        self.updateStateOnServer (dev, "Q_Number", "0")
        self.updateStateOnServer (dev, "Q_ObjectID", "")
        self.updateStateOnServer (dev, "GROUP_Coordinator", "")
        self.updateStateOnServer (dev, "GROUP_Name", "")
        self.updateStateOnServer (dev, "ZP_CurrentTrack", "")
        self.updateStateOnServer (dev, "ZP_CurrentTrackURI", "")
        self.updateStateOnServer (dev, "ZoneGroupID", "")
        self.updateStateOnServer (dev, "ZoneGroupName", "")
        self.updateStateOnServer (dev, "ZonePlayerUUIDsInGroup", "")
        self.updateStateOnServer (dev, "alive", "")
        self.updateStateOnServer (dev, "bootseq", "")

        url = u"http://" + zoneIP + ":1400/status/zp"
        try:
            response = requests.get(url)
            root = ET.fromstring(response.content)
            ZoneName = root.findtext('.//ZoneName')
            LocalUID = root.findtext('.//LocalUID')
            #SerialNumber = '5C-AA-FD-5B-5C-D6:4'
            MyzonePlayerID='120169368'
            SerialNumber = root.findtext('.//SerialNumber')
        except:
            self.plugin.errorLog("Error getting ZonePlayer data: %s" % url)
            self.plugin.errorLog("  Offending ZonePlayer: %s" % dev.name)
            self.plugin.errorLog("  ZonePlayer may be physically turned off or in a bad state.")
            self.plugin.errorLog("  Please disable communications or remove from Indigo.")
            self.deviceList.remove(dev.id)
            dev.setErrorStateOnServer(u"error")
            return

        #self.updateStateOnServer (dev, "ZP_ZoneName", ZPInfo.findtext('ZoneName').decode('utf-8'))
        # Allow for special characters in ZoneName
        self.updateStateOnServer (dev, "ZP_ZoneName", ZoneName)
        self.updateStateOnServer (dev, "ZP_LocalUID", LocalUID)
        self.updateStateOnServer (dev, "SerialNumber", SerialNumber)

        self.getModelName (dev)

        self.updateZoneGroupStates (dev)
        self.updateZoneTopology (dev)

        indigo.server.log ("Adding ZonePlayer: %s, %s, %s" % (zoneIP, LocalUID, dev.name))
        self.ZonePlayers.append (LocalUID)
        if hasattr(dev, "pluginProps"):
            self.ZPTypes.append([LocalUID, dict(dev.pluginProps).get("model", "")])
        else:
            self.logger.warning(f"⚠️ Skipping pluginProps access — dev is not an Indigo device (type: {type(dev)})")

        self.zonePlayerState[dev.id] = {'zonePlayerAlive':True}
        self.updateStateOnServer (dev, "alive", time.asctime())

        if self.EventProcessor == "SoCo":
            self.socoSubscribe(dev, soco_device)


    def getModelName(self, dev):
        url = u"http://" + dev.pluginProps["address"] + ":1400/xml/device_description.xml"
        response = requests.get(url)
        if response.ok:
            root = ET.fromstring(response.content)
            ModelName = root.findtext('.//{urn:schemas-upnp-org:device-1-0}displayName')
            self.updateStateOnServer (dev, "ModelName", ModelName)
        else:
            self.plugin.errorLog("[%s] Cannot get ModelName for ZonePlayer: %s" % (time.asctime(), dev.name))




    def updateZoneTopology(self, dev):
        # Deprecated in Sonos 10.1
        #url = u"http://" + dev.pluginProps["address"] + ":1400/status/topology"
        #response = requests.get(url)
        #if response.ok:
        #   root = ET.fromstring(response.content)
        #   for ZonePlayer in root.findall("./ZonePlayers/ZonePlayer"):
        #       if ZonePlayer.get('uuid') == dev.states['ZP_LocalUID']:
        #           self.updateStateOnServer (dev, "GROUP_Coordinator", ZonePlayer.get('coordinator'))
        #           self.updateStateOnServer (dev, "bootseq", ZonePlayer.get('bootseq'))
        #else:
        #   self.plugin.errorLog("[%s] Cannot get ZoneGroupTopology for ZonePlayer: %s" % (time.asctime(), dev.name))

        res = self.restoreString(self.SOAPSend (self.rootZPIP, "/ZonePlayer", "/ZoneGroupTopology", "GetZoneGroupState", ""),1)
        ZGS = ET.fromstring(res)
        for ZoneGroup in ZGS.findall('.//ZoneGroup'):
            for ZonePlayer in ZoneGroup.findall('.//ZoneGroupMember'):
                if ZonePlayer.attrib['UUID'] == dev.states['ZP_LocalUID']:
                    if ZonePlayer.attrib['UUID'] == ZoneGroup.attrib['Coordinator']:
                        self.updateStateOnServer (dev, "GROUP_Coordinator", 'true')
                    else:
                        self.updateStateOnServer (dev, "GROUP_Coordinator", 'false')
                    #self.trace_me()
                    self.updateStateOnServer (dev, "GROUP_Name", ZoneGroup.attrib['ID'])                
                    self.updateStateOnServer (dev, "bootseq", ZonePlayer.attrib['BootSeq'])
 

    def updateZoneGroupStates(self, dev):
        zoneIP = dev.pluginProps["address"]
        res = self.SOAPSend(zoneIP, "/ZonePlayer", "/ZoneGroupTopology", "GetZoneGroupAttributes", "")

        # ✅ Removed .decode('utf-8') – not needed in Python 3
        self.updateStateOnServer(dev, "ZoneGroupName", self.parseCurrentZoneGroupName(res))
        self.updateStateOnServer(dev, "ZoneGroupID", self.parseCurrentZoneGroupID(res))
        self.updateStateOnServer(dev, "ZonePlayerUUIDsInGroup", self.parseCurrentZonePlayerUUIDsInGroup(res))


    def parsePoint (self, res, startString, stopString):
        loc = str(res).find(startString)
        if (loc > 0):
            loc_beg = loc + len(startString)
            loc_end = str(res).find(stopString, loc_beg)
            return (self.restoreString(str(res)[loc_beg:loc_end],0))
        else:
            return ""

    def parseDirty (self, res, startString, stopString):
        loc = str(res).find(startString)
        if (loc > 0):
            loc_beg = loc + len(startString)
            loc_end = str(res).find(stopString, loc_beg)
            return (str(res)[loc_beg:loc_end])
        else:
            return ""
    
    def parseFirstTrackNumberEnqueued(self, deviceId, res):
        loc = str(res).find("<FirstTrackNumberEnqueued>")
        if (loc > 0):
            loc_beg = loc + len("<FirstTrackNumberEnqueued>")
            loc_end = str(res).find("</FirstTrackNumberEnqueued>", loc_beg)
            item = self.restoreString(str(res)[loc_beg:loc_end],0)
            return item

    def parseRelTime(self, deviceId, res):
        return self.parsePoint (res, "<RelTime>", "</RelTime>")

    def parseCurrentZoneGroupName(self, res):
        return self.parsePoint (res, "<CurrentZoneGroupName>", "</CurrentZoneGroupName>")

    def parseCurrentZoneGroupID(self, res):
        return self.parsePoint (res, "<CurrentZoneGroupID>", "</CurrentZoneGroupID>")

    def parseCurrentZonePlayerUUIDsInGroup(self, res):
        return self.parsePoint (res, "<CurrentZonePlayerUUIDsInGroup>", "</CurrentZonePlayerUUIDsInGroup>")

    def parseCurrentVolume(self, res):
        return self.parsePoint (res, "<CurrentVolume>", "</CurrentVolume>")

    def parseCurrentMute(self, res):
        return self.parsePoint (res, "<CurrentMute>", "</CurrentMute>")

    def parseCurrentTransportActions(self, res):
        return self.parsePoint (res, "<Actions>", "</Actions>")

    def parseErrorCode(self, res):
        return self.parsePoint (res, "<errorCode>", "</errorCode>")

    def parseBrowseNumberReturned(self, res):
        return self.parsePoint (res, "<NumberReturned>", "</NumberReturned>")

    def parseAssignedObjectID(self, res):
        return self.parsePoint (res, "<AssignedObjectID>", "</AssignedObjectID>")

    def parsePandoraToken(self, res):
        return self.parsePoint (res, "&m=", "&f")

    def playRadio(self, zoneIP, l2p):
        self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+l2p+"</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"-1\" parentID=\"-1\" restricted=\"true\"&gt;&lt;dc:title&gt;RADIO&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON65031_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
        self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")






    def updateGroupPlaybackStates(self, coordinator_dev):
        """
        Runtime method: Propagates current playback metadata from the coordinator to all grouped slave devices.
        Only runs after startup and assumes device states are generally initialized.
        """
        try:
            #self.trace_me()
            self.logger.info(f"🔄 Runtime: Updating playback metadata to slaves for group '{coordinator_dev.states.get('GROUP_Name', 'Unknown')}'")

            coordinator_ip = coordinator_dev.address.strip()
            soco_device = self.soco_by_ip.get(coordinator_ip)
            if not soco_device:
                self.logger.debug(f"⚠️ Runtime: No SoCo found for coordinator {coordinator_dev.name} @ {coordinator_ip}")
                return

            group = soco_device.group
            if not group:
                self.logger.warning(f"⚠️ Runtime: SoCo group is None for {coordinator_dev.name}")
                return

            group_member_ips = {member.ip_address.strip() for member in group.members}
            slave_devices = [
                dev for dev in indigo.devices.iter("self")
                if dev.address.strip() in group_member_ips and dev.id != coordinator_dev.id
            ]

            # Ensure all slave devices have expected state keys
            for slave_dev in slave_devices:
                self.safe_initialize_states(slave_dev)

            # Define all playback-related state keys to copy
            playback_keys = [
                "Album", "Artist", "Track", "Source", "state",
                "CurrentAlbum", "CurrentArtist", "CurrentTrack", "CurrentSource",
                "CurrentAlbumURI", "CurrentTrackURI", "CurrentTrackArt",
                "albumArtURL", "Q_Album", "Q_Artist", "Q_Track", "Q_Source"
            ]

            # Propagate coordinator state values to all slaves
            for slave_dev in slave_devices:
                for key in playback_keys:
                    value = coordinator_dev.states.get(key, "")
                    try:
                        if value is None:
                            value = ""
                        slave_dev.updateStateOnServer(key, value)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to update key '{key}' on slave {slave_dev.name}: {e}")

        except Exception as e:
            self.exception_handler(e, True)









    def safe_initialize_states(self, dev):
        """
        Ensures that all expected state keys are initialized for the given device.
        This method mirrors the behavior of deviceStartComm() to prevent 'state key not defined' errors.
        """
        #self.trace_me()
        try:
            # Define all expected state keys with default empty values
            expected_keys = [
                "Album", "Artist", "Track", "Source", "state",
                "CurrentAlbum", "CurrentArtist", "CurrentTrack", "CurrentSource",
                "CurrentAlbumURI", "CurrentTrackURI", "CurrentTrackArt",
                "albumArtURL", "Q_Album", "Q_Artist", "Q_Track", "Q_Source",
                "GROUP_Coordinator", "GROUP_Name", "ZP_ART", "ZP_LocalUID", "ZonePlayerUUIDsInGroup"
            ]

            for key in expected_keys:
                if key not in dev.states:
                    dev.updateStateOnServer(key, "")
                    self.logger.debug(f"Initialized state key '{key}' for device '{dev.name}'.")

        except Exception as e:
            self.logger.error(f"Error initializing states for device '{dev.name}': {e}")






    def copyStateFromMaster(self, dev):
        try:
            #self.trace_me()
            self.safe_debug("Copy states from master ZonePlayer...")
            try:
                MasterUID, x = dev.states['GROUP_Name'].split(":")
            except Exception as exception_error:
                self.logger.error(f"copyStateFromMaster - Unable to split Group Name: {dev.states['GROUP_Name']}")
                return

            for mdev in indigo.devices.iter("self.ZonePlayer"):
                if mdev.states['ZP_LocalUID'] == MasterUID:
                    for state in list(ZoneGroupStates):
                        if state == "ZP_CurrentURI":
                            value = uri_group + mdev.states['ZP_LocalUID']
                        else:
                            value = mdev.states[state]
                        if self.plugin.stateUpdatesDebug:
                            self.safe_debug(f"\t Updating Slave Device: {dev.name}, State: {state}, Value: {value}")
                        dev.updateStateOnServer(state, value)
                    dev.updateStateOnServer("ZP_ART", mdev.states['ZP_ART'])
                    try:
                        shutil.copy2("/Library/Application Support/Perceptive Automation/images/Sonos/"+mdev.states['ZP_ZoneName']+"_art.jpg",
                                     "/Library/Application Support/Perceptive Automation/images/Sonos/"+dev.states['ZP_ZoneName']+"_art.jpg")
                    except Exception as exception_error:
                        pass

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getLocale(self):
        try:
            locale.setlocale(locale.LC_ALL, '')
            return locale.getdefaultlocale()[0]

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement




    def get_soco_device(self, ip):
        if ip in self.soco_by_ip:
            return self.soco_by_ip[ip]

        self.logger.warning(f"⚠️ get_soco_device: IP {ip} not found in soco_by_ip. Performing fallback discovery.")
        try:
            soco_device = soco.SoCo(ip)
            self.soco_by_ip[ip] = soco_device
            return soco_device
        except Exception as e:
            self.logger.error(f"❌ get_soco_device: Could not find device with IP {ip} — {e}")
            return None



    from soco.data_structures import to_didl_string

 


    def getPlaylistsDirect(self):
        try:
            self.logger.info("📡 Loading Sonos Playlists...")

            soco_device = self.get_soco_device(self.rootZPIP)
            if not soco_device:
                self.logger.error("❌ getPlaylistsDirect: No SoCo device found.")
                return

            playlists = soco_device.get_sonos_playlists(complete_result=True)
            Sonos_Playlists.clear()

            self.safe_debug(f"🧪 Using SoCo device: {soco_device} ({soco_device.player_name})")
            self.safe_debug(f"🧪 Raw playlists returned: {playlists}")

            for pl in playlists:
                try:
                    eid = getattr(pl, "item_id", None)
                    title = getattr(pl, "title", "Unnamed Playlist")

                    # Handle Sonos item_id that might be in formats like SQ:5 or ...#5
                    if eid:
                        if eid.startswith("SQ:"):
                            uri = eid
                        elif "#" in eid:
                            uri = f"SQ:{eid.split('#')[1]}"
                        else:
                            uri = None
                    else:
                        uri = None

                    if uri:
                        Sonos_Playlists.append((uri, title, eid, pl))
                        self.safe_debug(f"➕ Playlist loaded: {title} | URI: {uri} | ID: {eid}")
                    else:
                        self.logger.warning(f"⚠️ Skipped playlist: {title} — item_id missing or unrecognized format: {eid}")

                except Exception as pe:
                    self.logger.warning(f"⚠️ Error loading playlist object: {pl} — {pe}")

            self.safe_debug(f"🧪 Final dump of Sonos_Playlists entries:")
            for entry in Sonos_Playlists:
                self.safe_debug(f"🧾 {entry}")

            self.logger.info(f"✅ Loaded {len(Sonos_Playlists)} Sonos playlists.")

        except Exception as e:
            self.logger.error(f"❌ getPlaylistsDirect: {e}")





    def getRT_FavStationsDirect(self):
        try:
            global Sonos_RT_FavStations
            list_count = 0
            Sonos_RT_FavStations = []
            ZP  = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>R:0/0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"), 1)
            # self.safe_debug(f"ZP: {ZP}")
            ZPxml = ET.fromstring(ZP)
            # iter = ZPxml.getiterator()
            iter = list(ZPxml.iter())
            for element in iter:
                if str(element).find("}item") >= 0:
                    if element.keys():
                        for name, value in element.items():
                            if name == "id":
                                e_id = value
                    # for child in element.getchildren():
                    for child in list(element.iter()):
                        ctag = str(child.tag).split('}')
                        if ctag[1] == "title":
                            e_title = child.text
                        elif ctag[1] == "res":
                            e_res = self.restoreString(child.text, 0)
                    Sonos_RT_FavStations.append((e_res, e_title))
                    self.safe_debug(f"\tRadioTime Favorite Station: {e_id}, {e_title}, {e_res}")
                    list_count = list_count + 1
            self.logger.info(f"Loaded RadioTime Favorite Stations... [{list_count}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getLineIn(self, dev, val):
        try:
            global Sonos_LineIn
            zoneName = dev.states['ZP_ZoneName']
            LocalUID = dev.states['ZP_LocalUID']
            for x in Sonos_LineIn:
                if x[0] == dev.id:
                    Sonos_LineIn.remove([x[0], x[1]])
                    self.logger.info(f"LineIn: Removed: {LocalUID}, {x[1]}")
            Sonos_LineIn.append([dev.id, val + ":" + zoneName])
            self.logger.info(f"LineIn: {LocalUID}, {val}:{zoneName}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


    def getPandora(self, PandoraEmailAddress, PandoraPassword, PandoraNickname):
        global Sonos_Pandora

        self.logger.debug("🧪 Starting getPandora()")
        self.logger.debug(f"🧪 Pandora flag: {self.pluginPrefs.get('Pandora')}")
        self.logger.debug(f"🧪 Email: {PandoraEmailAddress}")
        self.logger.debug(f"🧪 Password: {'***' if PandoraPassword else '(empty)'}")
        self.logger.debug(f"🧪 Nickname: {PandoraNickname}")
        self.safe_debug(f"✅ Sonos_Pandora currently has {len(Sonos_Pandora)} entries")

        # 🛡️ Validate credentials early
        if not PandoraEmailAddress or not PandoraPassword:
            self.logger.warning("⚠️ Missing Pandora email or password — skipping getPandora()")
            return

        try:
            list_count = 0
            pandora = Pandora()

            self.logger.debug("🧪 Calling Pandora.authenticate()...")
            result = pandora.authenticate(PandoraEmailAddress, PandoraPassword)
            self.logger.debug(f"🧪 Returned from authenticate(): {result}")

            if not result:
                self.logger.error("❌ Pandora authentication failed — skipping station fetch.")
                return

            self.logger.info("🧪 Authentication successful — calling get_station_list()")
            stations = pandora.get_station_list()

            for station in stations:
                Sonos_Pandora.append((
                    station.get('stationId'),
                    station.get('stationName'),
                    PandoraEmailAddress,
                    PandoraNickname or ''
                ))
                self.safe_debug(f"📻 Pandora Station: {station.get('stationId')} - {station.get('stationName')}")

                list_count += 1

            self.logger.info(f"✅ Loaded Pandora Stations for {PandoraNickname or '(no nickname)'}: [{list_count}]")

        except Exception as exception_error:
            self.logger.error(f"❌ Exception in getPandora(): {exception_error}")
            self.exception_handler(exception_error, True)



    def get_artwork_filename(self, dev_name):
        # Normalize device name: lowercase, underscores instead of spaces
        safe_name = dev_name.lower().replace(" ", "_")
        return f"sonos_art_{safe_name}.jpg"


    def cleanup_old_artwork(self):
        import os
        import time

        artwork_dir = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        now = time.time()
        cutoff = now - (2 * 24 * 60 * 60)  # 2 days ago

        deleted = 0
        for filename in os.listdir(artwork_dir):
            if filename.startswith("sonos_art_") and filename.endswith(".jpg"):
                filepath = os.path.join(artwork_dir, filename)
                if os.path.isfile(filepath):
                    if os.path.getmtime(filepath) < cutoff:
                        try:
                            os.remove(filepath)
                            deleted += 1
                            self.logger.info(f"🗑️ Deleted stale artwork file: {filename}")
                        except Exception as e:
                            self.logger.warning(f"⚠️ Could not delete {filename}: {e}")

        if deleted > 0:
            self.logger.info(f"🧹 Artwork cleanup done: {deleted} file(s) removed.")
        else:
            self.logger.info("🧹 No stale artwork files found.")





    def getSiriusXM(self):
        try:
            #from SiriusHelper import SiriusXM  # this must be placed inside the function for Indigo plugin compatibility

            zoneIP = self.getReferencePlayerIP()
            if not zoneIP:
                self.logger.error("❌ getSiriusXM: No reference ZonePlayer IP found.")
                return

            if not self.SiriusXMID or not self.SiriusXMPassword:
                self.logger.error("❌ getSiriusXM: SiriusXM credentials missing.")
                return

            self.logger.info(f"🔐 Attempting SiriusXM login for {self.SiriusXMID}")

            sxm = SiriusXM(self.SiriusXMID, self.SiriusXMPassword)
            if not sxm.authenticate():
                self.logger.error("❌ SiriusXM authentication failed.")
                return

            channels = sxm.get_channels()
            self.logger.info(f"✅ Loaded {len(channels)} SiriusXM channels.")
            
            # Optional: store them globally or assign to Indigo states
            global Sonos_SiriusXM
            Sonos_SiriusXM = []
            for ch in channels:
                number = ch.get("siriusChannelNumber", 0)
                name = ch.get("name", "Unknown")
                channelId = ch.get("channelId", "")
                channelGuid = ch.get("channelGuid", "")
                Sonos_SiriusXM.append((int(number), channelId, name, channelGuid))
                self.safe_debug(f"\t📻 {number}: {name} ({channelId})")

            Sonos_SiriusXM.sort(key=lambda x: x[0])

        except Exception as exception_error:
            self.exception_handler(exception_error, True)

    def getSoundFiles(self):
        try:
            self.Sound_Files = []  # << correct instance var
            list_count = 0

            self.logger.info(f"🔍 Scanning for MP3s in: {self.SoundFilePath}")
            for f in listdir(self.SoundFilePath):
                self.logger.warning(f"🧪 Found file in folder: {f}")
                if f.lower().endswith(".mp3"):
                    self.Sound_Files.append(f)
                    self.logger.info(f"🎵 Added sound file: {f}")
                    list_count += 1

            self.logger.info(f"✅ Loaded Sound Files... [{list_count}]")
        except Exception as exception_error:
            self.exception_handler(exception_error, True)





    #################################################################################################
    ### SOAPSend function with custom filtering for known specific error responses as needed 
    #################################################################################################



    def SOAPSend(self, zoneIP, soapRoot, soapBranch, soapAction, soapPayload):
        try:
            if soapBranch == "/Queue":
                urn = "schemas-sonos-com"
            else:
                urn = "schemas-upnp-org"

            self.safe_debug(f"zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")

            # Convert soapPayload to a string if currently bytes
            if isinstance(soapPayload, bytes):
                soapPayload = soapPayload.decode("utf-8")

            SM_TEMPLATE = (
                '<?xml version="1.0" encoding="utf-8"?>'
                '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" '
                'xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
                '<s:Body>'
                f'<ns0:{soapAction} xmlns:ns0="urn:{urn}:service:{soapBranch[1:]}:1">'
                '<InstanceID>0</InstanceID>'
                f'{soapPayload}'
                f'</ns0:{soapAction}>'
                '</s:Body></s:Envelope>'
            )

            SoapMessage = SM_TEMPLATE
            base_url = f"http://{zoneIP}:1400"

            if soapRoot == "/ZonePlayer":
                control_url = f"{soapBranch}/Control"
            else:
                control_url = f"{soapRoot}{soapBranch}/Control"

            soap_action = f"urn:{urn}:service:{soapBranch[1:]}:1#{soapAction}"
            headers = {
                'Content-Type': 'text/xml; charset="utf-8"',
                'Content-Length': str(len(SoapMessage)),
                'Host': f"{zoneIP}:1400",
                'User-Agent': 'Indigo',
                'SOAPACTION': soap_action
            }

            try:
                response = requests.post(base_url + control_url, headers=headers, data=SoapMessage.encode("utf-8"))
            except Exception as exception_error:
                self.logger.error(f"SOAPSend Error: {exception_error}")
                raise

            res_bytes = response.text.encode("utf-8")
            res = res_bytes.decode("utf-8")
            status = response.status_code

            # Handle non-200 errors AFTER checking errorCode
            if status != 200:
                try:
                    errorCode = self.parseErrorCode(res)

                    if errorCode == "714":
                        self.logger.info(f"🔁 Ignoring benign UPNP error 714 — already using own queue.")
                        return ""

                    elif errorCode == "701":
                        self.safe_debug(f"Ignored UPNP Error 701 (No Such Object) for {zoneIP} — likely SPDIF/TV input")
                        return ""

                    # Only log if not benign
                    self.logger.error(f"UPNP Error: {UPNP_ERRORS.get(errorCode, errorCode)}")
                    self.logger.error(f"Offending Command -> zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")
                    self.logger.error(f"Error Response: {res}")

                except Exception as inner_error:
                    self.logger.error(f"UPNP Error: {status}")
                    self.logger.error(f"Offending Command -> zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")
                    self.logger.error(f"Error Response: {res}")

            # Reconstruct multiline XML response
            resx = ""
            for line in res.splitlines():
                if len(line) <= 5:
                    try:
                        if 0 <= int(line, 16) <= 4096:
                            pass
                        else:
                            resx += line.rstrip('\n')
                    except Exception:
                        pass
                else:
                    resx += line.rstrip('\n')

            if getattr(self.plugin, "xmlDebug", False):
                self.safe_debug(SoapMessage)
                self.safe_debug(resx)

            return resx

        except Exception as exception_error:
            self.exception_handler(exception_error, True)



    #################################################################################################
    ### End - SOAPSend function with custom filtering for known specific error responses as needed 
    #################################################################################################



    def runConcurrentThread(self):
        self.logger.info("🔁 runConcurrentThread started")

        # Keep the plugin thread alive with a regular sleep loop
        while True:
            self.sleep(300)  # Sleep 5 minutes between wakeups

    def stopConcurrentThread(self):
        self.safe_debug("⏹ stopConcurrentThread called")
        self.stopThread = True


    def getZPDeviceList(self, filter=""):
        try:
            array = []
            if filter == "withNone":
                array.append(("00000", "No Selection"))
            for dev in indigo.devices.iter("self.ZonePlayer"):
                array.append((dev.id, dev.states['ZP_ZoneName']))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_LIST(self, filter=""):
        try:
            array = []
            for plist in Sonos_Playlists:
                array.append((plist[0], plist[1]))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_LIST_PlaylistObjects(self, filter=""):
        try:
            array = []
            for plist in Sonos_Playlists:
                array.append((plist[2], plist[1]))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_LineIn(self, filter=""):
        try:
            return Sonos_LineIn

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_SonosFavorites(self, filter=""):
        try:
            array = []
            for title in Sonos_Favorites:
                array.append((title[4], title[1]))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_RT_FavStations(self, filter=""):
        try:
            return Sonos_RT_FavStations

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_Pandora(self, filter="", valuesDict=None, typeId="", targetId=0):
        try:
            return [(s[0], s[1]) for s in Sonos_Pandora]
        except Exception as e:
            self.logger.error(f"❌ getZP_Pandora() failed: {e}")
            return []



    def getZP_SiriusXM(self, filter="", valuesDict=None, typeId="", targetId=0):
        if not self.siriusxm_channels:
            self.logger.error("SiriusXM channel list is empty — cannot populate dropdown.")
            return []

        self.safe_debug(f"SiriusXM total channels fetched: {len(self.siriusxm_channels)}")

        items = []
        for ch in self.siriusxm_channels:
            title = ch.get("title")
            stream_url = ch.get("streamUrl")
            if title and stream_url:
                items.append((title, title))
            elif title:
                self.safe_debug(f"SiriusXM channel '{title}' skipped — no streamUrl found.")

        if not items:
            self.logger.error("No SiriusXM channels with stream URLs found for dropdown list.")
        else:
            self.safe_debug(f"Returning {len(items)} SiriusXM channels with stream URLs to Indigo UI.")

        return items


    def getZP_SoundFiles(self, filter=""):
        try:
            return Sound_Files

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getIVONAVoices(self, filter=""):
        try:
            array = []
            for voice in IVONAVoices:
                array.append((voice[0], voice[4] + " | " + voice[1]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getPollyVoices(self, filter=""):
        try:
            array = []
            for voice in PollyVoices:
                array.append((voice[0], voice[4] + " | " + voice[1]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getAppleVoices(self, filter=""):
        try:
            array = []
            for voice in NSVoices:
                name = NSSpeechSynthesizer.attributesForVoice_(voice)['VoiceName']
                locale = re.split('-|_', NSSpeechSynthesizer.attributesForVoice_(voice)['VoiceLocaleIdentifier'])
                try:
                    vl = language_codes.languages[locale[0]].encode('utf-8')
                except Exception as exception_error:
                    vl = locale[0]
                try:
                    vc = language_codes.countries[locale[1]].encode('utf-8')
                except Exception as exception_error:
                    vc = locale[1]
                # array.append((voice,  vc + ', ' +  vl + ' | ' + name))

                print(f"Voice: {type(voice)}")
                print(f"vc: {type(voice)}")
                print(f"vl: {type(voice)}")
                print(f"name: {type(voice)}")

                try:
                    vc = vc.decode("utf-8")
                except Exception as exception_error:
                    pass
                try:
                    vl = vl.decode("utf-8")
                except Exception as exception_error:
                    pass

                array.append((voice, f"{vc}, {vl} | {name}"))

            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


    def actionTogglePlay(self, indigo_device):
        zoneIP = indigo_device.address
        transport_state = indigo_device.states.get("ZP_STATE", "STOPPED").upper()

        self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from Indigo): {transport_state}")

        # If ZP_STATE looks unreliable, fall back to querying SoCo directly
        if transport_state not in ("PLAYING", "PAUSED_PLAYBACK", "STOPPED"):
            soco_device = self.findDeviceByIP(zoneIP)
            if soco_device:
                try:
                    transport_info = soco_device.get_current_transport_info()
                    transport_state = transport_info.get("current_transport_state", "STOPPED").upper()
                    self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from SoCo): {transport_state}")
                except Exception as e:
                    self.logger.warning(f"⚠️ SoCo state fetch failed for {indigo_device.name}: {e}")
                    transport_state = "STOPPED"

        # Execute based on state
        if transport_state == "PLAYING":
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"⏸ Pause triggered for {indigo_device.name}")
        else:
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"▶️ Play triggered for {indigo_device.name}")

    def getReferencePlayerIP(self):
        try:
            for dev in indigo.devices.iter("self"):
                if dev.enabled and dev.address:
                    return dev.address
            self.logger.warning("⚠️ No enabled Sonos devices found with IP addresses.")
        except Exception as e:
            self.logger.error(f"❌ Error in getReferencePlayerIP: {e}")
        return None


    def diagnoseSubscriptions(self):
        self.logger.info("🧪 Running SoCo subscription diagnostics...")
        try:
            if not self.soco_subs:
                self.logger.warning("⚠️ No subscriptions found in self.soco_subs.")
                return

            for dev_id, subs in self.soco_subs.items():
                try:
                    indigo_device = indigo.devices[int(dev_id)]
                    self.logger.info(f"🔍 Device: {indigo_device.name} ({indigo_device.address})")
                except Exception:
                    self.logger.warning(f"🔍 Device ID {dev_id} (not found in Indigo)")

                if not subs:
                    self.logger.warning("   ⚠️ No subscriptions registered for this device.")
                    continue

                for service_name, sub in subs.items():
                    sid = getattr(sub, 'sid', 'no-sid')
                    has_cb = hasattr(sub, 'callback') and sub.callback is not None
                    cb_name = sub.callback.__name__ if has_cb else "None"
                    self.logger.info(f"   🔔 {service_name} | SID: {sid} | Callback: {cb_name}")
        except Exception as e:
            self.logger.error(f"❌ diagnoseSubscriptions failed: {e}")

#####


    def getMicrosoftLanguages(self, filter=""):
        try:
            array = []
            for code in self.MSTranslateVoices:
                array.append((code, self.MSTranslateVoices[code]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


########################################################################################################################################################################
## SiriusXM Class wraps the SXM.PY app into a standalone class that will be used for login / session management / metadata capture for use within the indigo plugin   ##
########################################################################################################################################################################


class SiriusXM:
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    REST_FORMAT = 'https://player.siriusxm.com/rest/v2/experience/modules/{}'
    LIVE_PRIMARY_HLS = 'https://siriusxm-priprodlive.akamaized.net'

    def __init__(self, username, password, logger=None):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
        self.username = username
        self.password = password
        self.playlists = {}
        self.channels = None
        self.logger = logger  # ✅ Indigo logger passed in

    def log(self, message):
        if self.logger:
            self.logger.warning(f"<SiriusXM>: {message}")
        else:
            print(f"{datetime.datetime.now().strftime('%d.%b %Y %H:%M:%S')} <SiriusXM>: {message}")

    def is_logged_in(self):
        return 'SXMDATA' in self.session.cookies

    def is_session_authenticated(self):
        return 'AWSALB' in self.session.cookies and 'JSESSIONID' in self.session.cookies

    def get(self, method, params, authenticate=True):
        if authenticate and not self.is_session_authenticated() and not self.authenticate():
            self.log('Unable to authenticate')
            return None

        res = self.session.get(self.REST_FORMAT.format(method), params=params)
        if res.status_code != 200:
            self.log(f"Received status code {res.status_code} for method '{method}'")
            return None

        try:
            return res.json()
        except ValueError:
            self.log(f"Error decoding json for method '{method}'")
            return None

    def post(self, method, postdata, authenticate=True):
        if authenticate and not self.is_session_authenticated() and not self.authenticate():
            self.log('Unable to authenticate')
            return None

        res = self.session.post(self.REST_FORMAT.format(method), data=json.dumps(postdata))
        if res.status_code != 200:
            self.log(f"Received status code {res.status_code} for method '{method}'")
            return None

        try:
            return res.json()
        except ValueError:
            self.log(f"Error decoding json for method '{method}'")
            return None

    def login(self):
        postdata = {
            'moduleList': {
                'modules': [{
                    'moduleRequest': {
                        'resultTemplate': 'web',
                        'deviceInfo': {
                            'osVersion': 'Mac',
                            'platform': 'Web',
                            'sxmAppVersion': '3.1802.10011.0',
                            'browser': 'Safari',
                            'browserVersion': '11.0.3',
                            'appRegion': 'US',
                            'deviceModel': 'K2WebClient',
                            'clientDeviceId': 'null',
                            'player': 'html5',
                            'clientDeviceType': 'web',
                        },
                        'standardAuth': {
                            'username': self.username,
                            'password': self.password,
                        },
                    },
                }],
            },
        }
        data = self.post('modify/authentication', postdata, authenticate=False)
        if not data:
            return False

        try:
            return data['ModuleListResponse']['status'] == 1 and self.is_logged_in()
        except KeyError:
            self.log('Error decoding json response for login')
            return False

    def authenticate(self):
        if not self.is_logged_in() and not self.login():
            self.log('Unable to authenticate because login failed')
            return False

        postdata = {
            'moduleList': {
                'modules': [{
                    'moduleRequest': {
                        'resultTemplate': 'web',
                        'deviceInfo': {
                            'osVersion': 'Mac',
                            'platform': 'Web',
                            'clientDeviceType': 'web',
                            'sxmAppVersion': '3.1802.10011.0',
                            'browser': 'Safari',
                            'browserVersion': '11.0.3',
                            'appRegion': 'US',
                            'deviceModel': 'K2WebClient',
                            'player': 'html5',
                            'clientDeviceId': 'null'
                        }
                    }
                }]
            }
        }
        data = self.post('resume?OAtrial=false', postdata, authenticate=False)
        if not data:
            return False

        try:
            return data['ModuleListResponse']['status'] == 1 and self.is_session_authenticated()
        except KeyError:
            self.log('Error parsing json response for authentication')
            return False

    def get_sxmak_token(self):
        try:
            return self.session.cookies['SXMAKTOKEN'].split('=', 1)[1].split(',', 1)[0]
        except (KeyError, IndexError):
            return None

    def get_gup_id(self):
        try:
            return json.loads(urllib.parse.unquote(self.session.cookies['SXMDATA']))['gupId']
        except (KeyError, ValueError):
            return None

    def get_playlist_url(self, guid, channel_id, use_cache=True, max_attempts=5):
        if use_cache and channel_id in self.playlists:
             return self.playlists[channel_id]

        params = {
            'assetGUID': guid,
            'ccRequestType': 'AUDIO_VIDEO',
            'channelId': channel_id,
            'hls_output_mode': 'custom',
            'marker_mode': 'all_separate_cue_points',
            'result-template': 'web',
            'time': int(round(time.time() * 1000.0)),
            'timestamp': datetime.datetime.utcnow().isoformat('T') + 'Z'
        }
        data = self.get('tune/now-playing-live', params)
        if not data:
            return None

        try:
            status = data['ModuleListResponse']['status']
            message = data['ModuleListResponse']['messages'][0]['message']
            message_code = data['ModuleListResponse']['messages'][0]['code']
        except (KeyError, IndexError):
            self.log('Error parsing json response for playlist')
            return None

        if message_code in [201, 208]:
            if max_attempts > 0:
                self.log('Session expired, logging in and authenticating')
                if self.authenticate():
                    self.log('Successfully authenticated')
                    return self.get_playlist_url(guid, channel_id, use_cache, max_attempts - 1)
                else:
                    self.log('Failed to authenticate')
                    return None
            else:
                self.log('Reached max attempts for playlist')
                return None
        elif message_code != 100:
            self.log(f'Received error {message_code} {message}')
            return None

        try:
            playlists = data['ModuleListResponse']['moduleList']['modules'][0]['moduleResponse']['liveChannelData']['hlsAudioInfos']
        except (KeyError, IndexError):
            self.log('Error parsing json response for playlist')
            return None

        for playlist_info in playlists:
            if playlist_info['size'] == 'LARGE':
                playlist_url = playlist_info['url'].replace('%Live_Primary_HLS%', self.LIVE_PRIMARY_HLS)
                self.playlists[channel_id] = self.get_playlist_variant_url(playlist_url)
                return self.playlists[channel_id]

        return None

    def get_playlist_variant_url(self, url):
        params = {
            'token': self.get_sxmak_token(),
            'consumer': 'k2',
            'gupId': self.get_gup_id(),
        }
        res = self.session.get(url, params=params)

        if res.status_code != 200:
            self.log(f"Received status code {res.status_code} on playlist variant retrieval")
            return None

        for line in res.text.split('\n'):
            if line.rstrip().endswith('.m3u8'):
                return f"{url.rsplit('/', 1)[0]}/{line.rstrip()}"

        return None

    def get_channels(self):
        if not self.channels:
            postdata = {
                'moduleList': {
                    'modules': [{
                        'moduleArea': 'Discovery',
                        'moduleType': 'ChannelListing',
                        'moduleRequest': {
                            'consumeRequests': [],
                            'resultTemplate': 'responsive',
                            'alerts': [],
                            'profileInfos': []
                        }
                    }]
                }
            }
            data = self.post('get', postdata)
            if not data:
                self.log('Unable to get channel list')
                return []

            try:
                self.channels = data['ModuleListResponse']['moduleList']['modules'][0]['moduleResponse']['contentData']['channelListing']['channels']
            except (KeyError, IndexError):
                self.log('Error parsing json response for channels')
                return []

        return self.channels

    def get_channel(self, name):
        name = name.lower()
        for channel in self.get_channels():
            if (channel.get('name', '').lower() == name or
                channel.get('channelId', '').lower() == name or
                channel.get('siriusChannelNumber', '').lower() == name or
                channel.get('channelGuid') == name):
                return (channel['channelGuid'], channel['channelId'])

        return (None, None)