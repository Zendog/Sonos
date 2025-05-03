import sys
import os
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
logging.getLogger("Plugin.Sonos").warning(
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
    'ZP_ALBUM', 'ZP_ARTIST', 'ZP_CREATOR', 'ZP_TRACK', 'ZP_NALBUM',
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


        self.httpd = None
        self.httpd_thread = None

        self.plugin = plugin
        self.pluginPrefs = pluginPrefs  # ✅ Must be assigned first

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
            self.logger.warning("🔁 Preloading Pandora stations at init.")
            Sonos_Pandora = []  # Clear global list to ensure fresh load
            self.getPandora(self.PandoraEmailAddress, self.PandoraPassword, self.PandoraNickname)

        # ... continue your normal init process ...

        import uuid
        import os
        import json
        from sxm import SXMClient, RegionChoice, XMChannel

        self.logger = logging.getLogger("Plugin.Sonos")
        self.logger.info(f"Initializing SonosPlugin... [{uuid.uuid4()}]")

        self.plugin = plugin
        self.pluginPrefs = pluginPrefs
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

    ### End of Initialization



    ############################################################################################
    ### Actiondirect List Processing
    ############################################################################################


############################################################################################
### Actiondirect List Processing
############################################################################################

    def actionDirect(self, pluginAction, action_id_override=None):
        try:
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
                "VolumeUp": "actionVolumeUp",
                "VolumeDown": "actionVolumeDown",
                "BassUp": "actionBassUp",
                "BassDown": "actionBassDown",
                "TrebleUp": "actionTrebleUp",
                "TrebleDown": "actionTrebleDown",
                "setStandalone": "actionZP_setStandalone",
                "actionsetStandalone": "actionZP_setStandalone",
                "setStandalones": "actionZP_setStandalones",
                "addPlayerToZone": "actionZP_addPlayerToZone",
                "addPlayersToZone": "actionZP_addPlayersToZone",
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
                "Q_RepeatToggle": "actionQ_RepeatToggle",
            }

            raw_key = action_id_override or pluginAction.pluginTypeId
            action_key = action_map.get(raw_key, raw_key)
            action_id = action_key

            device_id = int(pluginAction.deviceId)
            self.safe_debug(f"⚡ Action received: {action_id} for device ID {device_id}")
            self.safe_debug(f"🧭 Final resolved action_id: {action_id}")

            dev = indigo.devices[device_id]
            zoneIP = dev.address

            # Table-driven dispatch with normalized handler signatures
            dispatch_table = {
                "SetSiriusXMChannel": lambda p, d, z: self.handleAction_SetSiriusXMChannel(p, d, z),
                "actionZP_SiriusXM": lambda p, d, z: self.handleAction_ZP_SiriusXM(p, d, z),
                "actionZP_Pandora": lambda p, d, z: self.handleAction_ZP_Pandora(p, d, z, p.props),
                "actionChannelUp": lambda p, d, z: self.handleAction_ChannelUp(p, d, z),
                "actionChannelDown": lambda p, d, z: self.handleAction_ChannelDown(p, d, z),
                "actionZP_setStandalone": lambda p, d, z: self.handleAction_ZP_setStandalone(p, d, z),
                "actionQ_Shuffle": lambda p, d, z: self.handleAction_Q_Shuffle(p, d, z),
                "actionQ_Crossfade": lambda p, d, z: self.handleAction_Q_Crossfade(p, d, z),
            }

            if action_id in dispatch_table:
                dispatch_table[action_id](pluginAction, dev, zoneIP)
                return

            # Inline action handlers follow...
            # ... (Omitted for brevity)
            # Inline handlers
            if action_id == "actionBassUp":
                current = int(dev.states.get("ZP_BASS", 0))
                newVal = max(min(current + 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass",
                              f"<DesiredBass>{newVal}</DesiredBass>")
                self.logger.info(f"🔊 Bass increased on {dev.name}: {current} → {newVal}")
                return

            elif action_id == "actionBassDown":
                current = int(dev.states.get("ZP_BASS", 0))
                newVal = max(min(current - 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass",
                              f"<DesiredBass>{newVal}</DesiredBass>")
                self.logger.info(f"🔉 Bass decreased on {dev.name}: {current} → {newVal}")
                return

            elif action_id == "actionTrebleUp":
                current = int(dev.states.get("ZP_TREBLE", 0))
                newVal = max(min(current + 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble",
                              f"<DesiredTreble>{newVal}</DesiredTreble>")
                self.logger.info(f"🎶 Treble increased on {dev.name}: {current} → {newVal}")
                return

            elif action_id == "actionTrebleDown":
                current = int(dev.states.get("ZP_TREBLE", 0))
                newVal = max(min(current - 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble",
                              f"<DesiredTreble>{newVal}</DesiredTreble>")
                self.logger.info(f"🎵 Treble decreased on {dev.name}: {current} → {newVal}")
                return

            elif action_id == "actionVolumeUp":
                self.safe_debug("🧪 Matched action_id == actionVolumeUp")  # <- ADD THIS
                current = int(dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = min(100, current + 5)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")
                self.logger.info(f"🔊 Volume UP for {dev.name}: {current} → {new_volume}")
                return

            elif action_id == "actionVolumeDown":
                current = int(dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = max(0, current - 5)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")
                self.logger.info(f"🔉 Volume DOWN for {dev.name}: {current} → {new_volume}")
                return

            elif action_id == "actionMuteToggle":
                raw_state = dev.states.get("ZP_MUTE", "unknown")
                mute_state = raw_state.lower() == "true"
                mute_val = "0" if mute_state else "1"
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              f"<Channel>Master</Channel><DesiredMute>{mute_val}</DesiredMute>")
                self.logger.info(f"🎚 Mute TOGGLE for {dev.name}: {'Off' if mute_state else 'On'}")
                return

            elif action_id == "actionMuteOn":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                self.logger.info(f"🔇 Mute ON for {dev.name}")
                return

            elif action_id == "actionMuteOff":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                self.logger.info(f"🔊 Mute OFF for {dev.name}")
                return

            elif action_id == "actionStop":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "<InstanceID>0</InstanceID>")
                self.logger.info(f"⏹️ Stop triggered for {dev.name}")
                return


            elif action_id == "actionNext":
                uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
                self.safe_debug(f"🧪 Current track URI for Next: {uri}")
                if "sirius" in uri.lower() or "x-sonosapi-" in uri.lower():
                    self.logger.info(f"📻 Detected SiriusXM stream — calling channelUpOrDown(up) for {dev.name}")
                    self.channelUpOrDown(dev, direction="up")
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Next", "<InstanceID>0</InstanceID>")
                    self.logger.info(f"⏭️ Next track for {dev.name}")
                return

            elif action_id == "actionPrevious":
                uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
                self.safe_debug(f"🧪 Current track URI for Previous: {uri}")
                if "sirius" in uri.lower() or "x-sonosapi-" in uri.lower():
                    self.logger.info(f"📻 Detected SiriusXM stream — calling channelUpOrDown(down) for {dev.name}")
                    self.channelUpOrDown(dev, direction="down")
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


            elif action_id == "ZP_LIST":
                self.actionZP_LIST(pluginAction, dev)
                return



            # If it gets this far, action was not handled
            self.logger.warning(f"⚠️ Unknown or unsupported action: {action_id}")

        except Exception as e:
            self.logger.error(f"❌ actionDirect exception: {e}")


### End of Actiondirect List Processing

 
    ### End of Actiondirect List Processing


    ############################################################################################
    ### Handleaction definitions
    ############################################################################################



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






    def handleAction_ZP_Pandora(self, pluginAction, dev, zoneIP, props):
        try:
            station_id = pluginAction.props.get("setting") or pluginAction.props.get("channelSelector")
            self.logger.warning(f"🧪 handleAction_ZP_Pandora() called — device: {dev.name} | zoneIP: {zoneIP}")
            self.logger.warning(f"🪪 Extracted Pandora station ID: {station_id}")

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
            self.safe_debug(f"🪪 handleAction_SetSiriusXMChannel() called for device {dev.name} at {zoneIP}")
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
        self.logger.warning(f"📝 Sample ID map keys: {list(self.siriusxm_id_map.keys())[:5]}")
        self.logger.warning(f"📝 Sample GUID map keys: {list(self.siriusxm_guid_map.keys())[:5]}")
        self.logger.info(f"✅ Maps built: {len(self.siriusxm_id_map)} IDs, {len(self.siriusxm_guid_map)} GUIDs")

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
        self.logger.warning("🪪 Entered plugin.py::actionZP_SiriusXM")

        props = pluginAction.props
        self.logger.warning(f"🧪 Raw pluginAction.props: {props}")

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
            raw_val = pluginAction.props.get("ZP_LIST") or pluginAction.props.get("setting")
            if not raw_val:
                self.logger.error(f"❌ actionZP_LIST: No playlist selected for {dev.name}")
                return

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

            soco_dev.avTransport.SetAVTransportURI([
                ('InstanceID', 0),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', metadata),
            ])
            soco_dev.play()

            if "channel_number" in channel and "name" in channel:
                channel_number = channel["channel_number"]
                channel_name = channel["name"]
                dev.updateStateOnServer("ZP_STATION", f"CH {channel_number} - {channel_name}")
                self.safe_debug(f"📝 Updated ZP_STATION to CH {channel_number} - {channel_name}")

            self.logger.info(f"✅ Successfully changed {dev.name} to {title}")

            # --- Save last known SiriusXM channel number ---
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
            self.logger.warning("▶️ Play payload: <Speed>1</Speed>")
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
                    if self.SoundFilePath != self.plugin.pluginPrefs["SoundFilePath"]:
                        self.SoundFilePath = self.plugin.pluginPrefs["SoundFilePath"]
                        if self.SoundFilePath is not None and self.SoundFilePath != "":
                            self.getSoundFiles()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve SoundFilePath.")

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
            self.safe_debug(f"🛑 deviceStopComm called for: {indigo_device.name} (ID: {indigo_device.id})")
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


        # Cleanup old art before starting the server to reduce storage size and keep things tidy
        self.cleanup_old_artwork()        


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
        self.logger.warning(f"🧪 Model name for {indigo_device.name}: {model_name}")

        self.soco_subs[indigo_device.id] = {}
        self.soco_by_ip[indigo_device.address] = soco_device
        self.safe_debug(f"✅ soco_by_ip[{indigo_device.address}] stored with SoCo {soco_device.uid}")

        def _log_subscription_result(service_name, sub_obj):
            self.safe_debug(f"🔍 {service_name}.subscribe() returned: {sub_obj}")
            self.safe_debug(f"🔍 {service_name} Subscription SID: {getattr(sub_obj, 'sid', 'No SID')}")
            self.safe_debug(f"🔍 {service_name} Subscription type: {type(sub_obj)}")

        # AVTransport
        try:
            self.logger.warning(f"🔔 Initiating subscription to AVTransport for {indigo_device.name}")
            av_sub = soco_device.avTransport.subscribe(auto_renew=True, strict=True)
            _log_subscription_result("AVTransport", av_sub)

            av_sub.callback = self.soco_event_handler
            self.soco_subs[indigo_device.id]["AVTransport"] = av_sub
            self.logger.info(f"✅ Subscribed to AVTransport | SID: {getattr(av_sub, 'sid', 'N/A')}, Callback: {getattr(av_sub.callback, '__name__', 'None')}")
        except Exception as e:
            self.logger.error(f"❌ Failed to subscribe to AVTransport: {e}")

        # RenderingControl
        try:
            self.logger.warning(f"🔔 Initiating subscription to RenderingControl for {indigo_device.name}")
            rc_sub = soco_device.renderingControl.subscribe(auto_renew=True, strict=True)
            _log_subscription_result("RenderingControl", rc_sub)

            rc_sub.callback = self.soco_event_handler
            self.soco_subs[indigo_device.id]["RenderingControl"] = rc_sub
            self.logger.info(f"✅ Subscribed to RenderingControl | SID: {getattr(rc_sub, 'sid', 'N/A')}, Callback: {getattr(rc_sub.callback, '__name__', 'None')}")
        except Exception as e:
            self.logger.error(f"❌ Failed to subscribe to RenderingControl: {e}")

        # Optional AudioIn
        if model_name.lower().startswith("connect") or "port" in model_name.lower():
            try:
                self.logger.warning(f"🔔 Initiating subscription to AudioIn for {indigo_device.name}")
                ai_sub = soco_device.audioIn.subscribe(auto_renew=True, strict=True)
                _log_subscription_result("AudioIn", ai_sub)

                ai_sub.callback = self.soco_event_handler
                self.soco_subs[indigo_device.id]["AudioIn"] = ai_sub
                self.logger.info(f"✅ Subscribed to AudioIn | SID: {getattr(ai_sub, 'sid', 'N/A')}, Callback: {getattr(ai_sub.callback, '__name__', 'None')}")
            except Exception as e:
                self.logger.error(f"❌ Failed to subscribe to AudioIn: {e}")

        # Final Listener Check
        self.logger.warning(
            f"🛰 Listener running={event_listener.is_running}, "
            f"bound to {getattr(event_listener, 'address', '?')}:{getattr(event_listener, 'port', '?')}"
        )


    ############################################################################################
    ### Start Device communications
    ############################################################################################


    def deviceStartComm(self, indigo_device):
        self.logger.warning(f"🧪 deviceStartComm CALLED for {indigo_device.name}")

        try:
            self.logger.info(f"🔌 Starting communication with Indigo device {indigo_device.name} ({indigo_device.address})")
            self.devices[indigo_device.id] = indigo_device

            # 🖼️ Preload ZP_ART with default placeholder if missing
            if not indigo_device.states.get("ZP_ART"):
                self.logger.warning(f"🖼️ Preloading ZP_ART with default placeholder for {indigo_device.name}")
                indigo_device.updateStateOnServer("ZP_ART", "/images/no_album_art.png")

            # Force plugin to use upgraded SoCo library
            import sys
            import os
            upgraded_path = os.path.join(os.path.dirname(__file__), "soco-upgraded")
            if upgraded_path not in sys.path:
                sys.path.insert(0, upgraded_path)

            import soco
            from soco import SoCo
            import inspect

            # Confirm SoCo version and path
            self.logger.warning(f"🧪 SoCo loaded from: {getattr(soco, '__file__', 'unknown')}")
            self.logger.warning(f"🧪 SoCo version: {getattr(soco, '__version__', 'unknown')}")

            soco_device = None

            try:
                self.logger.info("🔍 Performing SoCo discovery to find matching device...")
                discovered = soco.discover()
                if discovered:
                    for dev in discovered:
                        if dev.ip_address == indigo_device.address:
                            soco_device = dev
                            self.logger.warning(f"✅ Found and initialized SoCo device for {indigo_device.name} at {dev.ip_address}")
                            break
                    if not soco_device:
                        self.logger.warning(f"⚠️ No matching SoCo device found for {indigo_device.name}")
                else:
                    self.logger.warning("❌ No Sonos devices discovered on the network.")
            except Exception as soco_discovery_error:
                self.logger.error(f"❌ SoCo discovery failed: {soco_discovery_error}")

            # 🔁 Fallback to direct SoCo creation if discovery missed it
            if not soco_device:
                self.logger.warning(f"⚠️ Discovery missed {indigo_device.name}, trying direct SoCo init...")
                try:
                    soco_device = SoCo(indigo_device.address)
                    self.logger.warning(f"✅ Fallback SoCo created for {indigo_device.name} at {indigo_device.address}")
                except Exception as e:
                    self.logger.error(f"❌ Fallback SoCo init failed for {indigo_device.name}: {e}")

            if soco_device:
                # ✅ Store in lookup map
                self.soco_by_ip[indigo_device.address] = soco_device
                self.safe_debug(f"✅ soco_by_ip[{indigo_device.address}] stored with SoCo {getattr(soco_device, 'uid', 'unknown')}")

                # Retrieve and log model name
                model_name = self.get_model_name(soco_device)
                self.logger.warning(f"🧪 Retrieved model_name for {indigo_device.name}: {model_name}")

                # Start SoCo Event Listener once
                if not getattr(self, "event_listener_started", False):
                    try:
                        from soco.events import event_listener
                        self.logger.info("🚀 Starting SoCo Event Listener...")
                        soco.config.EVENT_LISTENER_IP = self.find_sonos_interface_ip()
                        event_listener.start(any_zone=soco_device)
                        self.event_listener_started = True
                        self.logger.info(f"✅ SoCo Event Listener running: {event_listener.is_running}")
                    except Exception as e:
                        self.logger.error(f"❌ Failed to start SoCo Event Listener: {e}")

                try:
                    # Confirm UPnP control points exist
                    av = soco_device.avTransport
                    rc = soco_device.renderingControl
                    self.safe_debug(f"🧪 About to call socoSubscribe() for {indigo_device.name}")
                    self.socoSubscribe(indigo_device, soco_device)
                    self.safe_debug(f"🧪 Returned from socoSubscribe() for {indigo_device.name}")
                except Exception as e:
                    self.logger.error(f"❌ socoSubscribe() failed for {indigo_device.name}: {e}")

            else:
                self.logger.warning(f"🧪 soco_device is None — skipping subscription for {indigo_device.name}")

        except Exception as e:
            self.logger.error(f"❌ Error in deviceStartComm for {indigo_device.name}: {e}")





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



    def find_sonos_interface_ip(self, target_subnet=None):
        try:
            subnet_to_use = target_subnet or self.targetSonosSubnet or "192.168.80.0/24"
            target_net = ipaddress.IPv4Network(subnet_to_use)
            self.logger.info(f"🔍 Searching for interface IP on subnet {subnet_to_use}...")

            adapters = ifaddr.get_adapters()
            for adapter in adapters:
                for ip_obj in adapter.ips:
                    ip = ip_obj.ip
                    if isinstance(ip, (list, tuple)):
                        continue
                    try:
                        ip_addr = ipaddress.IPv4Address(ip)
                        self.logger.info(f"   🧪 Interface {adapter.nice_name} has IP {ip_addr}")
                        if ip_addr in target_net:
                            self.logger.info(f"   ✅ Selected interface {adapter.nice_name} with IP {ip_addr} (matches target subnet)")
                            return str(ip_addr)
                    except ipaddress.AddressValueError:
                        continue

            self.logger.warning("❌ No interface found on target Sonos subnet.")
            return None
        except Exception as e:
            self.logger.error(f"Exception in find_sonos_interface_ip: {e}")
            return None

            



    #################################################################################################
    ### Event Handler to process soco state changes and retreive current dynamic state updates
    #################################################################################################


    def soco_event_handler(self, event_obj):
        try:
            # Get zone_ip
            zone_ip = getattr(event_obj, "zone_ip", None)
            if not zone_ip and hasattr(event_obj, "soco"):
                zone_ip = getattr(event_obj.soco, "ip_address", None)

            # Fallback: find zone_ip from subscription
            if not zone_ip:
                for dev_id, subs in self.soco_subs.items():
                    if any(sub.sid == getattr(event_obj, "sid", None) for sub in subs.values()):
                        zone_ip = indigo.devices[int(dev_id)].address
                        break

            if not zone_ip:
                zone_ip = "unknown"

            self.safe_debug(f"🧪 Event handler fired! SID={getattr(event_obj, 'sid', 'N/A')} zone_ip={zone_ip} Type={type(event_obj)}")
            self.safe_debug(f"🧑‍💻 Full event variables: {getattr(event_obj, 'variables', {})}")

            if not hasattr(self, "last_siriusxm_track_by_dev"):
                self.last_siriusxm_track_by_dev = {}
            if not hasattr(self, "last_siriusxm_artist_by_dev"):
                self.last_siriusxm_artist_by_dev = {}

            state_updates = {}

            def safe_call(val):
                try:
                    return val() if callable(val) else val
                except Exception:
                    return ""

            # Find indigo device
            indigo_device = None
            for dev_id, subs in self.soco_subs.items():
                if any(sub.sid == getattr(event_obj, "sid", None) for sub in subs.values()):
                    indigo_device = indigo.devices[int(dev_id)]
                    break

            if not indigo_device:
                self.logger.warning(f"⚠️ Could not find device for SID {event_obj.sid}")
                return

            dev_id = indigo_device.id
            current_uri = None
            is_siriusxm = False

            self.safe_debug(f"🧪 Event received from SID {event_obj.sid} | Seq: {event_obj.seq}")
            for var, val in event_obj.variables.items():
                self.safe_debug(f"   🖼️ {var} = {val}")

            # Transport state, volume, mute, bass, treble
            if "transport_state" in event_obj.variables:
                state_updates["ZP_STATE"] = event_obj.variables["transport_state"]

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

            # Handle track URI and SiriusXM
            current_uri = (
                event_obj.variables.get("current_track_uri") or
                event_obj.variables.get("enqueued_transport_uri") or
                event_obj.variables.get("av_transport_uri")
            )
            if current_uri:
                state_updates["ZP_CurrentTrackURI"] = current_uri
                if current_uri.startswith("x-sonosapi-hls:channel-linear"):
                    is_siriusxm = True
                    self.safe_debug(f"🧪 Detected SiriusXM stream URI: {current_uri}")

            if is_siriusxm and "av_transport_uri_meta_data" in event_obj.variables:
                meta = event_obj.variables["av_transport_uri_meta_data"]
                try:
                    title_raw = safe_call(getattr(meta, "title", ""))
                    if " - " in title_raw:
                        ch_part, name_part = title_raw.split(" - ", 1)
                        ch_part = ch_part.strip()
                        name_part = name_part.strip()
                    else:
                        ch_part = title_raw.strip()
                        name_part = ""

                    if ch_part:
                        state_updates["ZP_TRACK"] = ch_part
                        self.last_siriusxm_track_by_dev[dev_id] = ch_part
                    if name_part:
                        state_updates["ZP_ARTIST"] = name_part
                        self.last_siriusxm_artist_by_dev[dev_id] = name_part
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to parse SiriusXM av_transport_uri_meta_data: {e}")

            if is_siriusxm:
                if "ZP_TRACK" not in state_updates and dev_id in self.last_siriusxm_track_by_dev:
                    state_updates["ZP_TRACK"] = self.last_siriusxm_track_by_dev[dev_id]
                    self.safe_debug(f"🧪 Reusing last SiriusXM track value")
                if "ZP_ARTIST" not in state_updates and dev_id in self.last_siriusxm_artist_by_dev:
                    state_updates["ZP_ARTIST"] = self.last_siriusxm_artist_by_dev[dev_id]
                    self.safe_debug(f"🧪 Reusing last SiriusXM artist value")

            # NEW: Handle regular music metadata (non-SiriusXM)
            if "current_track_meta_data" in event_obj.variables:
                meta = event_obj.variables["current_track_meta_data"]
                try:
                    track_title = safe_call(getattr(meta, "title", ""))
                    track_artist = safe_call(getattr(meta, "artist", ""))
                    track_album = safe_call(getattr(meta, "album", ""))
                    if track_title:
                        state_updates["ZP_TRACK"] = track_title
                    if track_artist:
                        state_updates["ZP_ARTIST"] = track_artist
                    if track_album:
                        state_updates["ZP_ALBUM"] = track_album
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to extract current_track_meta_data: {e}")

            # Check if this device is the coordinator (master)
            coordinator = self.getCoordinatorDevice(indigo_device)
            is_master = (coordinator.address == indigo_device.address)

            album_art_uri = ""
            if is_master:
                meta = event_obj.variables.get("current_track_meta_data", None)
                if meta:
                    album_art_uri = safe_call(getattr(meta, "album_art_uri", ""))
                    if album_art_uri.startswith("/"):
                        album_art_uri = f"http://{zone_ip}:1400{album_art_uri}"

                    if album_art_uri.startswith("http://") or album_art_uri.startswith("https://"):
                        try:
                            response = requests.get(album_art_uri, timeout=5)
                            if response.status_code == 200:
                                artwork_path = f"/Library/Application Support/Perceptive Automation/images/Sonos/sonos_art_{zone_ip}.jpg"
                                with open(artwork_path, "wb") as f:
                                    f.write(response.content)
                                album_art_uri = f"http://localhost:8888/sonos_art_{zone_ip}.jpg"
                                self.logger.info(f"🖼️ Updated album art URI for master {zone_ip} to: {album_art_uri}")
                            else:
                                self.logger.warning(f"⚠️ Failed to download album art. Status code: {response.status_code}")
                                album_art_uri = f"http://localhost:8888/default.jpg"
                        except Exception as e:
                            self.logger.error(f"❌ Error downloading album art: {e}")
                            album_art_uri = f"http://localhost:8888/default.jpg"
                    else:
                        self.logger.warning(f"⚠️ Unexpected album_art_uri format: {album_art_uri}")
                        album_art_uri = f"http://localhost:8888/default.jpg"
                else:
                    self.logger.warning(f"⚠️ No track metadata found for master {indigo_device.name}")
                    album_art_uri = f"http://localhost:8888/default.jpg"

                # Store on coordinator
                state_updates["ZP_ART"] = album_art_uri

            else:
                # Slaves copy from master (golden rule)
                master_zone_ip = coordinator.address
                album_art_uri = f"http://localhost:8888/sonos_art_{master_zone_ip}.jpg"
                self.logger.info(f"🖼️ Slave {indigo_device.name} using master artwork: {album_art_uri}")
                state_updates["ZP_ART"] = album_art_uri

            # Update device states
            if state_updates:
                self.safe_debug(f"🧑‍💻 Updating {indigo_device.name} with state: {state_updates}")
                for k, v in state_updates.items():
                    self.logger.debug(f"🧑‍💻 Updating {indigo_device.name} state {k} with value {v}")
                    indigo_device.updateStateOnServer(key=k, value=v)

                # Replicate to slaves
                if is_master:
                    self.logger.info(f"🧪 Replicating state updates to slave devices in the group for {indigo_device.name}")
                    self.updateStateOnSlaves(indigo_device)
            else:
                self.safe_debug(f"⚠️ No recognized state updates for {indigo_device.name}")

        except Exception as e:
            self.logger.error(f"❌ Error in soco_event_handler: {e}")









    #################################################################################################
    ### End - Event Handler to process soco state changes and retreive current dynamic state updates
    #################################################################################################



    def getSoCoDeviceByIP(self, ip_address):
        """
        Given an IP address, return the matching SoCo device object from known subscriptions.
        """
        try:
            for dev_id, subs in self.soco_subs.items():
                soco_obj = subs.get("soco")
                if soco_obj and soco_obj.ip_address == ip_address:
                    return soco_obj
        except Exception as e:
            self.logger.warning(f"⚠️ getSoCoDeviceByIP encountered an error: {e}")
        return None



    def getCoordinatorDevice(self, device):
        """
        Given an Indigo device, return the Indigo device object representing
        the group coordinator (master) for that device's group.
        If the device is the master, it returns itself.
        """
        try:
            zone_ip = device.address
            soco_device = self.getSoCoDeviceByIP(zone_ip)
            if not soco_device:
                self.logger.warning(f"⚠️ Could not resolve SoCo device for {device.name}")
                return device  # fallback: treat self as coordinator

            coordinator = soco_device.group.coordinator
            coordinator_ip = coordinator.ip_address

            # Find Indigo device matching the coordinator IP
            for dev in indigo.devices.iter("self"):
                if dev.address == coordinator_ip:
                    return dev

            self.logger.warning(f"⚠️ No Indigo device found matching coordinator IP {coordinator_ip}, returning self")
            return device  # fallback: treat self as coordinator

        except Exception as e:
            self.logger.error(f"❌ Error in getCoordinatorDevice: {e}")
            return device  # fallback: treat self as coordinator





    def soco_discover_and_subscribe(self):
        try:
            self.logger.info("🔍 Discovering Sonos devices on the network...")

            devices = soco.discover()
            for device in devices:
                if device.ip_address == indigo_device.address:
                    soco_device = device

            #devices = soco.discover()
            if not devices:
                self.logger.warning("❌ No Sonos devices discovered.")
                return

            self.logger.info(f"✅ Found {len(devices)} Sonos device(s). Subscribing to events...")

            for device in devices:
                try:
                    self.logger.info(f"   📻 Discovered {device.player_name} @ {device.ip_address}")

                    # 🔍 Match SoCo device to Indigo device by IP
                    matched_device = None
                    for dev in indigo.devices.iter("self"):
                        if dev.address == device.ip_address:
                            matched_device = dev
                            break

                    if matched_device:
                        self.safe_debug(f"   🔗 Matched to Indigo device {matched_device.name} (ID: {matched_device.id})")
                        self.socoSubscribe(matched_device, device)
                    else:
                        self.logger.warning(f"⚠️ No Indigo device found matching IP {device.ip_address}")

                except Exception as e:
                    self.logger.exception(f"❌ Error subscribing to {getattr(device, 'ip_address', 'unknown')}: {e}")

        except Exception as e:
            self.logger.exception("❌ Error during Sonos device discovery and subscription")



    ######################################################################################
    # Utiliies



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

    def updateStateOnServer(self, dev, state, value):
        try:
            if self.plugin.stateUpdatesDebug:
                self.safe_debug(f"\t Updating Device: {dev.name}, State: {state}, Value: {value}")
            GROUP_Coordinator = dev.states['GROUP_Coordinator']
            if GROUP_Coordinator == "false" and state in ZoneGroupStates:
                pass
            else:
                if value is None or value == "None":
                    dev.updateStateOnServer(state, "")
                else:
                    # self.logger.warning(f"State: '{state}', Value [Type = {type(value)}]: '{value}'")
                    dev.updateStateOnServer(state, value.encode('utf-8'))
                    # dev.updateStateOnServer(state, value)


            # Replicate states to slave ZonePlayers
            if state in ZoneGroupStates and dev.states['GROUP_Coordinator'] == "true" and dev.states['ZonePlayerUUIDsInGroup'].find(",") != -1:
                self.safe_debug("Replicate state to slave ZonePlayers...")
                ZonePlayerUUIDsInGroup = dev.states['ZonePlayerUUIDsInGroup'].split(',')
                for rdev in indigo.devices.iter("self.ZonePlayer"):
                    SlaveUID = rdev.states['ZP_LocalUID']
                    GROUP_Coordinator = rdev.states['GROUP_Coordinator']
                    if SlaveUID != dev.states['ZP_LocalUID'] and GROUP_Coordinator == "false" and SlaveUID in ZonePlayerUUIDsInGroup:
                        if state == "ZP_CurrentURI":
                            value = uri_group + dev.states['ZP_LocalUID']
                        if self.plugin.stateUpdatesDebug:
                            self.safe_debug(f"\t Updating Device: {rdev.name}, State: {state}, Value: {value}")
                        if value is None or value == "None":
                            rdev.updateStateOnServer(state, "")
                        else:
                            rdev.updateStateOnServer(state, value.encode('utf-8'))

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement




    import shutil
    import os


    def dump_groups_to_log(self):
        # Check if the SonosPlugin instance is properly initialized
        if not self.soco_by_ip:
            self.logger.warning("🚫 Sonos device map (soco_by_ip) is missing or not initialized.")
            return

        self.logger.info("📦 Dumping all currently grouped devices to the log...")

        # Iterate over all the devices in the SoCo device map
        seen_groups = set()  # To track already logged groups
        for dev in self.soco_by_ip.values():
            # Get the device IP
            device_ip = dev.ip_address
            # Retrieve the SoCo device object
            soco_device = dev

            # Ensure that the device has a valid group (and it is a coordinator or part of a group)
            if soco_device.group is None:
                self.logger.info(f"🧑‍💻 {dev.player_name} with IP {device_ip} is not part of any group.")
                continue

            # Check if the current device is the coordinator (master)
            group = soco_device.group
            coordinator = group.coordinator
            role = "Master (Coordinator)" if soco_device == coordinator else "Slave"

            # Avoid repeating the log for the same group
            if group in seen_groups:
                continue
            seen_groups.add(group)

            # List all devices in the group (including the master)
            devices_in_group = group.members

            # Add a space separator before the devices list and log the group details
            self.logger.info("\n🧑‍💻 Devices in group (ZonePlayerUUIDsInGroup): {[d.player_name for d in devices_in_group]}")

            # Print header after the group devices list for each group
            header = f"{'Device Name':<25} {'IP Address':<20} {'Role':<25} {'Indigo Device Name':<25} {'Indigo Device Number':<20}"
            self.logger.info(header)
            self.logger.info("=" * len(header))  # Print a separator line

            # Iterate through all devices in the group and log their information
            for rdev in devices_in_group:
                # Check the role (Coordinator or Slave)
                device_role = "Master (Coordinator)" if rdev == coordinator else "Slave"

                # Fetch the corresponding Indigo device for the slave (by IP)
                indigo_slave_device = None
                for indigo_device in indigo.devices:
                    if indigo_device.address == rdev.ip_address:
                        indigo_slave_device = indigo_device
                        break

                # Log if no corresponding Indigo device is found
                if not indigo_slave_device:
                    self.logger.warning(f"⚠️ No Indigo device found for slave device {rdev.player_name} with IP {rdev.ip_address}.")
                else:
                    # Format the row with more spacing and log it in a table format
                    row = f"{rdev.player_name:<25} {rdev.ip_address:<20} {device_role:<25} {indigo_slave_device.name:<25} {indigo_slave_device.id:<20}"
                    self.logger.info(row)

    def logger_accumulator_matrix(self, master_device, master_file_path, slave_devices, artwork_url=None, default_artwork=False):
        """
        Accumulates and logs detailed artwork processing steps for master and slave devices.
        
        Args:
            master_device (object): The master Sonos device.
            master_file_path (str): Path to the saved master artwork.
            slave_devices (list): List of slave devices to replicate artwork.
            artwork_url (str, optional): URL of the artwork (if available). Defaults to None.
            default_artwork (bool, optional): Flag to indicate if default artwork is used. Defaults to False.
        """
        
        # Check if master_device is valid and set ip_address to "tbd" if missing
        master_ip = getattr(master_device, 'ip_address', 'tbd')
        master_name = getattr(master_device, 'name', 'tbd')
        
        # Check if artwork_url and master_file_path are valid, set them to "tbd" if missing
        if not master_file_path:
            master_file_path = 'tbd'
        if not artwork_url:
            artwork_url = 'tbd'

        # Step 1: Log details about the stream file for the master device
        self.logger.info(f"——————————————————————————————————————————————————————————————————————————————————")
        self.logger.info(f"Stream file for the Master player {master_ip} (Name: {master_name}) art file was processed as art file name = {master_file_path} and stored in {master_file_path} as the base image.")
        
        # Step 2: Log the artwork saved as the master file
        if artwork_url != 'tbd':
            self.logger.info(f"This stream file was then saved in this directory - {master_file_path} with name= {master_ip} as the master file to be served")
        else:
            self.logger.info(f"Default artwork used. Master artwork saved in {master_file_path} for {master_ip}.")
        
        # Step 3: Log the artwork copied to each slave device
        for slave_device in slave_devices:
            # Set slave device info to "tbd" if missing
            slave_ip = getattr(slave_device, 'ip_address', 'tbd')
            slave_name = getattr(slave_device, 'name', 'tbd')
            
            # Use the correct path for slave artwork file
            slave_file_path = f"/Library/Application Support/Perceptive Automation/images/Sonos/{slave_ip}_art.jpg"
            
            if artwork_url != 'tbd':
                self.logger.info(f"This master file was then copied to this directory - {slave_file_path} with name= {slave_ip} as the slave {slave_ip} file to be served")
            else:
                self.logger.info(f"Default artwork used. Master file copied to slave {slave_name} ({slave_ip}) at {slave_file_path}")
        
        # End of the matrix
        self.logger.info(f"——————————————————————————————————————————————————————————————————————————————————")









    def updateStateOnSlaves(self, dev):
        try:
            self.safe_debug("Update all states to slave ZonePlayers...")

            ARTWORK_FOLDER = "/Library/Application Support/Perceptive Automation/images/Sonos/"
            DEFAULT_ARTWORK_PATH = ARTWORK_FOLDER + "default_artwork.jpg"
            DEFAULT_ARTWORK_SOURCE = "/Library/Application Support/Perceptive Automation/Indigo 2024.2/Plugins/Sonos.indigoPlugin/Contents/Server Plugin/default_artwork.jpg"
            MAX_DOWNLOAD_ATTEMPTS = 3

            os.makedirs(ARTWORK_FOLDER, exist_ok=True)

            # Ensure default artwork exists
            if not os.path.exists(DEFAULT_ARTWORK_PATH):
                try:
                    shutil.copy(DEFAULT_ARTWORK_SOURCE, DEFAULT_ARTWORK_PATH)
                    self.logger.info(f"✅ Default artwork copied to {DEFAULT_ARTWORK_PATH}")
                except Exception as e:
                    self.logger.error(f"❌ Failed to copy default artwork to {DEFAULT_ARTWORK_PATH}: {e}")

            device_ip = dev.address.strip()
            self.safe_debug(f"🧑‍💻 Device IP: {device_ip}")

            if device_ip in self.soco_by_ip:
                soco_device = self.soco_by_ip[device_ip]
                self.safe_debug(f"🧑‍💻 Found SoCo device for {dev.name} with IP {device_ip}")
            else:
                self.logger.warning(f"⚠️ No SoCo device found for IP {device_ip}")
                return

            group = soco_device.group
            coordinator = group.coordinator
            devices_in_group = group.members
            self.safe_debug(f"🧑‍💻 Devices in group: {[device.ip_address for device in devices_in_group]}")

            coordinator_ip = coordinator.ip_address.strip()
            coordinator_dev = None
            for indigo_device in indigo.devices:
                if indigo_device.address.strip() == coordinator_ip:
                    coordinator_dev = indigo_device
                    break

            self.logger.warning(f"🧪 Coordinator resolved: {coordinator_dev.name if coordinator_dev else 'None'} at IP {coordinator_ip}")

            master_artwork_file_path = None
            artwork_url = coordinator_dev.states.get('ZP_ART', None) if coordinator_dev else None
            self.logger.warning(f"🧪 Coordinator ZP_ART value: {artwork_url}")

            if artwork_url and not artwork_url.endswith("default.jpg"):
                for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
                    try:
                        response = requests.get(artwork_url, stream=True, timeout=5)
                        self.logger.warning(f"🧪 Artwork fetch attempt {attempt} HTTP status: {response.status_code}")

                        if response.status_code == 200:
                            master_artwork_file_path = f"{ARTWORK_FOLDER}sonos_art_{coordinator_dev.address}.jpg"
                            with open(master_artwork_file_path, 'wb') as f:
                                for chunk in response.iter_content(1024):
                                    f.write(chunk)

                            if os.path.exists(master_artwork_file_path):
                                artwork_size = os.path.getsize(master_artwork_file_path)
                                self.safe_debug(f"🖼️ Artwork saved on attempt {attempt} for master {coordinator_dev.name} at {master_artwork_file_path}, Size: {artwork_size} bytes")
                                break
                            else:
                                self.logger.warning(f"⚠️ Artwork file not saved properly on attempt {attempt}")
                        else:
                            self.logger.warning(f"⚠️ Artwork download failed (status {response.status_code}) on attempt {attempt}")
                    except Exception as e:
                        self.logger.error(f"❌ Exception during artwork download attempt {attempt}: {e}")

            if not master_artwork_file_path or not os.path.exists(master_artwork_file_path):
                self.logger.warning(f"⚠️ Master artwork unavailable; using default artwork.")
                master_artwork_file_path = DEFAULT_ARTWORK_PATH

            for rdev in devices_in_group:
                if rdev == coordinator:
                    self.safe_debug(f"🧑‍💻 Skipping coordinator: {rdev.player_name} (IP: {rdev.ip_address})")
                    continue

                self.safe_debug(f"🧑‍💻 Processing slave: {rdev.player_name} (IP: {rdev.ip_address})")

                indigo_slave_device = None
                for indigo_device in indigo.devices:
                    if indigo_device.address.strip() == rdev.ip_address.strip():
                        indigo_slave_device = indigo_device
                        break

                if not indigo_slave_device:
                    self.logger.warning(f"⚠️ No Indigo device found for slave {rdev.player_name} with IP {rdev.ip_address}, skipping.")
                    continue

                for state in list(ZoneGroupStates):
                    value = dev.states.get(state, "")
                    self.safe_debug(f"🧑‍💻 Updating slave {indigo_slave_device.name}, State: {state}, Value: {value}")
                    indigo_slave_device.updateStateOnServer(state, value)

                try:
                    slave_artwork_file_path = f"{ARTWORK_FOLDER}sonos_art_{indigo_slave_device.address}.jpg"
                    shutil.copy(master_artwork_file_path, slave_artwork_file_path)
                    self.safe_debug(f"🖼️ Copied master artwork to slave {indigo_slave_device.name} at {slave_artwork_file_path}")
                except Exception as e:
                    self.logger.error(f"❌ Error copying artwork to slave {indigo_slave_device.name}: {e}")

                indigo_slave_device.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{indigo_slave_device.address}.jpg")
                self.logger.info(f"🧑‍💻 Successfully updated slave: {indigo_slave_device.name} with IP: {indigo_slave_device.address}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)




















    import os
    import shutil
    import requests


    def copyStateFromMaster(self, dev):
        try:
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

        self.logger.warning("🧪 Starting getPandora()")
        self.logger.warning(f"🧪 Pandora flag: {self.pluginPrefs.get('Pandora')}")
        self.logger.warning(f"🧪 Email: {PandoraEmailAddress}")
        self.logger.warning(f"🧪 Password: {'***' if PandoraPassword else '(empty)'}")
        self.logger.warning(f"🧪 Nickname: {PandoraNickname}")
        self.safe_debug(f"✅ Sonos_Pandora currently has {len(Sonos_Pandora)} entries")

        # 🛡️ Validate credentials early
        if not PandoraEmailAddress or not PandoraPassword:
            self.logger.warning("⚠️ Missing Pandora email or password — skipping getPandora()")
            return

        try:
            list_count = 0
            pandora = Pandora()

            self.logger.warning("🧪 Calling Pandora.authenticate()...")
            result = pandora.authenticate(PandoraEmailAddress, PandoraPassword)
            self.logger.warning(f"🧪 Returned from authenticate(): {result}")

            if not result:
                self.logger.error("❌ Pandora authentication failed — skipping station fetch.")
                return

            self.logger.warning("🧪 Authentication successful — calling get_station_list()")
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
            global Sound_Files
            list_count = 0
            Sound_Files = []

            for f in listdir(self.SoundFilePath):
                if ".mp3" in f:
                    Sound_Files.append(f)
                    self.safe_debug(f"\tSound File: {f}")
                    list_count = list_count + 1

            self.logger.info(f"Loaded Sound Files... [{list_count}]")
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement




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

    def __init__(self, username, password):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
        self.username = username
        self.password = password
        self.playlists = {}
        self.channels = None
        #self.pluginPrefs = pluginPrefs

    @staticmethod
    def log(x):
        print('{} <SiriusXM>: {}'.format(datetime.datetime.now().strftime('%d.%b %Y %H:%M:%S'), x))

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
            self.log('Received status code {} for method \'{}\''.format(res.status_code, method))
            return None

        try:
            return res.json()
        except ValueError:
            self.log('Error decoding json for method \'{}\''.format(method))
            return None

    def post(self, method, postdata, authenticate=True):
        if authenticate and not self.is_session_authenticated() and not self.authenticate():
            self.log('Unable to authenticate')
            return None

        res = self.session.post(self.REST_FORMAT.format(method), data=json.dumps(postdata))
        if res.status_code != 200:
            self.log('Received status code {} for method \'{}\''.format(res.status_code, method))
            return None

        try:
            return res.json()
        except ValueError:
            self.log('Error decoding json for method \'{}\''.format(method))
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

        # get status
        try:
            status = data['ModuleListResponse']['status']
            message = data['ModuleListResponse']['messages'][0]['message']
            message_code = data['ModuleListResponse']['messages'][0]['code']
        except (KeyError, IndexError):
            self.log('Error parsing json response for playlist')
            return None

        # login if session expired
        if message_code == 201 or message_code == 208:
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
            self.log('Received error {} {}'.format(message_code, message))
            return None

        # get m3u8 url
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
            self.log('Received status code {} on playlist variant retrieval'.format(res.status_code))
            return None
        
        for x in res.text.split('\n'):
            if x.rstrip().endswith('.m3u8'):
                # first variant should be 256k one
                return '{}/{}'.format(url.rsplit('/', 1)[0], x.rstrip())
        
        return None

    def get_playlist(self, name, use_cache=True):
        guid, channel_id = self.get_channel(name)
        if not guid or not channel_id:
            self.log('No channel for {}'.format(name))
            return None

        url = self.get_playlist_url(guid, channel_id, use_cache)
        params = {
            'token': self.get_sxmak_token(),
            'consumer': 'k2',
            'gupId': self.get_gup_id(),
        }
        res = self.session.get(url, params=params)

        if res.status_code == 403:
            self.log('Received status code 403 on playlist, renewing session')
            return self.get_playlist(name, False)

        if res.status_code != 200:
            self.log('Received status code {} on playlist variant'.format(res.status_code))
            return None

        # add base path to segments
        base_url = url.rsplit('/', 1)[0]
        base_path = base_url[8:].split('/', 1)[1]
        lines = res.text.split('\n')
        for x in range(len(lines)):
            if lines[x].rstrip().endswith('.aac'):
                lines[x] = '{}/{}'.format(base_path, lines[x])
        return '\n'.join(lines)

    def get_segment(self, path, max_attempts=5):
        url = '{}/{}'.format(self.LIVE_PRIMARY_HLS, path)
        params = {
            'token': self.get_sxmak_token(),
            'consumer': 'k2',
            'gupId': self.get_gup_id(),
        }
        res = self.session.get(url, params=params)

        if res.status_code == 403:
            if max_attempts > 0:
                self.log('Received status code 403 on segment, renewing session')
                self.get_playlist(path.split('/', 2)[1], False)
                return self.get_segment(path, max_attempts - 1)
            else:
                self.log('Received status code 403 on segment, max attempts exceeded')
                return None

        if res.status_code != 200:
            self.log('Received status code {} on segment'.format(res.status_code))
            return None

        return res.content
    
    def get_channels(self):
        # download channel list if necessary
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
                return (None, None)
            try:
                self.channels = data['ModuleListResponse']['moduleList']['modules'][0]['moduleResponse']['contentData']['channelListing']['channels']
            except (KeyError, IndexError):
                self.log('Error parsing json response for channels')
                return []
        za = 0
        for za in self.channels[za]:
            print(za)
        x = self.channels[1]
        print(x.get('name', '').lower(), x.get('channelId', '').lower(), x.get('channelGuid', '').lower())         
        return self.channels

    def get_channel(self, name):
        name = name.lower()
        for x in self.get_channels():
            if x.get('name', '').lower() == name or x.get('channelId', '').lower() == name or x.get('siriusChannelNumber', '').lower() == name or x.get('channelGuid') == name:
                return (x['channelGuid'], x['channelId'])
        return (None, None)





    def process_album_art(self):
        self.logger.info("🧪 Running dynamic album art processing based on active subscriptions...")

        try:
            if not self.soco_subs:
                self.logger.warning("⚠️ No subscriptions found in self.soco_subs.")
                return

            # Iterate over all devices in self.soco_subs dynamically
            for dev_id, subs in self.soco_subs.items():
                try:
                    indigo_device = indigo.devices[int(dev_id)]
                    self.logger.info(f"🔍 Device: {indigo_device.name} ({indigo_device.address})")
                except Exception:
                    self.logger.warning(f"🔍 Device ID {dev_id} (not found in Indigo)")

                if not subs:
                    self.logger.warning("   ⚠️ No subscriptions registered for this device.")
                    continue

                # For each service (AVTransport, RenderingControl, etc.), process album art
                for service_name, sub in subs.items():
                    sid = getattr(sub, 'sid', 'no-sid')
                    self.logger.info(f"   🔔 Processing service: {service_name} | SID: {sid}")

                    # Retrieve player name and IP dynamically from subscription
                    device_name = indigo_device.name if indigo_device else f"Unknown device ({dev_id})"
                    zone_ip = indigo_device.address if indigo_device else "unknown"

                    # Log the processing for the player
                    self.safe_debug(f"🧪 Processing album art for player: {device_name} with IP: {zone_ip}")

                    # Try to retrieve track metadata for album art processing
                    meta = sub.variables.get("current_track_meta_data")  # Assuming `sub` has `variables` with track data
                    if meta:
                        self.safe_debug(f"🖼️ Found current_track_meta_data for player {device_name} — processing album art metadata.")
                        state_updates["ZP_TRACK"] = safe_call(getattr(meta, "title", ""))
                        state_updates["ZP_ARTIST"] = safe_call(getattr(meta, "creator", ""))
                        state_updates["ZP_ALBUM"] = safe_call(getattr(meta, "album", ""))
                        state_updates["ZP_DURATION"] = safe_call(getattr(meta, "duration", ""))

                        album_art_uri = safe_call(getattr(meta, "album_art_uri", ""))
                        if album_art_uri:
                            self.safe_debug(f"🖼️ Found album art URI for {device_name}: {album_art_uri}")
                            if album_art_uri.startswith("/"):
                                if zone_ip != "unknown":
                                    album_art_uri = f"http://{zone_ip}:1400{album_art_uri}"
                                    self.safe_debug(f"🖼️ Built album art URL using zone_ip: {album_art_uri}")
                                else:
                                    self.logger.warning("⚠️ Skipping album art URL generation — zone_ip unknown")
                                    album_art_uri = ""
                            elif album_art_uri.startswith("http://") or album_art_uri.startswith("https://"):
                                self.safe_debug(f"🖼️ Received full album art URL: {album_art_uri}")
                                # ✅ Attempt to download and localize
                                try:
                                    response = requests.get(album_art_uri, timeout=5)
                                    if response.status_code == 200:
                                        #artwork_path = f"/Library/Application Support/Perceptive Automation/Indigo 2024.2/IndigoWebServer/images/sonos_art_{zone_ip}.jpg"
                                        artwork_path = "/Library/Application Support/Perceptive Automation/images/Sonos/sonos_art_{zone_ip}.jpg"
                                        with open(artwork_path, "wb") as f:
                                            f.write(response.content)
                                        self.safe_debug(f"🖼️ Downloaded album art locally to {artwork_path}")
                                        album_art_uri = f"http://localhost:8888/sonos_art_{zone_ip}.jpg"
                                        self.logger.info(f"🖼️ Updated album art URI to: {album_art_uri}")
                                    else:
                                        self.logger.warning(f"⚠️ Failed to download album art. Status code: {response.status_code}")
                                except Exception as e:
                                    self.logger.error(f"❌ Error downloading album art: {e}")
                            else:
                                self.logger.warning(f"⚠️ Unexpected album_art_uri format: {album_art_uri} — clearing")
                                album_art_uri = ""
                        else:
                            self.safe_debug(f"🖼️ No album_art_uri present in current_track_meta_data")

                        if album_art_uri:
                            self.logger.debug(f"🖼️ Assigning album art for {device_name} — URL: {album_art_uri}")
                            state_updates["ZP_ART"] = album_art_uri
                        else:
                            self.safe_debug(f"🖼️ Skipping ZP_ART update — no valid album art URL for {device_name}")
                            # Fallback image
                            state_updates["ZP_ART"] = f"http://localhost:8888/sonos_art_{zone_ip}.jpg"
                            self.logger.debug(f"🖼️ Falling back to default image for {device_name}: {state_updates['ZP_ART']}")

                        state_updates["ZP_CurrentTrackURI"] = safe_call(getattr(meta, "uri", ""))
                    else:
                        self.logger.warning(f"⚠️ No current_track_meta_data or current_track found for {device_name} — no album art to process.")
                        # 🛡️ After everything, guarantee a valid ZP_ART even if missing
                        if not state_updates.get("ZP_ART"):
                            self.logger.warning(f"🖼️ No album art URI found for {device_name} — setting default placeholder")
                            state_updates["ZP_ART"] = f"http://localhost:8888/sonos_art_{zone_ip}.jpg"

        except Exception as e:
            self.logger.error(f"❌ Error during dynamic album art processing: {e}")

        
