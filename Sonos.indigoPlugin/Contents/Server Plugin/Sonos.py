#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import requirements  # Autolog additiom
from constants import *
import locale
import sys
import os
from os import listdir
import platform
import time
import socket
import subprocess
import traceback
import urllib
import urllib.parse
from urllib.request import urlopen
import urllib.request
import shutil
import json
import logging
from contextlib import closing
# import BaseHTTPServer
import http.server as BaseHTTPServer
# from SimpleHTTPServer import SimpleHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
from threading import Thread
from xml.etree import ElementTree as ET
import re

from AppKit import NSSpeechSynthesizer  # noqa
from AppKit import NSURL  # noqa

# sys.path.insert(1, "./lib")
import requests
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

# ============================== Custom Imports ===============================
try:
    import indigo  # noqa
except ImportError:
    pass

# ============================== Plugin Imports ===============================


import soco
from soco import config
from soco import SoCo

# from soco.music_services import MusicService


# try:
#     from .lib import soco
#     # import soco
#     from soco import config
#     from soco import SoCo
#     # from soco.music_services import MusicService
# except ImportError:
#     pass

try:
    from soco import events_twisted
    soco.config.EVENTS_MODULE = events_twisted
    # config.EVENTS_MODULE = events_twisted
except ImportError:
    pass

import language_codes

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

# used to bypass ZonePlayer updates for certain actions like Group Announcements
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

ZoneGroupStates = {'ZP_ALBUM', 'ZP_ARTIST', 'ZP_CREATOR', 'ZP_TRACK', 'ZP_NALBUM', 'ZP_NART', 'ZP_NARTIST', 'ZP_NCREATOR', 'ZP_NTRACK', 'ZP_CurrentTrack', 'ZP_CurrentTrackURI', 'ZP_DURATION',
                   'ZP_RELATIVE', 'ZP_INFO', 'ZP_STATION', 'ZP_STATE'}

IVONAlanguages = {'en-US': 'English, American',
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
                  'nb-NO': 'Norweigian'
                  }
# IVONAlanguages['en-US'] = 'English, American'

IVONAVoices = []
PollyVoices = []
NSVoices = []


class PA():
    def __init__(self, deviceId=None, props=None):
        self.deviceId = deviceId
        self.props = props


class SSDPListener(DatagramProtocol):
    def __init__(self, sonos_class_self):
        self.sonos_class_self = sonos_class_self
        a = 1

    def startProtocol(self):
        self.transport.setTTL(5)
        self.transport.joinGroup("239.255.255.250")
        # indigo.server.log("SSDP Listener Started...")
        self.sonos_class_self.logger.info("SSDP Listener Started...")

    def datagramReceived(self, data_bytes, address_port):
        address, port = address_port
        self.SSDPProcess(address, data_bytes)

    def SSDPProcess(self, address, data_bytes):
        try:
            message = {'address': address}

            data = data_bytes.decode("utf-8")

            if ("Sonos" in data) and ("NOTIFY" in data):
                # print(f"SSDPProcess data: {data}")
                for line in data.split('\r\n'):
                    if (len(line) > 0) and ("NOTIFY" not in line):
                        (item, value)  = line.split(': ')
                        message[item] = value

                for deviceId in self.sonos_class_self.deviceList:
                    dev = indigo.devices[int(deviceId)]
                    if dev.address == message["address"]:
                        if (dev.states["ZP_LocalUID"] == message["NT"][5:]) and (dev.states["ZP_LocalUID"] == message["USN"][5:]):
                            if message["NTS"] == "ssdp:byebye":
                                self.sonos_class_self.logger.error(f"[{time.asctime()}] Network Error, Disconnect from ZonePlayer: {dev.name}")
                                dev.setErrorStateOnServer("error")
                            elif message["NTS"] == "ssdp:alive":
                                self.sonos_class_self.updateStateOnServer(dev, "alive", time.asctime())
                                self.sonos_class_self.logger.debug(f"[{time.asctime()}] Received ALIVE message from ZonePlayer: {dev.name}")
                                # self.sonos_class_self.logger.info(f"[{time.asctime()}] Received ALIVE message from ZonePlayer: {dev.name}")
                                if int(message["X-RINCON-BOOTSEQ"]) != int(dev.states["bootseq"]):
                                    self.sonos_class_self.socoResubscribe(dev, message["X-RINCON-BOOTSEQ"])
                        break
        except Exception as exception_error:
            self.sonos_class_self.exception_handler(exception_error, True)  # Log error and display failing statement


class Sonos(object):

    ######################################################################################
    # class init & del
    def __init__(self, plugin, pluginPrefs):

        self.globals = plugin.globals  # Autolog additiom
        self.logger = logging.getLogger("Plugin.Sonos")  # Autolog additiom

        self.plugin = plugin
        self.EventProcessor = None
        self.EventIP = None
        self.EventCheck = None
        self.SubscriptionCheck = None
        self.HTTPStreamingIP = None
        self.HTTPStreamingPort = None
        self.HTTPStreamerOn = None
        self.httpd = None
        self.SoundFilePath = None
        self.rootZPIP = None
        self.Pandora = None
        self.PandoraEmailAddress = None
        self.PandoraPassword = None
        self.PandoraNickname = None
        self.Pandora2 = None
        self.PandoraEmailAddress2 = None
        self.PandoraPassword2 = None
        self.PandoraNickname2 = None
        self.SiriusXM = None
        self.SiriusXMID = None
        self.SiriusXMPassword = None
        self.IVONA = None
        self.IVONAaccessKey = None
        self.IVONAsecretKey = None
        self.Polly = None
        self.PollyaccessKey = None
        self.PollysecretKey = None
        self.MSTranslate = None
        self.MSTranslateClientID = None
        self.MSTranslateClientSecret = None
        self.ttsORfile = None
        self.deviceList = []
        self.ZonePlayers = []
        self.ZPTypes = []

        self.SonArray = [{}]
        self.HTTPServer = None
        self.control_point = None

        self.soco_sub = {}
        self.event_threads = {}

        self.MSTranslateVoices = {}
        self.myLocale = None

        self.zonePlayerState = {}
        self.SonosDeviceID = None

        if platform.machine() == "x86_64":
            self.lame_platform_folder = "intel"
        else:
            self.lame_platform_folder = "apple_silicon"

        self.optional_packages_checked = plugin.optional_packages_checked  # List of optional packages already checked

        # Set Plugin Config Values - Autolog additiom
        self.closedPrefsConfigUi(pluginPrefs, False)  # Autolog additiom

    def __del__(self):
        pass

    def exception_handler(self, exception_error_message, log_failing_statement):
        filename, line_number, method, statement = traceback.extract_tb(sys.exc_info()[2])[-1]
        module = filename.split('/')
        log_message = f"'{exception_error_message}' in module '{module[-1]}', method '{method} [{self.globals[PLUGIN_INFO][PLUGIN_VERSION]}]'"
        if log_failing_statement:
            log_message = log_message + f"\n   Failing statement [line {line_number}]: '{statement}'"
        else:
            log_message = log_message + f" at line {line_number}"
        self.logger.error(log_message)

    def startup(self):
        try:
            global NSVoices

            self.logger.debug("Sonos Plugin Startup...")

            logging.getLogger("requests").setLevel(logging.WARNING)
            # logging.getLogger("soco").setLevel(logging.INFO)

            if os.path.exists('/Library/Application Support/Perceptive Automation/images/Sonos') == 0:
                os.makedirs('/Library/Application Support/Perceptive Automation/images/Sonos')

            self.closedPrefsConfigUi(None, None)

            try:
                NSVoices = NSSpeechSynthesizer.availableVoices()
                self.logger.info(f"Loaded Apple Voices.. [{len(NSVoices)}]")
            except Exception as exception_error:
                self.logger.error(f"[{time.asctime()}] Cannot load Apple Voices.")

            # self.plugin.updater.checkVersionPoll()

            reactor.listenMulticast(1900, SSDPListener(self), listenMultiple=True)  # noqa
            soco.config.EVENT_LISTENER_IP = self.EventIP

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def shutdown(self):
        try:
            self.HTTPStreamerOn = False
            if self.EventProcessor == "SoCo":
                self.logger.info("SoCo Reactor Landing...")
                if reactor.running:  # noqa
                    try:
                        reactor.stop()  # noqa
                    except Exception as exception_error:
                        pass

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def deviceStartComm(self, device):
        try:
            self.logger.debug(f"ZonePlayer: {device.name}, Enabled: {device.enabled}")
            if device.id not in self.deviceList:
                self.deviceList.append(device.id)
                device.stateListOrDisplayStateIdChanged()
                self.initZones(device)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def deviceStopComm(self, device):
        try:
            self.logger.debug(f"Stopping device: {device.name} ")
            if device.id in self.deviceList:
                self.deviceList.remove(device.id)
                if self.EventProcessor == "SoCo":
                    self.socoUnsubscribe(device)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def SoCoReactor(self):
        try:
            self.logger.info("SoCo Reactor Ignition...")
            reactor.run(installSignalHandlers=0)  # noqa

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

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

    ######################################################################################
    # Concurrent Thread Start

    def runConcurrentThread(self):
        try:
            self.logger.debug("Running Concurrent Thread")

            if self.EventProcessor == "SoCo":
                # x = Thread(target=self.SoCoReactor, daemon=True)
                # x.setDaemon(True)
                x = Thread(target=self.SoCoReactor)
                x.setDaemon(True)
                x.start()

            # updateTime = time.time()
            eventTime = time.time()
            subTestTime = time.time()
            relTime = time.time()

            while not self.plugin.StopThread:

                # if time.time() - updateTime >= 3600:
                #     updateTime = time.time()
                #     self.plugin.updater.checkVersionPoll()

                if time.time() - eventTime >= int(self.EventCheck):
                    eventTime = time.time()
                    self.checkEvents()

                if time.time() - subTestTime >= int(self.SubscriptionCheck):
                    subTestTime = time.time()
                    self.socoSubTest()

                if time.time() - relTime >= 1:
                    relTime = time.time()
                    self.updateRelTime()

                self.plugin.sleep(0.1)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def restartPlugin(self):
        try:
            self.logger.info("Restarting Sonos Plugin...")
            self.plugin.stopConcurrentThread()
            SonosPlug = indigo.server.getPlugin("com.ssi.indigoplugin.Sonos")
            SonosPlug.restart(waitUntilDone=True)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def stopConcurrentThread(self):
        try:
            self.logger.debug("Stopping Concurrent Thread")
            self.plugin.StopThread = True

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def checkEvents(self):
        try:
            timeout = (15 * 60) + 10
            for item in self.deviceList:
                dev = indigo.devices[item]
                try:
                    if time.time() - time.mktime(time.strptime(dev.states["alive"], "%a %b %d %H:%M:%S %Y")) > timeout:
                        self.logger.error(f"[{time.asctime()}] ZonePlayer: {dev.name} has fallen off the network.")
                        dev.setErrorStateOnServer("error")
                        self.socoTimeout(dev)
                except Exception as exception_error:
                    dev.setErrorStateOnServer("error")
                    self.socoTimeout(dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # Check for messages

    def initZones(self, dev):
        try:
            zoneIP = dev.pluginProps["address"]
            self.logger.debug(f"Resetting States for zone: {zoneIP}")
            self.updateStateOnServer(dev, "ZP_ALBUM", "")
            self.updateStateOnServer(dev, "ZP_ART", "")
            self.updateStateOnServer(dev, "ZP_ARTIST", "")
            self.updateStateOnServer(dev, "ZP_CREATOR", "")
            self.updateStateOnServer(dev, "ZP_CurrentURI", "")
            self.updateStateOnServer(dev, "ZP_DURATION", "")
            self.updateStateOnServer(dev, "ZP_RELATIVE", "")
            self.updateStateOnServer(dev, "ZP_INFO", "")
            self.updateStateOnServer(dev, "ZP_MUTE", "")
            self.updateStateOnServer(dev, "ZP_STATE", "")
            self.updateStateOnServer(dev, "ZP_STATION", "")
            self.updateStateOnServer(dev, "ZP_TRACK", "")
            self.updateStateOnServer(dev, "ZP_VOLUME", "")
            self.updateStateOnServer(dev, "ZP_VOLUME_FIXED", "")
            self.updateStateOnServer(dev, "ZP_BASS", "")
            self.updateStateOnServer(dev, "ZP_TREBLE", "")
            self.updateStateOnServer(dev, "ZP_ZoneName", "")
            self.updateStateOnServer(dev, "ZP_LocalUID", "")
            self.updateStateOnServer(dev, "ZP_AIName", "")
            self.updateStateOnServer(dev, "ZP_AIPath", "")
            self.updateStateOnServer(dev, "ZP_NALBUM", "")
            self.updateStateOnServer(dev, "ZP_NART", "")
            self.updateStateOnServer(dev, "ZP_NARTIST", "")
            self.updateStateOnServer(dev, "ZP_NCREATOR", "")
            self.updateStateOnServer(dev, "ZP_NTRACK", "")
            self.updateStateOnServer(dev, "Q_Crossfade", "off")
            self.updateStateOnServer(dev, "Q_Repeat", "off")
            self.updateStateOnServer(dev, "Q_RepeatOne", "off")
            self.updateStateOnServer(dev, "Q_Shuffle", "off")
            self.updateStateOnServer(dev, "Q_Number", "0")
            self.updateStateOnServer(dev, "Q_ObjectID", "")
            self.updateStateOnServer(dev, "GROUP_Coordinator", "")
            self.updateStateOnServer(dev, "GROUP_Name", "")
            self.updateStateOnServer(dev, "ZP_CurrentTrack", "")
            self.updateStateOnServer(dev, "ZP_CurrentTrackURI", "")
            self.updateStateOnServer(dev, "ZoneGroupID", "")
            self.updateStateOnServer(dev, "ZoneGroupName", "")
            self.updateStateOnServer(dev, "ZonePlayerUUIDsInGroup", "")
            self.updateStateOnServer(dev, "alive", "")
            self.updateStateOnServer(dev, "bootseq", "")

            url = "http://" + zoneIP + ":1400/status/zp"
            try:
                response = requests.get(url)
                root = ET.fromstring(response.content)
                ZoneName = root.findtext('.//ZoneName')
                LocalUID = root.findtext('.//LocalUID')
                SerialNumber = root.findtext('.//SerialNumber')
            except Exception as exception_error:
                self.logger.error(f"Error getting ZonePlayer data: {url}")
                self.logger.error(f"  Offending ZonePlayer: {dev.name}")
                self.logger.error("  ZonePlayer may be physically turned off or in a bad state.")
                self.logger.error("  Please disable communications or remove from Indigo.")
                self.deviceList.remove(dev.id)
                dev.setErrorStateOnServer("error")
                return

            # Allow for special characters in ZoneName
            self.updateStateOnServer(dev, "ZP_ZoneName", ZoneName)
            self.updateStateOnServer(dev, "ZP_LocalUID", LocalUID)
            self.updateStateOnServer(dev, "SerialNumber", SerialNumber)

            self.getModelName(dev)

            self.updateZoneGroupStates(dev)
            self.updateZoneTopology(dev)

            self.logger.info(f"Adding ZonePlayer: {zoneIP}, {LocalUID}, {dev.name}")
            self.ZonePlayers.append(LocalUID)
            self.ZPTypes.append([LocalUID, dev.pluginProps["model"]])

            self.zonePlayerState[dev.id] = {'zonePlayerAlive': True}
            self.updateStateOnServer(dev, "alive", time.asctime())

            if self.EventProcessor == "SoCo":
                self.socoSubscribe(dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def socoTimeout(self, dev):
        try:
            self.logger.error(f"[{time.asctime()}] Resubscription due to timeout for ZonePlayer: {dev.name}")
            self.socoUnsubscribe(dev)
            self.socoSubscribe(dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def socoSubTest(self):
        try:
            for item in self.deviceList:
                dev = indigo.devices[item]
                subStatus = True
                if not self.soco_sub[dev.id]['avTransport'].is_subscribed:
                    self.logger.debug(f"[{time.asctime()}] [{dev.name}]: avTransport subscription failed.  Resubscribing...")
                    subStatus = False
                if not self.soco_sub[dev.id]['renderingControl'].is_subscribed:
                    self.logger.debug(f"[{time.asctime()}] [{dev.name}]: renderingControl subscription failed.  Resubscribing...")
                    subStatus = False
                if not self.soco_sub[dev.id]['zoneGroupTopology'].is_subscribed:
                    self.logger.debug(f"[{time.asctime()}] [{dev.name}]: zoneGroupTopology subscription failed.  Resubscribing...")
                    subStatus = False
                if not self.soco_sub[dev.id]['queue'].is_subscribed:
                    self.logger.debug(f"[{time.asctime()}] [{dev.name}]: queue subscription failed.  Resubscribing...")
                    subStatus = False
                if not self.soco_sub[dev.id]['groupRenderingControl'].is_subscribed:
                    self.logger.debug(f"[{time.asctime()}] [{dev.name}]: groupRenderingControl subscription failed.  Resubscribing...")
                    subStatus = False
                if not self.soco_sub[dev.id]['contentDirectory'].is_subscribed:
                    self.logger.debug(f"[{time.asctime()}] [{dev.name}]: contentDirectory subscription failed.  Resubscribing...")
                    subStatus = False
                # if not self.soco_sub[dev.id]['groupManagement'].is_subscribed:
                #     self.logger.debug(f"[{time.asctime()}] [{dev.name}]: groupManagement subscription failed.  Resubscribing...")
                #     subStatus = False
                if int(dev.pluginProps["model"]) in [SONOS_CONNECT, SONOS_CONNECTAMP, SONOS_PLAY5, SONOS_ERA100, SONOS_ERA300]:
                    if not self.soco_sub[dev.id]['audioIn'].is_subscribed:
                        self.logger.debug(f"[{time.asctime()}] [{dev.name}]: audioIn subscription failed.  Resubscribing...")
                        subStatus = False
                if not subStatus:
                    self.socoUnsubscribe(dev)
                    self.socoSubscribe(dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def socoResubscribeAll(self):
        try:
            for item in self.deviceList:
                dev = indigo.devices[item]
                self.socoUnsubscribe(dev)
                self.socoSubscribe(dev)
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def socoResubscribe(self, dev, bootseq):
        try:
            self.logger.error(f"[{time.asctime()}] Network Error causing resubscription (bootseq={dev.states['bootseq']},{bootseq}) for ZonePlayer: {dev.name}")
            self.updateStateOnServer(dev, "bootseq", bootseq)
            self.socoUnsubscribe(dev)
            self.socoSubscribe(dev)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def socoSubscribe(self, dev):
        try:
            # self.soco_sub[dev.id] = {'soco_dev': SoCo(dev.address),
            #                          'avTransport': SoCo(dev.address).avTransport.subscribe(requested_timeout=600, auto_renew=True).subscription,
            #                          'renderingControl': SoCo(dev.address).renderingControl.subscribe(requested_timeout=600, auto_renew=True).subscription,
            #                          'zoneGroupTopology': SoCo(dev.address).zoneGroupTopology.subscribe(requested_timeout=600, auto_renew=True).subscription,
            #                          'queue': SoCo(dev.address).queue.subscribe(requested_timeout=600, auto_renew=True).subscription,
            #                          'groupRenderingControl': SoCo(dev.address).groupRenderingControl.subscribe(requested_timeout=600, auto_renew=True).subscription,
            #                          'contentDirectory': SoCo(dev.address).contentDirectory.subscribe(requested_timeout=600, auto_renew=True).subscription,
            #                          'groupManagement': SoCo(dev.address).groupManagement.subscribe(requested_timeout=600, auto_renew=True).subscription}

            # print (SoCo(dev.address).__dict__)
            attributes = SoCo(dev.address).__dict__
            for key, value in attributes.items():
                print(f"$ {key}:")
                try:
                    for key2, value2 in value.__dict__.items():
                        print(f"$     {key2}:  {value2}")
                except Exception as exception_error:
                    try:
                        print(f"$     {value}:")
                    except Exception as exception_error:
                        pass

            self.soco_sub[dev.id] = {'soco_dev': SoCo(dev.address),
                                     'avTransport': SoCo(dev.address).avTransport.subscribe(requested_timeout=600, auto_renew=True).subscription,
                                     'renderingControl': SoCo(dev.address).renderingControl.subscribe(requested_timeout=600, auto_renew=True).subscription,
                                     'zoneGroupTopology': SoCo(dev.address).zoneGroupTopology.subscribe(requested_timeout=600, auto_renew=True).subscription,
                                     'queue': SoCo(dev.address).queue.subscribe(requested_timeout=600, auto_renew=True).subscription,
                                     'groupRenderingControl': SoCo(dev.address).groupRenderingControl.subscribe(requested_timeout=600, auto_renew=True).subscription,
                                     # 'groupManagement': SoCo(dev.address).GroupManagement.subscribe(requested_timeout=600, auto_renew=True).subscription,
                                     'contentDirectory': SoCo(dev.address).contentDirectory.subscribe(requested_timeout=600, auto_renew=True).subscription}

            if int(dev.pluginProps["model"]) in [SONOS_CONNECT, SONOS_CONNECTAMP, SONOS_PLAY5, SONOS_ERA100, SONOS_ERA300]:
                self.soco_sub[dev.id]['audioIn'] = SoCo(dev.address).audioIn.subscribe(requested_timeout=600, auto_renew=True).subscription

            self.soco_sub[dev.id]['avTransport'].callback = self.soco_events
            self.soco_sub[dev.id]['renderingControl'].callback = self.soco_events
            self.soco_sub[dev.id]['zoneGroupTopology'].callback = self.soco_events
            self.soco_sub[dev.id]['queue'].callback = self.soco_events
            self.soco_sub[dev.id]['groupRenderingControl'].callback = self.soco_events
            self.soco_sub[dev.id]['contentDirectory'].callback = self.soco_events
            # self.soco_sub[dev.id]['groupManagement'].callback = self.soco_events
            if int(dev.pluginProps["model"]) in [SONOS_CONNECT, SONOS_CONNECTAMP, SONOS_PLAY5, SONOS_ERA100, SONOS_ERA300]:
                self.soco_sub[dev.id]['audioIn'].callback = self.soco_events

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def socoUnsubscribe(self, dev):
        try:
            self.logger.debug(f"[{time.asctime()}] Unsubscribing to ZonePlayer: {dev.name}")
            try: 
                self.soco_sub[dev.id]['avTransport'].unsubscribe()
            except Exception as exception_error: 
                self.logger.debug(f"Cannot unsubscribe from avTransport events for ZonePlayer: {dev.name}")
            try: 
                self.soco_sub[dev.id]['renderingControl'].unsubscribe()
            except Exception as exception_error: 
                self.logger.debug(f"Cannot unsubscribe from renderingControl events for ZonePlayer: {dev.name}")
            try: 
                self.soco_sub[dev.id]['zoneGroupTopology'].unsubscribe()
            except Exception as exception_error: 
                self.logger.debug(f"Cannot unsubscribe from zoneGroupTopology events for ZonePlayer: {dev.name}")
            try: 
                self.soco_sub[dev.id]['queue'].unsubscribe()
            except Exception as exception_error: 
                self.logger.debug(f"Cannot unsubscribe from queue events for ZonePlayer: {dev.name}")
            try: 
                self.soco_sub[dev.id]['groupRenderingControl'].unsubscribe()
            except Exception as exception_error: 
                self.logger.debug(f"Cannot unsubscribe from groupRenderingControl events for ZonePlayer: {dev.name}")
            try: 
                self.soco_sub[dev.id]['contentDirectory'].unsubscribe()
            except Exception as exception_error: 
                self.logger.debug(f"Cannot unsubscribe from contentDirectory events for ZonePlayer: {dev.name}")
            # try: 
            #     self.soco_sub[dev.id]['groupManagement'].unsubscribe()
            # except Exception as exception_error: self.logger.debug(f"Cannot unsubscribe from groupManagement events for ZonePlayer: {dev.name}")
            if int(dev.pluginProps["model"]) in [SONOS_CONNECT, SONOS_CONNECTAMP, SONOS_PLAY5, SONOS_ERA100, SONOS_ERA300]:
                try: 
                    self.soco_sub[dev.id]['audioIn'].unsubscribe()
                except Exception as exception_error: 
                    self.logger.debug(f"Cannot unsubscribe from audioIn events for ZonePlayer: {dev.name}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getModelName(self, dev):
        try:
            url = f"http://{dev.pluginProps['address']}:1400/xml/device_description.xml"
            response = requests.get(url)
            if response.ok:
                root = ET.fromstring(response.content)
                ModelName = root.findtext('.//{urn:schemas-upnp-org:device-1-0}displayName')
                self.updateStateOnServer(dev, "ModelName", ModelName)
            else:
                self.logger.error(f"[{time.asctime()}] Cannot get ModelName for ZonePlayer: {dev.name}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def updateZoneTopology(self, dev):
        try:
            # # Deprecated in Sonos 10.1
            # url = "http://" + dev.pluginProps["address"] + ":1400/status/topology"
            # response = requests.get(url)
            # if response.ok:
            # 	root = ET.fromstring(response.content)
            # 	for ZonePlayer in root.findall("./ZonePlayers/ZonePlayer"):
            # 		if ZonePlayer.get('uuid') == dev.states['ZP_LocalUID']:
            # 			self.updateStateOnServer (dev, "GROUP_Coordinator", ZonePlayer.get('coordinator'))
            # 			self.updateStateOnServer (dev, "bootseq", ZonePlayer.get('bootseq'))
            # else:
            #    self.logger.error(f"[{time.asctime()}] Cannot get ZoneGroupTopology for ZonePlayer: {dev.name}")

            res = self.restoreString(self.SOAPSend(self.rootZPIP, "/ZonePlayer", "/ZoneGroupTopology", "GetZoneGroupState", ""), 1)
            ZGS = ET.fromstring(res)
            for ZoneGroup in ZGS.findall('.//ZoneGroup'):
                for ZonePlayer in ZoneGroup.findall('.//ZoneGroupMember'):
                    if ZonePlayer.attrib['UUID'] == dev.states['ZP_LocalUID']:
                        if ZonePlayer.attrib['UUID'] == ZoneGroup.attrib['Coordinator']:
                            self.updateStateOnServer(dev, "GROUP_Coordinator", 'true')
                        else:
                            self.updateStateOnServer(dev, "GROUP_Coordinator", 'false')
                        self.updateStateOnServer(dev, "GROUP_Name", ZoneGroup.attrib['ID'])
                        self.updateStateOnServer(dev, "bootseq", ZonePlayer.attrib['BootSeq'])

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def updateZoneGroupStates(self, dev):
        try:
            zoneIP = dev.pluginProps["address"]
            res = self.SOAPSend(zoneIP, "/ZonePlayer", "/ZoneGroupTopology", "GetZoneGroupAttributes", "")
            self.updateStateOnServer(dev, "ZoneGroupName", self.parseCurrentZoneGroupName(res))
            self.updateStateOnServer(dev, "ZoneGroupID", self.parseCurrentZoneGroupID(res))
            self.updateStateOnServer(dev, "ZonePlayerUUIDsInGroup", self.parseCurrentZonePlayerUUIDsInGroup(res))

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def updateRelTime(self):
        try:
            for item in self.deviceList:
                dev = indigo.devices[item]
                if dev.states["GROUP_Coordinator"] == "true" and dev.states["ZP_STATE"] == "PLAYING":
                    self.updateStateOnServer(dev, "ZP_RELATIVE", self.parseRelTime(dev, self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport", "GetPositionInfo", "")))

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def IVONAVoices(self):
        try:
            global IVONAVoices
            id = 0
            IVONAjson = json.load(open('pyvona.json'))

            IVONAgender = None
            IVONAlanguage = None
            IVONAname = None

            for majorkey, subdict in IVONAjson.items():
                for line in subdict:
                    # self.logger.info(f"line: {line}")
                    for subkey, value in line.items():
                        match subkey:
                            case "Gender":
                                IVONAgender = value
                            case "Language":
                                IVONAlanguage = value
                            case "Name":
                                IVONAname = value
                            case _:
                                pass
                    if IVONAgender is None or IVONAlanguage is None or IVONAname is None:
                        pass  # TODO: Log error
                    else:
                        IVONAVoices.append([id, IVONAname, IVONAgender, IVONAlanguage, IVONAlanguages[IVONAlanguage]])
                        self.logger.debug(f"\tIVONA: {id}|{IVONAlanguages[IVONAlanguage]}|{IVONAname}")
                        id = id + 1
            self.logger.info(f"Loaded IVONA Voices... [{id}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def PollyVoices(self):
        try:
            global PollyVoices
            id = 0
            client = boto3.client("polly", aws_access_key_id=self.PollyaccessKey, aws_secret_access_key=self.PollysecretKey, region_name="us-east-1")
            content = client.describe_voices()
            response = int(content["ResponseMetadata"]["HTTPStatusCode"])
            if response == 200:
                voices = content["Voices"]
                for voice in voices:
                    PollyVoices.append([voice["Id"], voice["Name"], voice["Gender"], voice["LanguageCode"], voice["LanguageName"]])
                    self.logger.debug(f"\tPolly: {voice['Id']}|{voice['LanguageName']}|{voice['Name']}")
                    id = id + 1
                self.logger.info(f"Loaded Polly Voices... [{id}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def SOAPSend(self, zoneIP, soapRoot, soapBranch, soapAction, soapPayload):
        try:
            if soapBranch == "/Queue":
                urn = "schemas-sonos-com"
            else:
                urn = "schemas-upnp-org"

            self.logger.debug(f"zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")

            # SM_TEMPLATE = f"""<?xml version="1.0" encoding="utf-8"?><s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ns0:{soapAction} xmlns:ns0=\"urn:{urn}:service:{soapBranch[1:]}:1\"><InstanceID>0</InstanceID>{soapPayload}</ns0:{soapAction}></s:Body></s:Envelope>"""

            # Convert soapPayload to a string if currently bytes
            if isinstance(soapPayload, bytes):
                soapPayload = soapPayload.decode("utf-8")

            SM_TEMPLATE = (
                    '<?xml version="1.0" encoding="utf-8"?>'
                    '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
                    '<s:Body>'
                    '<ns0:' + soapAction + ' xmlns:ns0="urn:' + urn + ':service:' + soapBranch[1:] + ':1">'
                                                                                                     '<InstanceID>0</InstanceID>'
                    + soapPayload +
                    '</ns0:' + soapAction + '>'
                                            '</s:Body>'
                                            '</s:Envelope>')

            SoapMessage = SM_TEMPLATE

            base_url = f"http://{zoneIP}:1400"

            if soapRoot == "/ZonePlayer":
                control_url = f"{soapBranch}/Control"
            else:
                control_url = f"{soapRoot}{soapBranch}/Control"

            soap_action = f"urn:{urn}:service:{soapBranch[1:]}:1#{soapAction}"
            headers = {'Content-Type': 'text/xml; charset="utf-8"',	'Content-Length': str(len(SoapMessage)), 'Host': zoneIP + ':1400', 'User-Agent': 'Indigo', 'SOAPACTION': soap_action}

            try:
                response = requests.post(base_url + control_url, headers=headers, data=SoapMessage.encode("utf-8"))
            except Exception as exception_error:
                self.logger.error(f"SOAPSend Error: {exception_error}")

            res_bytes = response.text.encode("utf-8")
            res = res_bytes.decode("utf-8")
            status = response.status_code
            if status != 200:
                try:
                    errorCode = self.parseErrorCode(res)
                    self.logger.error(f"UPNP Error: {UPNP_ERRORS[errorCode]}")
                except Exception as exception_error:
                    self.logger.error(f"UPNP Error: {status}")
                self.logger.error(f"Offending Command -> zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")
                self.logger.error(f"Error Response: {res}")  # TODO: Revert to Debug

            # reconstruct multi-line strings
            # discovered in Sonos beta firmware
            resx = ""

            for line in res.splitlines():
                # f = open ('beta.txt')
                # for line in iter(f):
                #     self.logger.info (f"line: {line}")
                if len(line) <= 5:
                    try:
                        if int(line, 16) >= 0 and int(line, 16) <= 4096:
                            pass
                        else:
                            resx = resx + line.rstrip('\n')
                    except Exception as exception_error:
                        pass
                else:
                    resx = resx + line.rstrip('\n')

            if self.plugin.xmlDebug:
                self.logger.debug(SoapMessage)
                self.logger.debug(resx)

            return resx

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_events(self, soco_event):
        try:
            deviceFound = False
            for deviceId in self.deviceList:
                if soco_event.service.soco.ip_address == indigo.devices[int(deviceId)].address:
                    dev = indigo.devices[int(deviceId)]
                    deviceFound = True
                    break
            if not deviceFound:
                self.logger.error(f"[{time.asctime()}] Cannot find Indigo device for ZonePlayer: {soco_event.service.soco.ip_address}")
                return

            service = soco_event.service.service_type

            match service:
                case "AVTransport":
                    self.soco_event_av_transport(dev, soco_event)
                case "RenderingControl":
                    self.soco_event_rendering_control(dev, soco_event)
                case "Queue":
                    self.soco_event_queue(dev, soco_event)
                case "GroupRenderingControl":
                    self.soco_event_group_rendering_control(dev, soco_event)
                case "ContentDirectory":
                    self.soco_event_content_directory(dev, soco_event)
                # case "GroupManagement":
                #     self.soco_event_group_management(dev, soco_event)
                case "ZoneGroupTopology":
                    self.soco_event_zone_group_topology(dev, soco_event)
                case "AudioIn":
                    self.soco_event_audio_in(dev, soco_event)
                case _:
                    self.logger.error(f"Unhandled Service tpe: {service}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_av_transport(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo AVTransport] {soco_event.variables}")

            # insures topology updates if AVTransport event received before Group event
            self.updateZoneGroupStates(dev)
            self.updateZoneTopology(dev)

            try:
                val = soco_event.variables["transport_state"]
                if val == "PAUSED_PLAYBACK":
                    val = "PAUSED"
                self.updateStateOnServer(dev, "ZP_STATE", val)
            except Exception as exception_error:
                pass
            try:
                val = soco_event.variables["current_play_mode"]
                match val:
                    case "NORMAL":
                        self.updateStateOnServer(dev, "Q_Repeat", "off")
                        self.updateStateOnServer(dev, "Q_RepeatOne", "off")
                        self.updateStateOnServer(dev, "Q_Shuffle", "off")
                    case "REPEAT_ALL":
                        self.updateStateOnServer(dev, "Q_Repeat", "on")
                        self.updateStateOnServer(dev, "Q_RepeatOne", "off")
                        self.updateStateOnServer(dev, "Q_Shuffle", "off")
                    case "REPEAT_ONE":
                        self.updateStateOnServer(dev, "Q_Repeat", "off")
                        self.updateStateOnServer(dev, "Q_RepeatOne", "on")
                        self.updateStateOnServer(dev, "Q_Shuffle", "off")
                    case "SHUFFLE_NOREPEAT":
                        self.updateStateOnServer(dev, "Q_Repeat", "off")
                        self.updateStateOnServer(dev, "Q_RepeatOne", "off")
                        self.updateStateOnServer(dev, "Q_Shuffle", "on")
                    case "SHUFFLE":
                        self.updateStateOnServer(dev, "Q_Repeat", "on")
                        self.updateStateOnServer(dev, "Q_RepeatOne", "off")
                        self.updateStateOnServer(dev, "Q_Shuffle", "on")
                    case "SHUFFLE_REPEAT_ONE":
                        self.updateStateOnServer(dev, "Q_Repeat", "off")
                        self.updateStateOnServer(dev, "Q_RepeatOne", "on")
                        self.updateStateOnServer(dev, "Q_Shuffle", "on")
            except Exception as exception_error:
                pass
            try:
                val = soco_event.variables["current_crossfade_mode"]
                if val == "0":
                    self.updateStateOnServer(dev, "Q_Crossfade", "off")
                elif val == "1":
                    self.updateStateOnServer(dev, "Q_Crossfade", "on")
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_CurrentTrack", soco_event.variables["current_track"])
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_CurrentTrackURI", soco_event.variables["current_track_uri"])
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_CurrentURI", soco_event.variables["av_transport_uri"])
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_DURATION", soco_event.variables["current_track_duration"])
            except Exception as exception_error:
                pass

            try:
                val = soco_event.variables["current_track_meta_data"]
                if val == "":
                    val = None
                try:
                    if uri_radio not in dev.states["ZP_CurrentURI"]:
                        # self.logger.info(f"ZP_TRACK val [Type = {type(val)}, Length = {len(val)}]: '{val}'")
                        title = val.title
                        self.updateStateOnServer(dev, "ZP_TRACK", title)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_TRACK", "")
                try:
                    creator = val.creator
                    self.updateStateOnServer(dev, "ZP_CREATOR", creator)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_CREATOR", "")
                try:
                    album = val.album
                    self.updateStateOnServer(dev, "ZP_ALBUM", album)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_ALBUM", "")
                try:
                    artist = val.artist
                    self.updateStateOnServer(dev, "ZP_ARTIST", artist)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_ARTIST", "")
                try:
                    self.processArt(dev, val.album_art_uri)
                    if dev.states['GROUP_Coordinator'] == "true":
                        ZonePlayerUUIDsInGroup = dev.states['ZonePlayerUUIDsInGroup'].split(',')
                        for rdev in indigo.devices.iter("self.ZonePlayer"):
                            SlaveUID = rdev.states['ZP_LocalUID']
                            if SlaveUID != dev.states['ZP_LocalUID'] and SlaveUID in ZonePlayerUUIDsInGroup:
                                self.processArt(rdev, val.album_art_uri)
                except Exception as exception_error:
                    self.processArt(dev, None)
                    # self.updateStateOnServer (dev, "ZP_ART", "")

                try:
                    if uri_siriusxm in dev.states["ZP_CurrentURI"]:
                        mediaInfo = val.stream_content.split("|")
                        for item in mediaInfo:
                            if "TITLE" in item:
                                self.updateStateOnServer(dev, "ZP_TRACK", item[6:])
                            elif "ARTIST" in item:
                                self.updateStateOnServer(dev, "ZP_ARTIST", item[7:])
                        self.updateStateOnServer(dev, "ZP_INFO", "")
                    else:
                        self.updateStateOnServer(dev, "ZP_INFO", val.stream_content)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_INFO", "")

                # TODO: need to figure out when this is really necessary - can't populate for music library
                try:
                    if soco_event.variables["enqueued_transport_uri_meta_data"] == "":
                        enqueued_transport_uri_meta_data = None
                    else:
                        enqueued_transport_uri_meta_data = soco_event.variables["enqueued_transport_uri_meta_data"]
                    title = enqueued_transport_uri_meta_data.title
                    self.updateStateOnServer(dev, "ZP_STATION", title)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_STATION", "")

            except Exception as exception_error:
                pass

            try:
                val = soco_event.variables["next_track_meta_data"]
                if val == "":
                    val = None
                try:
                    self.updateStateOnServer(dev, "ZP_NTRACK", val.title)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_NTRACK", "")
                try:
                    self.updateStateOnServer(dev, "ZP_NCREATOR", val.creator)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_NCREATOR", "")
                try:
                    self.updateStateOnServer(dev, "ZP_NALBUM", val.album)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_NALBUM", "")
                try:
                    self.updateStateOnServer(dev, "ZP_NARTIST", val.artist)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_NARTIST", "")
                try:
                    self.updateStateOnServer(dev, "ZP_NART", val.album_art_uri)
                except Exception as exception_error:
                    self.updateStateOnServer(dev, "ZP_NART", "")
            except Exception as exception_error:
                pass

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_rendering_control(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo RenderingControl] {soco_event.variables}")

            try:
                self.updateStateOnServer(dev, "ZP_VOLUME", soco_event.variables["volume"]["Master"])
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_MUTE", soco_event.variables["mute"]["Master"])
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_VOLUME_FIXED", soco_event.variables["output_fixed"])
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_BASS", soco_event.variables["bass"])
            except Exception as exception_error:
                pass
            try:
                self.updateStateOnServer(dev, "ZP_TREBLE", soco_event.variables["treble"])
            except Exception as exception_error:
                pass
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_queue(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo Queue] {soco_event.variables}")

            val = soco_event.variables["update_id"]
            if actionBusy == 0:
                PlaylistName = "Indigo_" + str(dev.states['ZP_LocalUID'])
                self.actionDirect(PA(dev.id, {"setting": PlaylistName}), "Q_Save")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_group_rendering_control(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo GroupRenderingControl] {soco_event.variables}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_content_directory(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo ContentDirectory] {soco_event.variables}")

            if dev.pluginProps['address'] == self.rootZPIP:
                try:
                    val = soco_event.variables["container_update_i_ds"]
                    if "SQ:" in val:
                        self.getPlaylistsDirect()
                    if "R:0" in val:
                        self.getRT_FavStationsDirect()
                    if "FV:2" in val:
                        self.getSonosFavorites()
                except Exception as exception_error:
                    pass
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_group_management(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo GroupManagement] {soco_event.variables}")

            try:
                self.updateStateOnServer(dev, "GROUP_Coordinator", str(bool(int(soco_event.variables["group_coordinator_is_local"]))).lower())
            except Exception as exception_error:
                pass
            try:
                # self.updateStateOnServer(dev, "GROUP_Name", soco_event.variables["local_group_uuid"].decode('utf-8'))  # TODO: Remove once confirmed as decode not needed
                self.updateStateOnServer(dev, "GROUP_Name", soco_event.variables["local_group_uuid"])
            except Exception as exception_error:
                pass
            if not dev.states["GROUP_Coordinator"]:
                self.copyStateFromMaster(dev)
            else:
                self.updateStateOnSlaves(dev)
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_zone_group_topology(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo ZoneGroupTopology] {soco_event.variables}")

            try:
                # self.updateStateOnServer(dev, "ZoneGroupID", soco_event.variables["zone_group_id"].decode('utf-8'))  # TODO: Remove once confirmed as decode not needed
                self.updateStateOnServer(dev, "ZoneGroupID", soco_event.variables["zone_group_id"])
            except Exception as exception_error:
                pass
            try:
                # self.updateStateOnServer(dev, "ZoneGroupName", soco_event.variables["zone_group_name"].decode('utf-8'))  # TODO: Remove once confirmed as decode not needed
                self.updateStateOnServer(dev, "ZoneGroupName", soco_event.variables["zone_group_name"])
            except Exception as exception_error:
                pass
            try:
                # self.updateStateOnServer(dev, "ZonePlayerUUIDsInGroup", soco_event.variables["zone_player_uui_ds_in_group"].decode('utf-8'))  # TODO: Remove once confirmed as decode not needed
                self.updateStateOnServer(dev, "ZonePlayerUUIDsInGroup", soco_event.variables["zone_player_uui_ds_in_group"])
            except Exception as exception_error:
                pass
            if dev.states['ZoneGroupName'] in ["", "None"]:
                self.copyStateFromMaster(dev)
            else:
                self.updateStateOnSlaves(dev)
            """
            try:
                # ZGS = XML(soco_event.variables["zone_group_state"].decode('utf-8'))  # TODO: Remove once confirmed as decode not needed
                ZGS = XML(soco_event.variables["zone_group_state"])
                for elem in ZGS:
                    for ZoneGroupMember in elem.findall("./ZoneGroupMember"):
                        ZGM_UUID = ZoneGroupMember.get('UUID')
                        ZGM_BootSeq = ZoneGroupMember.get('BootSeq')
                        for deviceId in self.deviceList:
                            dev = indigo.devices[int(deviceId)]
                            if dev.states["ZP_LocalUID"] == ZGM_UUID:
                                if int(ZGM_BootSeq) > int(dev.states["bootseq"]):
                                    self.socoResubscribe(dev, ZGM_BootSeq)
                                break
            except Exception as exception_error:
                pass
            """
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def soco_event_audio_in(self, dev, soco_event):
        try:
            if self.plugin.eventsDebug:
                self.logger.debug(f"[{time.asctime()}] [{dev.name}] [SoCo AudioIn] {soco_event.variables}")

            val = soco_event.variables["audio_input_name"]
            self.updateStateOnServer(dev, "ZP_AIName", val)
            self.getLineIn(dev, val)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def processArt(self, dev, val):
        try:
            self.logger.debug(f"Processing Cover Art: {dev.name}:{val}")
            ZP_ZoneName = dev.states["ZP_ZoneName"]
            res = dev.states["ZP_CurrentURI"]
            if val is not None:
                # Retrieve parent URI for slave zone
                if uri_group in res:
                    (ParentUID, x) = dev.states["ZoneGroupID"].split(':')
                    for pdev in indigo.devices.iter("self.ZonePlayer"):
                        if ParentUID == pdev.states["ZP_LocalUID"]:
                            res = pdev.states["ZP_CurrentURI"]
                prev_art = dev.states["ZP_ART"]
                if uri_radio in res:
                    loc = str(res).find(uri_radio)
                    if loc >= 0:
                        loc_beg = loc + len(uri_radio)
                        loc_end = str(res).find("?sid", loc_beg)
                        loc_end = str(res).find("?sid", loc_beg)
                        val = "http://d1i6vahw24eb07.cloudfront.net/"+self.restoreString(str(res)[loc_beg:loc_end], 0)+"q.png"
                        self.updateStateOnServer(dev, "ZP_ART", val)
                        if val != prev_art:
                            reqObj = urllib.request.Request(val)
                            fileObj = urlopen(reqObj)
                            localFile = open("/Library/Application Support/Perceptive Automation/images/Sonos/"+ZP_ZoneName+"_art.jpg", "wb")
                            localFile.write(fileObj.read())
                            localFile.close()
                elif uri_pandora in res or uri_file in res or uri_music or uri_playlist in res:
                    if str(val).find("/getaa?") >= 0:
                        if val[0:4] != "http":  # TODO: Check this - Fix to avoid double http being created in val?
                            val = "http://"+self.rootZPIP+":1400"+val
                        if val[0:4] != "http":
                            self.logger.warning(f"Artwork problem: val field does not start with 'http' = {val}")
                    self.updateStateOnServer(dev, "ZP_ART", val)
                    if val != prev_art:
                        reqObj = urllib.request.Request(val)
                        fileObj = urlopen(reqObj)
                        localFile = open("/Library/Application Support/Perceptive Automation/images/Sonos/"+ZP_ZoneName+"_art.jpg", "wb")
                        localFile.write(fileObj.read())
                        localFile.close()
                elif uri_siriusxm in res:
                    self.updateStateOnServer(dev, "ZP_ART", val)
                    if val != prev_art:
                        try:
                            reqObj = urllib.request.Request(val)
                            fileObj = urlopen(reqObj)
                            localFile = open("/Library/Application Support/Perceptive Automation/images/Sonos/"+ZP_ZoneName+"_art.jpg", "wb")
                            localFile.write(fileObj.read())
                            localFile.close()
                        except Exception as exception_error:
                            shutil.copy2("sonos_art.jpg", "/Library/Application Support/Perceptive Automation/images/Sonos/"+ZP_ZoneName+"_art.jpg")

            else:
                self.updateStateOnServer(dev, "ZP_ART", "")
                if uri_tv in res:
                    try: 
                        shutil.copy2("sonos_tv.jpg", "/Library/Application Support/Perceptive Automation/images/Sonos/"+ZP_ZoneName+"_art.jpg")
                    except Exception as exception_error:
                        pass
                else:
                    try: 
                        shutil.copy2("sonos_art.jpg", "/Library/Application Support/Perceptive Automation/images/Sonos/"+ZP_ZoneName+"_art.jpg")
                    except Exception as exception_error: 
                        pass

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parsePoint(self, res, startString, stopString):
        try:
            loc = str(res).find(startString)
            if loc > 0:
                loc_beg = loc + len(startString)
                loc_end = str(res).find(stopString, loc_beg)
                return self.restoreString(str(res)[loc_beg:loc_end], 0)
            else:
                return ""

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseDirty(self, res, startString, stopString):
        try:
            loc = str(res).find(startString)
            if loc > 0:
                loc_beg = loc + len(startString)
                loc_end = str(res).find(stopString, loc_beg)
                return str(res)[loc_beg:loc_end]
            else:
                return ""

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseFirstTrackNumberEnqueued(self, deviceId, res):
        try:
            loc = str(res).find("<FirstTrackNumberEnqueued>")
            if loc > 0:
                loc_beg = loc + len("<FirstTrackNumberEnqueued>")
                loc_end = str(res).find("</FirstTrackNumberEnqueued>", loc_beg)
                item = self.restoreString(str(res)[loc_beg:loc_end], 0)
                return item

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseRelTime(self, deviceId, res):
        try:
            return self.parsePoint(res, "<RelTime>", "</RelTime>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseCurrentZoneGroupName(self, res):
        try:
            return self.parsePoint(res, "<CurrentZoneGroupName>", "</CurrentZoneGroupName>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseCurrentZoneGroupID(self, res):
        try:
            return self.parsePoint(res, "<CurrentZoneGroupID>", "</CurrentZoneGroupID>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseCurrentZonePlayerUUIDsInGroup(self, res):
        try:
            return self.parsePoint(res, "<CurrentZonePlayerUUIDsInGroup>", "</CurrentZonePlayerUUIDsInGroup>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseCurrentVolume(self, res):
        try:
            return self.parsePoint(res, "<CurrentVolume>", "</CurrentVolume>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseCurrentMute(self, res):
        try:
            return self.parsePoint(res, "<CurrentMute>", "</CurrentMute>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseCurrentTransportActions(self, res):
        try:
            return self.parsePoint(res, "<Actions>", "</Actions>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseErrorCode(self, res):
        try:
            return self.parsePoint(res, "<errorCode>", "</errorCode>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseBrowseNumberReturned(self, res):
        try:
            return self.parsePoint(res, "<NumberReturned>", "</NumberReturned>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parseAssignedObjectID(self, res):
        try:
            return self.parsePoint(res, "<AssignedObjectID>", "</AssignedObjectID>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def parsePandoraToken(self, res):
        try:
            return self.parsePoint(res, "&m=", "&f")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def playRadio(self, zoneIP, l2p):
        try:
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+l2p+"</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"-1\" parentID=\"-1\" restricted=\"true\"&gt;&lt;dc:title&gt;RADIO&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON65031_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def playPandora(self, zoneIP, l2p, pstation):
        try:
            for pandora_station in Sonos_Pandora:
                if pandora_station[0] == l2p:
                    pemail = pandora_station[2]
                    break
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>pndrradio:"+l2p+"</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"OOOX" + l2p + "\" parentID=\"0\" restricted=\"true\"&gt;&lt;dc:title&gt;" + pstation + "&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON3_" + pemail + "&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def boolConv(self, val):
        try:
            # if val == "on":
            #     return True
            # else:
            #     return False
            return True if val == "on" else False

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def QMode(self, repeat, repeat_one, shuffle):
        try:
            PlayMode = "NORMAL"  # Default
            if not repeat and not repeat_one and not shuffle:
                PlayMode = "NORMAL"
            elif repeat and not shuffle:
                PlayMode = "REPEAT_ALL"
            elif repeat_one and not shuffle:
                PlayMode = "REPEAT_ONE"
            elif not repeat and not repeat_one and shuffle:
                PlayMode = "SHUFFLE_NOREPEAT"
            elif repeat and shuffle:
                PlayMode = "SHUFFLE"
            elif repeat_one and shuffle:
                PlayMode = "SHUFFLE_REPEAT_ONE"
            return PlayMode

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # Actions

    def actionDirect(self, pluginAction, action):
        try:
            global Sonos_Playlists
            global Sonos_Pandora
            global Sonos_RT_FavStations

            if action == "setStandalones":
                zones = []
                x = 1
                while x <= 12:
                    ivar = 'zp' + str(x)
                    if pluginAction.props.get(ivar) not in ["", None, "00000"]:
                        zones.append(pluginAction.props.get(ivar))
                    x = x + 1

                for item in zones:
                    self.logger.info(f"remove zone from group: {item}")
                    dev = indigo.devices[int(item)]
                    if dev.states['GROUP_Coordinator'] == "true":
                        self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")
                    self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev.states['ZP_LocalUID'])+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")

                return

            if pluginAction.deviceId not in indigo.devices:
                self.logger.warning(f"No Sonos device specified for action '{action}' - action ignored!")
                return

            dev = indigo.devices[pluginAction.deviceId]
            zoneIP = dev.pluginProps["address"]

            # Set default values
            CoordinatorIP = None
            CoordinatorDev = None
            idev = None

            if dev.states["GROUP_Coordinator"] == "false":
                Coordinator = dev.states["GROUP_Name"]
                for idev in indigo.devices.iter("self.ZonePlayer"):
                    if idev.states["GROUP_Coordinator"] == "true" and idev.states["GROUP_Name"] == Coordinator:
                        CoordinatorIP = idev.pluginProps["address"]
                        CoordinatorDev = idev
                        break

            match action:
                case "Play":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Play")
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Play")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Play' not actioned as Zone IP cannot be resolved!")

                case "TogglePlay":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Toggle Play")
                    if zoneIP is not None:
                        if dev.states["ZP_STATE"] == "PLAYING":
                            self.actionDirect(pluginAction, "Pause")
                            self.logger.info(f"ZonePlayer: {dev.name}, Pause")
                        else:
                            self.actionDirect(pluginAction, "Play")
                            self.logger.info(f"ZonePlayer: {dev.name}, Play")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Toggle Play' not actioned as Zone IP cannot be resolved!")

                case "Pause":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Pause")
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                        self.logger.info(f"ZonePlayer: {dev.name}, Pause")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Pause' not actioned as Zone IP cannot be resolved!")

                case "Stop":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Stop")
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                        self.logger.info(f"ZonePlayer: {dev.name}, Stop")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Stop' not actioned as Zone IP cannot be resolved!")

                case "Previous":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Previous")
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Previous", "")
                        self.logger.info(f"ZonePlayer: {dev.name}, Previous Track")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Previous Track' not actioned as Zone IP cannot be resolved!")

                case "Next":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Next")
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Next", "")
                        self.logger.info(f"ZonePlayer: {dev.name}, Next Track")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Next Track' not actioned as Zone IP cannot be resolved!")

                case "MuteToggle":
                    self.logger.debug("Sonos Action: Mute Toggle")
                    if int(dev.states["ZP_MUTE"]) == 0:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Mute On")
                    else:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Mute Off")

                case "MuteOn":
                    self.logger.debug("Sonos Action: Mute On")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Mute On")

                case "MuteOff":
                    self.logger.debug("Sonos Action: Mute Off")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Mute Off")

                case "GroupMuteToggle":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Group Mute Toggle")
                    if zoneIP is not None:
                        if int(self.parseCurrentMute(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", ""))) == 0:
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>1</DesiredMute>")
                            self.logger.info(f"ZonePlayer Group: {dev.name}, Mute On")
                        else:
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>0</DesiredMute>")
                            self.logger.info(f"ZonePlayer Group: {dev.name}, Mute Off")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Group Mute Toggle' not actioned as Zone IP cannot be resolved!")

                case "GroupMuteOn":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Group Mute On")
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>1</DesiredMute>")
                        self.logger.info(f"ZonePlayer Group: {dev.name}, Mute On")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Group Mute On' not actioned as Zone IP cannot be resolved!")

                case "GroupMuteOff":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    self.logger.debug("Sonos Action: Group Mute Off")
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>0</DesiredMute>")
                        self.logger.info(f"ZonePlayer Group: {dev.name}, Mute Off")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Group Mute Off' not actioned as Zone IP cannot be resolved!")

                case "Volume":
                    self.logger.debug("Sonos Action: Volume")
                    current_volume = dev.states["ZP_VOLUME"]
                    new_volume = int(eval(self.plugin.substitute(pluginAction.props.get("setting"))))
                    if new_volume < 0 or new_volume > 100:
                        new_volume = current_volume
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume", "<Channel>Master</Channel><DesiredVolume>"+str(new_volume)+"</DesiredVolume>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Volume: {current_volume}, New Volume: {new_volume}")
                case "VolumeDown":
                    self.logger.debug("Sonos Action: Volume Down")
                    current_volume = dev.states["ZP_VOLUME"]
                    new_volume = int(current_volume) - 2
                    if new_volume < 0:
                        new_volume = 0
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume", "<Channel>Master</Channel><DesiredVolume>"+str(new_volume)+"</DesiredVolume>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Volume: {current_volume}, New Volume: {new_volume}")
                case "VolumeUp":
                    self.logger.debug("Sonos Action: Volume Up")
                    current_volume = dev.states["ZP_VOLUME"]
                    new_volume = int(current_volume) + 2
                    if new_volume > 100:
                        new_volume = 100
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume", "<Channel>Master</Channel><DesiredVolume>"+str(new_volume)+"</DesiredVolume>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Volume: {current_volume}, New Volume: {new_volume}")

                case "GroupVolume":
                    self.logger.debug("Sonos Action: Group Volume")
                    current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                    new_volume = int(eval(self.plugin.substitute(pluginAction.props.get("setting"))))
                    if new_volume < 0 or new_volume > 100:
                        new_volume = current_volume
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume", "<DesiredVolume>"+str(new_volume)+"</DesiredVolume>")
                    self.logger.info(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                case "RelativeGroupVolume":
                    self.logger.debug("Sonos Action: Relative Group Volume")
                    current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                    adjustment = pluginAction.props.get("setting")
                    new_volume = int(current_volume) + int(adjustment)
                    if new_volume < 0:
                        new_volume = 0
                    if new_volume > 100:
                        new_volume = 100
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>"+adjustment+"</Adjustment>")
                    self.logger.info(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                case "GroupVolumeDown":
                    self.logger.debug("Sonos Action: Group Volume Down")
                    current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                    new_volume = int(current_volume) - 2
                    if new_volume < 0:
                        new_volume = 0
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>-2</Adjustment>")
                    self.logger.info(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                case "GroupVolumeUp":
                    self.logger.debug("Sonos Action: Group Volume Up")
                    current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                    new_volume = int(current_volume) + 2
                    if new_volume > 100:
                        new_volume = 100
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>2</Adjustment>")
                    self.logger.info(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")

                case "Bass":
                    self.logger.debug("Sonos Action: Bass")
                    current_bass = dev.states["ZP_BASS"]
                    new_bass = pluginAction.props.get("setting")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass", "<DesiredBass>"+str(new_bass)+"</DesiredBass>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Bass: {current_bass}, New Bass: {new_bass}")
                case "BassDown":
                    self.logger.debug("Sonos Action: Bass Down")
                    current_bass = dev.states["ZP_BASS"]
                    new_bass = int(current_bass) - 1
                    if new_bass < -10:
                        new_bass = -10
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass", "<DesiredBass>"+str(new_bass)+"</DesiredBass>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Bass: {current_bass}, New Bass: {new_bass}")
                case "BassUp":
                    self.logger.debug("Sonos Action: Bass Up")
                    current_bass = dev.states["ZP_BASS"]
                    new_bass = int(current_bass) + 1
                    if new_bass > 10:
                        new_bass = 10
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass", "<DesiredBass>"+str(new_bass)+"</DesiredBass>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Bass: {current_bass}, New Bass: {new_bass}")

                case "Treble":
                    self.logger.debug("Sonos Action: Treble")
                    current_treble = dev.states["ZP_BASS"]
                    new_treble = pluginAction.props.get("setting")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble", "<DesiredTreble>"+str(new_treble)+"</DesiredTreble>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Treble: {current_treble}, New Treble: {new_treble}")
                case "TrebleDown":
                    self.logger.debug("Sonos Action: Treble Down")
                    current_treble = dev.states["ZP_BASS"]
                    new_treble = int(current_treble) - 1
                    if new_treble < -10:
                        new_treble = -10
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble", "<DesiredTreble>"+str(new_treble)+"</DesiredTreble>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Treble: {current_treble}, New Treble: {new_treble}")
                case "TrebleUp":
                    self.logger.debug("Sonos Action: Treble Up")
                    current_treble = dev.states["ZP_BASS"]
                    new_treble = int(current_treble) + 1
                    if new_treble > 10:
                        new_treble = 10
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble", "<DesiredTreble>"+str(new_treble)+"</DesiredTreble>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Current Treble: {current_treble}, New Treble: {new_treble}")

                case "NightMode":
                    self.logger.debug("Sonos Action: Night Mode")
                    mode = pluginAction.props.get("setting")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", "<EQType>NightMode</EQType><DesiredValue>" + str(int(mode)) +
                                  "</DesiredValue>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Night Mode: {bool(mode)}")

                case "Q_Crossfade":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        mode = pluginAction.props.get("setting")
                        if mode == 0:
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>0</CrossfadeMode>")
                        elif mode == 1:
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>1</CrossfadeMode>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Queue Crossfade' not actioned as Zone IP cannot be resolved!")

                case "Q_Repeat":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        repeat = bool(int(pluginAction.props.get("setting")))
                        repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                        shuffle = self.boolConv(dev.states["Q_Shuffle"])
                        if repeat:
                            PlayMode = self.QMode(repeat, False, shuffle)
                        else:
                            PlayMode = self.QMode(repeat, repeat_one, shuffle)
                        self.logger.debug(f"Sonos Action: PlayMode {PlayMode}")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Queue Repeat' not actioned as Zone IP cannot be resolved!")

                case "Q_RepeatOne":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        repeat_one = bool(int(pluginAction.props.get("setting")))
                        repeat = self.boolConv(dev.states["Q_Repeat"])
                        shuffle = self.boolConv(dev.states["Q_Shuffle"])
                        if repeat_one:
                            PlayMode = self.QMode(False, repeat_one, shuffle)
                        else:
                            PlayMode = self.QMode(repeat, repeat_one, shuffle)
                        self.logger.debug(f"Sonos Action: PlayMode {PlayMode}")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Queue Repeat One' not actioned as Zone IP cannot be resolved!")

                case "Q_RepeatToggle":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        repeat = self.boolConv(dev.states["Q_Repeat"])
                        repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                        shuffle = self.boolConv(dev.states["Q_Shuffle"])
                        if not repeat and not repeat_one:
                            PlayMode = self.QMode(True, False, shuffle)
                        elif repeat and not repeat_one:
                            PlayMode = self.QMode(False, True, shuffle)
                        else:
                            PlayMode = self.QMode(False, False, shuffle)
                        self.logger.debug(f"Sonos Action: PlayMode {PlayMode}")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Queue Repeat Toggle' not actioned as Zone IP cannot be resolved!")

                case "Q_Shuffle":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        shuffle = bool(int(pluginAction.props.get("setting")))
                        repeat = self.boolConv(dev.states["Q_Repeat"])
                        repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                        PlayMode = self.QMode(repeat, repeat_one, shuffle)
                        self.logger.debug(f"Sonos Action: PlayMode {PlayMode}")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Queue Shuffle' not actioned as Zone IP cannot be resolved!")

                case "Q_ShuffleToggle":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        repeat = self.boolConv(dev.states["Q_Repeat"])
                        repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                        shuffle = self.boolConv(dev.states["Q_Shuffle"])
                        if shuffle:
                            PlayMode = self.QMode(repeat, repeat_one, False)
                        else:
                            PlayMode = self.QMode(repeat, repeat_one, True)
                        self.logger.debug(f"Sonos Action: PlayMode {PlayMode}")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Queue Shuffle Toggle' not actioned as Zone IP cannot be resolved!")

                case "Q_Clear":
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/Queue", "RemoveAllTracks", "<QueueID>0</QueueID><UpdateID>0</UpdateID>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Clear Queue")

                case "Q_Save":
                    self.updateZoneTopology(dev)
                    if dev.states["GROUP_Coordinator"] == "false":
                        self.logger.debug(f"ZonePlayer: {dev.name}, Cannot Save Queue for Slave")
                    else:
                        self.plugin.sleep(0.5)
                        PlaylistName = pluginAction.props.get("setting")

                        ZP  = self.parseBrowseNumberReturned(self.SOAPSend(zoneIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>Q:0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"))

                        try:
                            int(ZP)
                        except ValueError:
                            self.logger.error(f"Q_Save - ZP type is '{type(ZP)}', value is '{ZP}'")
                            return

                        if PlaylistName == "Indigo_" + dev.states['ZP_LocalUID']:
                            self.updateStateOnServer(dev, "Q_Number", ZP)
                        if int(ZP) > 0:
                            ObjectID = ""
                            for plist in Sonos_Playlists:
                                if plist[1] == PlaylistName:
                                    ObjectID = plist[2]
                            AssignedObjectID = self.parseAssignedObjectID(self.SOAPSend(zoneIP, "/MediaRenderer", "/Queue", "SaveAsSonosPlaylist", "<QueueID>0</QueueID><Title>" + PlaylistName + "</Title><ObjectID>" + ObjectID + "</ObjectID>"))
                            if ObjectID == "":
                                ObjectID = AssignedObjectID
                            if PlaylistName.find(dev.states['ZP_LocalUID']) > -1:
                                self.updateStateOnServer(dev, "Q_ObjectID", ObjectID)

                            self.logger.debug(f"ZonePlayer: {dev.name}, Save Queue: {PlaylistName}")
                        else:
                            if PlaylistName == "Indigo_" + dev.states['ZP_LocalUID']:
                                ObjectID = ""
                                for plist in Sonos_Playlists:
                                    if plist[1] == PlaylistName:
                                        ObjectID = plist[2]
                                        self.actionDirect(PA(dev.id, {"setting": ObjectID}), "CD_RemovePlaylist")
                                self.updateStateOnServer(dev, "Q_ObjectID", "")
                            self.logger.debug(f"ZonePlayer: {dev.name}, Nothing in Queue to Save")

                case "CD_RemovePlaylist":
                    ObjectID = pluginAction.props.get("setting")
                    for plist in Sonos_Playlists:
                        if plist[2] == ObjectID:
                            PlaylistName = plist[1]
                            self.SOAPSend(zoneIP, "/MediaServer", "/ContentDirectory", "DestroyObject", "<ObjectID>" + ObjectID + "</ObjectID>")
                            self.logger.info(f"ZonePlayer: {dev.name}, Remove Playlist: {PlaylistName}")

                case "ChannelUp":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                        currentURI = idev.states["ZP_CurrentURI"]
                    else:
                        currentURI = dev.states["ZP_CurrentURI"]
                    if zoneIP is not None:
                        x = 0
                        foundit = "false"
                        if uri_radio in currentURI:
                            for l2p in Sonos_RT_FavStations:
                                if currentURI == l2p[0]:
                                    foundit = "true"
                                    break
                                else:
                                    x = x + 1
                            if foundit == "false":
                                x = 0
                            elif foundit == "true":
                                if x == 0:
                                    x = len(Sonos_RT_FavStations) - 1
                                else:
                                    x = x - 1
                            l2p = Sonos_RT_FavStations[x][0].replace("&", "&amp;")
                            self.playRadio(zoneIP, l2p)
                        elif uri_pandora in currentURI:
                            Sonos_Pandora_Sort = sorted(Sonos_Pandora, key=lambda a: a[1])
                            self.logger.info(f"{Sonos_Pandora_Sort}")
                            for l2p in Sonos_Pandora_Sort:
                                if currentURI[10:] == l2p[0]:
                                    foundit = "true"
                                    break
                                else:
                                    x = x + 1
                            if foundit == "false":
                                x = 0
                            elif foundit == "true":
                                if x == 0:
                                    x = len(Sonos_Pandora_Sort) - 1
                                else:
                                    x = x - 1
                            l2p = Sonos_Pandora_Sort[x][0]
                            pstation = self.cleanString(Sonos_Pandora_Sort[x][1])
                            self.playPandora(zoneIP, l2p, pstation)
                        elif uri_siriusxm in currentURI:
                            # setting = currentURI[currentURI.find("%3a")+3:currentURI.find("?")]
                            setting = urllib.parse.unquote(currentURI[currentURI.find(":")+1:currentURI.find("?")])
                            for Channel in range(len(Sonos_SiriusXM)):
                                # if Sonos_SiriusXM[Channel][3] == setting:
                                if Sonos_SiriusXM[Channel][1] == setting:
                                    if Channel + 1 < len(Sonos_SiriusXM):
                                        # new_setting = Sonos_SiriusXM[Channel+1][3]
                                        new_setting = Sonos_SiriusXM[Channel+1][1]
                                    else:
                                        # new_setting = Sonos_SiriusXM[0][3]
                                        new_setting = Sonos_SiriusXM[0][1]
                                    break
                            self.actionDirect(PA(dev.id, {"setting": new_setting}), "ZP_SiriusXM")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Channel Up' not actioned as Zone IP cannot be resolved!")

                case "ChannelDown":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                        currentURI = idev.states["ZP_CurrentURI"]
                    else:
                        currentURI = dev.states["ZP_CurrentURI"]
                    if zoneIP is not None:
                        x = 0
                        foundit = "false"
                        if uri_radio in currentURI:
                            for l2p in Sonos_RT_FavStations:
                                if currentURI == l2p[0]:
                                    foundit = "true"
                                    break
                                else:
                                    x = x + 1
                            if foundit == "false":
                                x = 0
                            elif foundit == "true":
                                if x == (len(Sonos_RT_FavStations) - 1):
                                    x = 0
                                else:
                                    x = x + 1
                            l2p = Sonos_RT_FavStations[x][0].replace("&", "&amp;")
                            self.playRadio(zoneIP, l2p)
                        elif uri_pandora in currentURI:
                            Sonos_Pandora_Sort = sorted(Sonos_Pandora, key=lambda a: a[1])
                            self.logger.info(f"{Sonos_Pandora_Sort}")
                            for l2p in Sonos_Pandora_Sort:
                                if currentURI[10:] == l2p[0]:
                                    foundit = "true"
                                    break
                                else:
                                    x = x + 1
                            if foundit == "false":
                                x = 0
                            elif foundit == "true":
                                if x == (len(Sonos_Pandora_Sort) - 1):
                                    x = 0
                                else:
                                    x = x + 1
                            l2p = Sonos_Pandora_Sort[x][0]
                            pstation = self.cleanString(Sonos_Pandora_Sort[x][1])
                            self.playPandora(zoneIP, l2p, pstation)
                        elif uri_siriusxm in currentURI:
                            # setting = currentURI[currentURI.find("%3a")+3:currentURI.find("?")]
                            setting = urllib.parse.unquote(currentURI[currentURI.find(":")+1:currentURI.find("?")])
                            for Channel in range(len(Sonos_SiriusXM)):
                                # if Sonos_SiriusXM[Channel][3] == setting:
                                if Sonos_SiriusXM[Channel][1] == setting:
                                    if Channel > 0:
                                        # new_setting = Sonos_SiriusXM[Channel-1][3]
                                        new_setting = Sonos_SiriusXM[Channel-1][1]
                                    else:
                                        # new_setting = Sonos_SiriusXM[len(Sonos_SiriusXM)-1][3]
                                        new_setting = Sonos_SiriusXM[len(Sonos_SiriusXM)-1][1]
                                    break
                            self.actionDirect(PA(dev.id, {"setting": new_setting}), "ZP_SiriusXM")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'Channel Down' not actioned as Zone IP cannot be resolved!")

                case "ZP_LineIn":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        dev_src = indigo.devices[int(pluginAction.props.get("setting"))]
                        self.logger.debug(f"Playing LineIn: {dev_src.states['ZP_AIName']}...")
                        dev_src_LocalUID = dev_src.states['ZP_LocalUID']
                        if dev_src.states["ZP_AIName"] != "":
                            self.logger.debug("Sonos Action: Line-In")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-stream:"+str(dev_src_LocalUID)+"</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Line In' not actioned as Zone IP cannot be resolved!")

                case "ZP_RT_FavStation":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        l2p = pluginAction.props.get("setting").replace("&", "&amp;")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+l2p+"</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"-1\" parentID=\"-1\" restricted=\"true\"&gt;&lt;dc:title&gt;RADIO&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON65031_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP RT FavStation' not actioned as Zone IP cannot be resolved!")

                case "ZP_LIST":
                    dev_src_LocalUID = None
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                        if CoordinatorDev is not None:
                            dev_src_LocalUID = CoordinatorDev.states['ZP_LocalUID']
                    else:
                        dev_src_LocalUID = dev.states['ZP_LocalUID']
                    if zoneIP is not None and dev_src_LocalUID is not None:
                        l2p = pluginAction.props.get("setting")
                        mode = pluginAction.props.get("mode")
                        plist_name = ""
                        for plist in Sonos_Playlists:
                            if plist[0] == l2p:
                                plist_name = plist[1]
                        # self.logger.info(f"Queueing Playlist: {mode}: {plist_name}...")
                        if mode == "Play Now":
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData></EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        elif mode == "Play Next":
                            # current_track = self.parseCurrentTrack(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", ""))
                            current_track = dev.states['ZP_CurrentTrack']
                            self.logger.info(current_track)
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData></EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>"+str(int(current_track)+1)+"</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                        elif mode == "Add To Queue":
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData></EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                        elif mode == "Replace Queue":
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "RemoveAllTracksFromQueue", "")
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData></EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Play Sonos Playlist: {plist_name}")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP List' not actioned as Zone IP cannot be resolved!")

                case "ZP_Queue":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                        dev_src_LocalUID = CoordinatorDev.states['ZP_LocalUID']
                    else:
                        dev_src_LocalUID = dev.states['ZP_LocalUID']
                    if zoneIP is not None:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Queue' not actioned as Zone IP cannot be resolved!")

                case "addPlayerToZone":
                    dev_dest = indigo.devices[int(pluginAction.props.get("setting"))]
                    # self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon:"+str(dev_dest.states['ZP_LocalUID'])+"</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    self.SOAPSend(dev_dest.pluginProps["address"], "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon:"+str(dev.states['ZP_LocalUID'])+"</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                case "setStandalone":
                    self.logger.info(f"remove zone from group: {dev.name}")
                    if dev.states['GROUP_Coordinator'] == "true":
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev.states['ZP_LocalUID'])+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                case "addPlayersToZone":
                    zones = []
                    x = 1
                    while x <= 12:
                        ivar = 'zp' + str(x)
                        if pluginAction.props.get(ivar) not in ["", None, "00000"]:
                            zones.append(pluginAction.props.get(ivar))
                        x = x + 1

                    for item in zones:
                        self.logger.info(f"add zone to group: {item}")
                        dev_dest = indigo.devices[int(item)]
                        self.SOAPSend(dev_dest.pluginProps["address"], "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon:"+str(dev.states['ZP_LocalUID'])+"</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")

                case "ZP_sleepTimer":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        l2p = pluginAction.props.get("setting")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "ConfigureSleepTimer", "<NewSleepTimerDuration>" + l2p + "</NewSleepTimerDuration>")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Sleep Timer' not actioned as Zone IP cannot be resolved!")

                case "ZP_Pandora":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        l2p = pluginAction.props.get("setting")
                        for pandora_station in Sonos_Pandora:
                            if pandora_station[0] == l2p:
                                pstation = self.cleanString(pandora_station[1])
                                pemail = pandora_station[2]
                                pnickname = pandora_station[3]
                                break
                        # self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>pndrradio:"+l2p+"</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"OOOX" + l2p + "\" parentID=\"0\" restricted=\"true\"&gt;&lt;dc:title&gt;" + pstation +  "&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON3_" + pemail + "&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-sonosapi-radio:ST%3a"+l2p+"?sid=236&amp;flags=8300&amp;sn=10</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"OOOX" + l2p + "\" parentID=\"0\" restricted=\"true\"&gt;&lt;dc:title&gt;" + pstation + "&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON3_" + pemail + "&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Play Pandora: {pnickname}: {pstation}")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Pandora' not actioned as Zone IP cannot be resolved!")

                case "ZP_SiriusXM":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        contentId = pluginAction.props.get("setting")

                        for Channel in Sonos_SiriusXM:
                            # if Channel[3] == contentId:
                            if Channel[1] == contentId:
                                # siriusChannelNo = Channel[0]
                                # name = self.cleanString(Channel[4]).encode('ascii', 'xmlcharrefreplace')
                                title = Channel[2]
                                break
                        # self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-sonosapi-hls:r%3a" + contentId + "?sid=37&amp;flags=8480&amp;sn=8</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"" + contentId + "\" parentID=\"0\" restricted=\"true\"&gt;&lt;dc:title&gt;" + str(siriusChannelNo) + " - " + name +  "&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON6_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-sonosapi-hls:" + urllib.parse.quote(contentId) + "?sid=37&amp;flags=8480&amp;sn=8</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"" + contentId + "\" parentID=\"0\" restricted=\"true\"&gt;&lt;dc:title&gt;" + title + "&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON6_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Play SiriusXM: {title}")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP SiriusXM' not actioned as Zone IP cannot be resolved!")

                case "ZP_Spotify":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                        dev_src_LocalUID = CoordinatorDev.states['ZP_LocalUID']
                    else:
                        dev_src_LocalUID = dev.states['ZP_LocalUID']
                    if zoneIP is not None:
                        l2p = pluginAction.props.get("setting")
                        mode = pluginAction.props.get("mode")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Spotify' not actioned as Zone IP cannot be resolved!")

                case "ZP_Container":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                        dev_src_LocalUID = CoordinatorDev.states['ZP_LocalUID']
                    else:
                        dev_src_LocalUID = dev.states['ZP_LocalUID']
                    if zoneIP is not None:
                        l2p = pluginAction.props.get("setting")
                        mode = pluginAction.props.get("mode")
                        # (uri_header, uri_detail) = l2p.split(':')
                        for title in Sonos_Favorites:
                            if title[0] == l2p:
                                pTitle = self.cleanString(title[1]).encode('ascii', 'xmlcharrefreplace')
                                MD = title[2]
                                break

                        # SONOS api change for Favorites?
                        l2p = l2p.replace("&", "&amp;")

                        if mode == "Play Now":
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        elif mode == "Play Next":
                            # current_track = self.parseCurrentTrack(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", ""))
                            current_track = dev.states['ZP_CurrentTrack']
                            self.logger.info(current_track)
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>"+str(int(current_track)+1)+"</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                        elif mode == "Add To Queue":
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                        elif mode == "Replace Queue":
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "RemoveAllTracksFromQueue", "")
                            track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Play: {pTitle}")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Container' not actioned as Zone IP cannot be resolved!")

                case"ZP_SonosRadio":
                    if dev.states["GROUP_Coordinator"] == "false":
                        zoneIP = CoordinatorIP
                    if zoneIP is not None:
                        l2p = pluginAction.props.get("setting")
                        for title in Sonos_Favorites:
                            if title[0] == l2p:
                                pTitle = self.cleanString(title[1]).encode('ascii', 'xmlcharrefreplace')
                                URI = title[3]
                                MD = title[2]
                                break
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+URI+"</CurrentURI><CurrentURIMetaData>"+MD+"</CurrentURIMetaData>")
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                        self.logger.info(f"ZonePlayer: {dev.name}, Play Radio: {pTitle}")
                    else:
                        self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Sonos Radio' not actioned as Zone IP cannot be resolved!")

                case "ZP_TV":
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-sonos-htastream:"+str(dev.states['ZP_LocalUID'])+":spdif</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"spdif-input\" parentID=\"0\" restricted=\"false\"&gt;&lt;dc:title&gt;"+str(dev.states['ZP_LocalUID'])+"&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioItem&lt;/upnp:class&gt;&lt;res protocolInfo=\"spdif\"&gt;x-sonos-htastream:"+str(dev.states['ZP_LocalUID'])+":spdif&lt;/res&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")

                case "ZP_SonosFavorites":
                    setting = pluginAction.props.get("setting")
                    for uri in Sonos_Favorites:
                        if uri[4] == setting:
                            l2p = uri[0]
                            break
                    mode = pluginAction.props.get("mode")
                    if mode == "":
                        mode = "Play Now"

                    if uri_radio in l2p:
                        self.actionDirect(PA(dev.id, {"setting": l2p}), "ZP_RT_FavStation")
                    elif uri_pandora in l2p:
                        setting = l2p[l2p.find(":")+1:l2p.find("?")]
                        self.actionDirect(PA(dev.id, {"setting": setting}), "ZP_Pandora")
                    elif uri_siriusxm in l2p:
                        # setting = l2p[l2p.find("%3a")+3:l2p.find("?")]
                        setting = urllib.parse.unquote(l2p[l2p.find(":")+1:l2p.find("?")])
                        self.actionDirect(PA(dev.id, {"setting": setting}), "ZP_SiriusXM")
                    elif uri_spotify in l2p:
                        self.actionDirect(PA(dev.id, {"setting": l2p, "mode": mode}), "ZP_Container")
                    elif uri_container in l2p or uri_jffs in l2p or uri_playlist in l2p or uri_file in l2p:
                        self.actionDirect(PA(dev.id, {"setting": l2p, "mode": mode}), "ZP_Container")
                    elif uri_sonos_radio in l2p:
                        self.actionDirect(PA(dev.id, {"setting": l2p}), "ZP_SonosRadio")
                    else:
                        self.logger.info(f"I do not know what to do with Favorite: {l2p}")

                case "ZP_DumpURI":
                    MediaInfo = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetMediaInfo", "")
                    PositionInfo = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", "")
                    self.logSep(0)
                    self.logger.info(f"ZonePlayer: {zoneIP}, {dev.name}")
                    self.logger.info(f"MediaInfo: {MediaInfo}")
                    self.logger.info(f"PositionInfo: {PositionInfo}")
                    self.logSep(0)

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def actionPandoraThumbs(self, pluginAction, action):
        try:
            dev = indigo.devices[pluginAction.deviceId]
            zoneIP = dev.pluginProps["address"]

            if dev.states["GROUP_Coordinator"] == "false":
                Coordinator = dev.states["GROUP_Name"]
                for idev in indigo.devices.iter("self.ZonePlayer"):
                    if idev.states["GROUP_Coordinator"] == "true" and idev.states["GROUP_Name"] == Coordinator:
                        zoneIP = idev.pluginProps["address"]
                        dev = indigo.devices[idev.id]
                        break

            if uri_pandora in dev.states["ZP_CurrentURI"]:
                (x, y) = dev.states["ZP_CurrentURI"].split(':')
                (stationId, z) = y.split('?')
                for item in Sonos_Pandora:
                    if item[0] == stationId:
                        PandoraStation = item[1]
                        PandoraEmailAddress = item[2]
                        break
                trackToken = self.parsePandoraToken(dev.states["ZP_CurrentTrackURI"])

                if PandoraEmailAddress == self.PandoraEmailAddress:
                    PandoraPassword = self.PandoraPassword
                elif PandoraEmailAddress == self.PandoraEmailAddress2:
                    PandoraPassword = self.PandoraPassword2

                pandora = Pandora()
                pandora.authenticate(PandoraEmailAddress, PandoraPassword)

                if action == "thumbs_up":
                    thumbAction = "Thumbs Up"
                    feedback = True
                elif action == "thumbs_down":
                    thumbAction = "Thumbs Down"
                    feedback = False

                try:
                    thumb_status = pandora.add_feedback(stationId, trackToken, feedback)
                    partist = thumb_status['artistName']
                    ptrack = thumb_status['songName']
                    if action == "thumbs_down":
                        self.actionDirect(PA(dev.id), "Next")

                    self.logger.info(f"[{time.asctime()}] {thumbAction} for station: {PandoraStation}, artist: {partist}, track: {ptrack} on ZonePlayer: {dev.name}")
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Unable to {thumbAction} track on ZonePlzyer: {dev.name}")

            else:
                self.logger.error(f"[{time.asctime()}] Pandora not actively playing on ZonePlayer: {dev.name}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def actionStates(self, pluginAction, action):
        try:
            global SavedState
            if action == "saveStates":
                SavedState = []
                for dev in indigo.devices.iter("self.ZonePlayer"):
                    if dev.enabled and dev.pluginProps["model"] != SONOS_SUB:
                        # ZP  = self.parseBrowseNumberReturned(self.SOAPSend(dev.pluginProps["address"], "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>Q:0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"))
                        ZP = ""
                        ZP_CurrentURIMetaData = self.parseDirty(self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport", "GetMediaInfo", ""), "<CurrentURIMetaData>", "</CurrentURIMetaData>")
                        rel_time = self.parseRelTime(dev, self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport", "GetPositionInfo", ""))
                        SavedState.append((dev.states['ZP_LocalUID'], dev.states['Q_Crossfade'], dev.states['Q_Repeat'], dev.states['Q_Shuffle'], dev.states['ZP_MUTE'], dev.states['ZP_STATE'], dev.states['ZP_VOLUME'], dev.states['ZP_CurrentURI'], ZP_CurrentURIMetaData, dev.states['ZP_CurrentTrack'], dev.states['GROUP_Coordinator'], ZP, rel_time, dev.states['ZonePlayerUUIDsInGroup']))
            elif action == "restoreStates":
                pass

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def actionAnnouncement(self, pluginAction, action):
        try:
            global SavedState
            global actionBusy

            actionBusy = 1

            self.actionStates(pluginAction, "saveStates")

            zp_volume = self.plugin.substitute(pluginAction.props.get("zp_volume"))

            play_chime = pluginAction.props.get("chime", False)
            print(f"Play Chime? [{type(zp_volume)}: {play_chime}")

            # Preserve existing group structure if Group Coordinator Only is selected in action

            try:
                gc_only = pluginAction.props.get("gc_only")
            except Exception as exception_error:
                gc_only = False

            # need this until group announcement actions are merged
            if action == "announcement":
                gc_only = False

            AnnouncementZones = []
            if not gc_only:
                x = 1
                while x <= 12:
                    ivar = 'zp' + str(x)
                    if pluginAction.props.get(ivar) not in ["", None, "00000"]:
                        AnnouncementZones.append(pluginAction.props.get(ivar))
                    x = x + 1
            else:
                dev = indigo.devices[int(pluginAction.props.get("zp1"))]
                if dev.states["GROUP_Coordinator"] == "true":
                    AnnouncementZones.append(dev.id)
                else:
                    # if selected ZonePlayer is not master of a group, find the master
                    Coordinator = dev.states["GROUP_Name"]
                    for idev in indigo.devices.iter("self.ZonePlayer"):
                        if idev.states["GROUP_Coordinator"] == "true" and idev.states["GROUP_Name"] == Coordinator:
                            AnnouncementZones.append(idev.id)
                            break

            if action == "announcement":
                announcement = self.plugin.substitute(pluginAction.props.get("setting"), validateOnly=False)
                zp_input = pluginAction.props.get("zp_input")

                self.logger.info(f"Announcement: {announcement}, Volume: {zp_volume}, Line-In: {zp_input}")

                dev_src = indigo.devices[int(zp_input)]
                dev_src_LocalUID = dev_src.states['ZP_LocalUID']

                if dev_src.states['ZP_AIName'] == "":
                    self.logger.info("No Line-In Available...")
                    actionBusy = 0
                    return

                for item in AnnouncementZones:
                    dev = indigo.devices[int(item)]
                    zoneIP = dev.pluginProps["address"]

                    # if member of group, remove from group
                    # no action necessary since uri will change to line-in
                    if dev.states['GROUP_Coordinator'] == "false":
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")
                    # change input to line-in
                    self.logger.debug(f"Playing LineIn: {dev_src.states['ZP_AIName']}...")
                    self.logger.debug("Sonos Action: Line-In")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-stream:"+str(dev_src_LocalUID)+"</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    # set announcment volume
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume", "<Channel>Master</Channel><DesiredVolume>"+str(zp_volume)+"</DesiredVolume>")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    # un-mute ZonePlayer
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")

                # make announcement
                self.logger.debug("Making Announcement...")
                self.plugin.sleep(0.5)
                indigo.server.speak(" ", waitUntilDone=True)
                indigo.server.speak(announcement, waitUntilDone=True)
                self.plugin.sleep(1.0)

            elif action == "announcementMP3":
                if pluginAction.props.get("ttsORfile") == "TTS":
                    announcement = self.plugin.substitute(pluginAction.props.get("setting"), validateOnly=False)
                    zp_language = pluginAction.props.get("language")
                    tts = gTTS(text=announcement, lang=zp_language)
                    tts.save('announcement.mp3')
                    s_announcement = "announcement.mp3"
                    tts_delay = 0

                elif pluginAction.props.get("ttsORfile") == "IVONA":
                    announcement = self.plugin.substitute(pluginAction.props.get("IVONA_setting"), validateOnly=False)

                    v = pyvona.pyvona.create_voice(self.IVONAaccessKey, self.IVONAsecretKey)
                    v.codec = 'mp3'
                    v.voice_name = IVONAVoices[int(pluginAction.props.get("IVONA_voice"))][1]
                    v.sentence_break = int(pluginAction.props.get("IVONA_sentence_break"))
                    v.speech_rate = pluginAction.props.get("IVONA_speech_rate")
                    v.fetch_voice(announcement, 'announcement')
                    s_announcement = "announcement.mp3"
                    tts_delay = 0.5
                    # small delay to allow MP3 file creation completion
                    self.plugin.sleep(0.5)

                elif pluginAction.props.get("ttsORfile") == "POLLY":
                    announcement = self.plugin.substitute(pluginAction.props.get("POLLY_setting"), validateOnly=False)
                    client = boto3.client('polly', aws_access_key_id=self.PollyaccessKey, aws_secret_access_key=self.PollysecretKey, region_name='us-east-1')
                    response = client.synthesize_speech(OutputFormat='mp3', Text=announcement, VoiceId=pluginAction.props.get("POLLY_voice"))
                    if "AudioStream" in response:
                        with closing(response["AudioStream"]) as stream:
                            data_bytes = stream.read()
                            f = open("announcement.mp3", "wb+")
                            f.write(data_bytes)
                            f.close()
                    s_announcement = "announcement.mp3"
                    tts_delay = 0.5

                elif pluginAction.props.get("ttsORfile") == "APPLE":
                    announcement = self.plugin.substitute(pluginAction.props.get("APPLE_setting"), validateOnly=False)
                    sp = NSSpeechSynthesizer.alloc().initWithVoice_(pluginAction.props.get("APPLE_voice"))
                    ru = NSURL.fileURLWithPath_("./announcement.aiff")
                    sp.startSpeakingString_toURL_(announcement, ru)
                    while sp.isSpeaking():
                        print("Still speaking ...")
                        time.sleep(0.1)

                    lame_binary = f"./lame/{self.lame_platform_folder}/lame"
                    lameCommand = f'"{lame_binary}" -h "announcement.aiff" "announcement.mp3"'

                    ps = subprocess.Popen(lameCommand,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=True)

                    for line in ps.stderr:
                        print(f"stderr: {line}")
                    s_announcement = "announcement.mp3"
                    tts_delay = 0.5
                    # small delay to allow MP3 file creation completion
                    # self.plugin.sleep(1.0)  # TODO: IS this needed now?

                elif pluginAction.props.get("ttsORfile") == "MICROSOFT":
                    announcement = self.plugin.substitute(pluginAction.props.get("MICROSOFT_setting"), validateOnly=False)
                    language = pluginAction.props.get("MICROSOFT_voice")
                    statinfo = self.MicrosoftTranslate(announcement, language)
                    s_announcement = "announcement.mp3"
                    tts_delay = 0.5
                    if not statinfo:
                        self.logger.error("Microsoft Translate Error")
                        return

                else:
                    announcement = "FILE [" + pluginAction.props.get("sound_file") + "]"
                    os.system("cp -pr \"" + self.SoundFilePath + "/" + pluginAction.props.get("sound_file") + "\" announcement.mp3")
                    s_announcement = "announcement.mp3"
                    tts_delay = 0

                self.logger.info(f"Announcement: {announcement}, Volume: {zp_volume}")

                GM = indigo.devices[int(AnnouncementZones[0])]
                zoneIP = GM.pluginProps["address"]

                if gc_only:
                    group_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                    group_mute = self.parseCurrentMute(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", ""))

                if not gc_only:
                    # set standalone
                    self.logger.debug("Announcement: set standalone")
                    for item in AnnouncementZones:
                        dev = indigo.devices[int(item)]
                        self.actionDirect(PA(dev.id), "setStandalone")
                    # add announcement zones to group
                    self.logger.debug("Announcement: add announcement zones to group")
                    itemcount = 0
                    for item in AnnouncementZones:
                        dev = indigo.devices[int(item)]
                        if itemcount > 0:
                            self.actionDirect(PA(GM.id, {'setting': dev.id}), "addPlayerToZone")
                        itemcount = itemcount + 1
                else:
                    self.actionDirect(PA(GM.id), "Stop")

                # set volume
                self.logger.debug("Announcement: set volume")
                if not gc_only:
                    for item in AnnouncementZones:
                        dev = indigo.devices[int(item)]
                        self.actionDirect(PA(dev.id, {'setting': zp_volume}), "Volume")
                else:
                    self.actionDirect(PA(GM.id, {'setting': zp_volume}), "GroupVolume")
                    self.actionDirect(PA(GM.id), "GroupMuteOff")

                count = 0
                success = 0
                while count < 5 and success == 0:
                    try:
                        if "mp3" in s_announcement:
                            audio = MP3("./" + s_announcement)
                        elif "aiff" in s_announcement:
                            audio = AIFF("./" + s_announcement)
                        if play_chime:
                            chime = MP3("./chime.mp3")
                        success = 1
                    except Exception as exception_error:
                        self.plugin.sleep(0.5)
                        count = count + 1

                if success == 1:

                    if play_chime:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>http://" +
                                      self.HTTPServer + ":" + self.HTTPStreamingPort + "/" + "chime.mp3" +
                                      "</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")

                        # turn off queue repeat
                        self.actionDirect(PA(GM.id, {'setting': 0}), "Q_Repeat")

                        self.plugin.sleep(0.5)

                        self.actionDirect(PA(GM.id), "Play")
                        self.plugin.sleep(chime.info.length)
                        self.plugin.sleep(0.2)

                    self.logger.info(f"Announcement Length: {audio.info.length}")

                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>http://" + self.HTTPServer + ":" + self.HTTPStreamingPort + "/" + s_announcement + "</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")

                    # turn off queue repeat
                    self.actionDirect(PA(GM.id, {'setting': 0}), "Q_Repeat")

                    self.plugin.sleep(1)

                    self.actionDirect(PA(GM.id), "Play")
                    self.plugin.sleep(tts_delay + audio.info.length)
                else:
                    self.logger.error("Unable to read MP3 file.  Announcement aborted.")

            # restore state

            updatedURI = {}
            for item in AnnouncementZones:
                dev = indigo.devices[int(item)]
                if not gc_only:
                    self.actionDirect(PA(dev.id), "setStandalone")
                updatedURI[dev.id] = 0
                self.plugin.sleep(.5)

            for item in AnnouncementZones:
                dev = indigo.devices[int(item)]
                zoneIP = dev.pluginProps["address"]

                for state in SavedState:
                    if state[0] == dev.states['ZP_LocalUID']:
                        self.logger.debug(f"Restore States: {state[0]}:{dev.states['ZP_LocalUID']}:{dev.name}")
                        self.logger.debug(f"01:Q_Crossfade:            {state[1]}")
                        self.logger.debug(f"02:Q_Repeat:               {state[2]}")
                        self.logger.debug(f"03:Q_Shuffle:              {state[3]}")
                        self.logger.debug(f"04:ZP_MUTE:                {state[4]}")
                        self.logger.debug(f"05:ZP_STATE:               {state[5]}")
                        self.logger.debug(f"06:ZP_VOLUME:              {state[6]}")
                        self.logger.debug(f"07:ZP_CurrentURI:          {state[7]}")
                        self.logger.debug(f"08:CurrentURI MetaData:    {state[8]}")
                        self.logger.debug(f"09:ZP_CurrentTrack:        {state[9]}")
                        self.logger.debug(f"10:GROUP_Coordinator:      {state[10]}")
                        self.logger.debug(f"12:Relative Time:          {state[12]}")
                        self.logger.debug(f"13:ZonePlayerUUIDsInGroup: {state[13]}")

                        if not gc_only:
                            # restore group membership
                            if state[10] == "true":
                                self.logger.debug(f"{state[0]}: Restore URI: {state[7]}")

                                # Restore Queue from Saved Playlist
                                if int(dev.states['Q_Number']) == 0:
                                    self.actionDirect(PA(dev.id), "Q_Clear")
                                else:
                                    for plist in Sonos_Playlists:
                                        if dev.states['Q_ObjectID'] == plist[2]:
                                            l2p = plist[0]
                                    self.actionDirect(PA(dev.id), "Q_Clear")
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData></EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>")

                                SendVar = "<CurrentURI>" + state[7].replace("&", "&amp;") + "</CurrentURI><CurrentURIMetaData>" + state[8] + "</CurrentURIMetaData>"
                                # self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", SendVar.encode('utf-8'))
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", SendVar)
                                updatedURI[dev.id] = 1

                                ZonePlayerUUIDsInGroup = state[13].split(',')
                                for ZonePlayerUUID in ZonePlayerUUIDsInGroup:
                                    if state[0] != ZonePlayerUUID:
                                        for rdev in indigo.devices.iter("self.ZonePlayer"):
                                            if ZonePlayerUUID == rdev.states['ZP_LocalUID']:
                                                self.logger.info(f"add zone to group: {rdev.name}->{dev.name}")
                                                self.SOAPSend(rdev.pluginProps['address'], "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon:"+str(state[0])+"</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                                                updatedURI[rdev.id] = 1
                                                self.plugin.sleep(.5)

                            # restore mute
                            self.logger.debug(f"{state[0]}: Restore Mute: {state[4]}")
                            if state[4] == "0":
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                            else:
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                            # restore volume
                            self.logger.debug(f"{state[0]}: Restore Volume: {state[6]}")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume", "<Channel>Master</Channel><DesiredVolume>"+state[6]+"</DesiredVolume>")
                        else:
                            self.actionDirect(PA(dev.id, {'setting': group_volume}), "GroupVolume")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>" + group_mute + "</DesiredMute>")

                        # resture uri
                        if updatedURI[dev.id] == 0:
                            self.logger.debug(f"{state[0]}: Restore URI: {state[7]}")
                            SendVar = "<CurrentURI>" + state[7].replace("&", "&amp;") + "</CurrentURI><CurrentURIMetaData>" + state[8] + "</CurrentURIMetaData>"
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", SendVar.encode('utf-8'))
                            updatedURI[dev.id] = 1

            self.plugin.sleep(1)

            for item in AnnouncementZones:
                dev = indigo.devices[int(item)]
                zoneIP = dev.pluginProps["address"]
                CurrentTransportActions = self.parseCurrentTransportActions(self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetCurrentTransportActions", ""))

                for state in SavedState:
                    if state[0] == dev.states['ZP_LocalUID']:
                        # ZonePlayer is Group Coordinator and has a Current URI
                        if state[10] == "true":
                            if uri_music in dev.states['ZP_CurrentURI'] and int(dev.states['Q_Number']) > 0:
                                QueueReady = True
                            else:
                                QueueReady = False

                            if CurrentTransportActions.find("Seek") >= 0 and QueueReady:
                                # restore track number
                                self.logger.debug(f"{state[0]}: Restore Track Number: {state[9]}")
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+state[9]+"</Target>")
                                # restore rel time
                                self.logger.debug(f"{state[0]}: Restore Relative Time: {state[12]}")
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>REL_TIME</Unit><Target>"+state[12]+"</Target>")

                                # restore Q_Repeat
                                if state[2] == "off":
                                    Q_setting = 0
                                else:
                                    Q_setting = 1
                                self.actionDirect(PA(dev.id, {'setting': Q_setting}), "Q_Repeat")

                            # restore play state
                            self.logger.debug(f"{state[0]}: Restore Play State: {state[5]}")
                            if state[5] == "PLAYING":
                                self.actionDirect(PA(dev.id), "Play")
                            elif state[5] == "PAUSED":
                                self.actionDirect(PA(dev.id), "Play")
                                self.actionDirect(PA(dev.id), "Pause")
                            # else:
                            #    self.actionDirect(PA(dev.id), "Stop")

            AnnouncementZones = []
            actionBusy = 0

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def MicrosoftTranslateAuth(self):
        try:
            authUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13/'
            scopeUrl = 'http://api.microsofttranslator.com'
            grantType = 'client_credentials'

            postdata = {'grant_type': grantType, 'scope': scopeUrl, 'client_id': self.MSTranslateClientID, 'client_secret': self.MSTranslateClientSecret}
            response = requests.post(authUrl, data=postdata)

            if response.status_code == 200:
                content = json.loads(response.content)
                return content['access_token']
            else:
                self.logger.error(f"[{time.asctime()}] Cannot authenticate to Microsoft Translate")
                return False

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def MicrosoftTranslateLanguages(self):
        try:
            accessToken = self.MicrosoftTranslateAuth()
            if not accessToken:
                return False

            scopeUrl = 'http://api.microsofttranslator.com'
            headers = {'Content-Type': 'text/xml', 'Authorization': 'Bearer ' + accessToken}
            url = scopeUrl + '/V2/Http.svc/GetLanguagesForSpeak'
            response = requests.get(url, headers=headers)

            langCodes = []
            Languages = ET.fromstring(response.content)
            for lang in Languages:
                langCodes.append(lang.text)
            languageCodes = str(langCodes).replace("'", '"')

            # self.myLocale = self.getLocale()
            # if self.myLocale is None:
            self.myLocale = 'en'

            url = scopeUrl + '/V2/Ajax.svc/GetLanguageNames?locale=' + self.myLocale + '&languageCodes=' + languageCodes
            response = requests.post(url, headers=headers)

            name_code = dict(zip(langCodes, eval(response.content)))
            self.logger.info(f"Loaded Microsoft Translate Voices... [{len(name_code)}]")

            return name_code

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def MicrosoftTranslate(self, announcement, language):
        try:
            authUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13/'
            scopeUrl = 'http://api.microsofttranslator.com'
            speakUrl = 'http://api.microsofttranslator.com/V2/Http.svc/Speak'
            grantType = 'client_credentials'

            accessToken = self.MicrosoftTranslateAuth()
            if not accessToken:
                return False

            headers = {'Content-Type': 'audio/mp3', 'Authorization': 'Bearer ' + accessToken}
            url = speakUrl + '?text=' + announcement + '&language=' + language + '&format=audio/mp3&options=MaxQuality'

            with open('announcement.mp3', 'wb') as handle:
                response = requests.get(url, headers=headers, stream=True)

                if response.ok:
                    for block in response.iter_content(1024):
                        handle.write(block)
                    return True
                else:
                    return False

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getReferencePlayerIP(self):
        try:
            return soco.discover().pop().ip_address

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # Plugin Preferences
    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        try:
            if not userCancelled:
                self.logger.debug(f"[{time.asctime()}] Getting plugin preferences.")

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
                    if (self.HTTPStreamingIP != self.plugin.pluginPrefs["HTTPStreamingIP"]) or (self.HTTPStreamingPort != self.plugin.pluginPrefs["HTTPStreamingPort"]):
                        self.HTTPStreamingIP = self.plugin.pluginPrefs["HTTPStreamingIP"]
                        self.HTTPStreamingPort = self.plugin.pluginPrefs["HTTPStreamingPort"]

                        self.HTTPSTreamerOn = False
                        v = Thread(target=self.HTTPStreamer)
                        v.setDaemon(True)
                        v.start()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] HTTPStreamer not functioning.")

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

    def getZP_Pandora(self, filter=""):
        try:
            array = []
            for station in Sonos_Pandora:
                array.append((station[0], station[3] + ": " + station[1]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_SiriusXM(self, filter=""):
        try:
            array = []
            for channel in Sonos_SiriusXM:
                array.append((channel[1], channel[2]))
            # array.append((channel[3], str(channel[0]).zfill(3) + " | " + channel[4]))
            # array.sort(key=lambda x:x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

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

    def getMicrosoftLanguages(self, filter=""):
        try:
            array = []
            for code in self.MSTranslateVoices:
                array.append((code, self.MSTranslateVoices[code]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################
    # Utiliies

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
                self.logger.debug("---------------------------------------------")
            else:
                self.logger.info("---------------------------------------------")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def updateStateOnServer(self, dev, state, value):
        try:
            if self.plugin.stateUpdatesDebug:
                self.logger.debug(f"\t Updating Device: {dev.name}, State: {state}, Value: {value}")
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
                self.logger.debug("Replicate state to slave ZonePlayers...")
                ZonePlayerUUIDsInGroup = dev.states['ZonePlayerUUIDsInGroup'].split(',')
                for rdev in indigo.devices.iter("self.ZonePlayer"):
                    SlaveUID = rdev.states['ZP_LocalUID']
                    GROUP_Coordinator = rdev.states['GROUP_Coordinator']
                    if SlaveUID != dev.states['ZP_LocalUID'] and GROUP_Coordinator == "false" and SlaveUID in ZonePlayerUUIDsInGroup:
                        if state == "ZP_CurrentURI":
                            value = uri_group + dev.states['ZP_LocalUID']
                        if self.plugin.stateUpdatesDebug:
                            self.logger.debug(f"\t Updating Device: {rdev.name}, State: {state}, Value: {value}")
                        if value is None or value == "None":
                            rdev.updateStateOnServer(state, "")
                        else:
                            rdev.updateStateOnServer(state, value.encode('utf-8'))

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def updateStateOnSlaves(self, dev):
        try:
            self.logger.debug("Update all states to slave ZonePlayers...")
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
                            self.logger.debug(f"\t Updating Slave Device: {rdev.name}, State: {state}, Value: {value}")
                        rdev.updateStateOnServer(state, value)
                    rdev.updateStateOnServer("ZP_ART", dev.states['ZP_ART'])
                    try:
                        shutil.copy2("/Library/Application Support/Perceptive Automation/images/Sonos/"+dev.states['ZP_ZoneName']+"_art.jpg",
                                     "/Library/Application Support/Perceptive Automation/images/Sonos/"+rdev.states['ZP_ZoneName']+"_art.jpg")
                    except Exception as exception_error:
                        pass

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def copyStateFromMaster(self, dev):
        try:
            self.logger.debug("Copy states from master ZonePlayer...")
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
                            self.logger.debug(f"\t Updating Slave Device: {dev.name}, State: {state}, Value: {value}")
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

    def getSonosFavorites(self):
        try:
            global Sonos_Favorites
            Sonos_Favorites = []

            # list_count = 0
            # ZP  = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>FV:2</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"),1)
            # ZPxml = ET.fromstring(ZP)
            # iter = ZPxml.getiterator()
            # for element in iter:
            # 	if str(element).find("}item") >= 0:
            # 		if element.keys():
            # 			for name, value in element.items():
            # 				if name == "id":
            # 					e_id = value
            # 		for child in element.getchildren():
            # 			ctag = str(child.tag).split('}')
            # 			if ctag[1] == "title":
            # 				e_title = self.restoreString(child.text,0)
            # 			elif ctag[1] == "res":
            # 				e_res = self.restoreString(child.text,0)
            # 				e_res_clean = child.text
            # 			elif ctag[1] == "resMD":
            # 				e_resMD = child.text
            # 				# self.logger.info(f"resMD: {e_resMD}")
            # 				#e_class = self.parsePoint(e_resMD, "&lt;upnp:class&gt;", "&lt;/upnp:class&gt;")
            # 			elif ctag[1] == "ordinal":
            # 				e_ordinal = child.text
            # 		Sonos_Favorites.append ((e_res, e_title, e_resMD, e_res_clean, e_id))
            # 		self.logger.debug(f"\tSonos Favorites: {e_id}, {e_title}, {e_res}")
            # 		list_count = list_count + 1
            # self.logger.info(f"Loaded Sonos Favorites... [{list_count}]")

            res = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>FV:2</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"), 1)
            Favorites = ET.fromstring(res)
            for Favorite in Favorites.findall('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}item'):
                e_id = Favorite.attrib['id']
                e_res_clean = Favorite.findtext('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res')
                e_res = self.restoreString(e_res_clean, 0)
                e_title = self.restoreString(Favorite.findtext('.//{http://purl.org/dc/elements/1.1/}title'), 0)
                e_resMD = Favorite.findtext('.//{urn:schemas-rinconnetworks-com:metadata-1-0/}resMD')
                Sonos_Favorites.append((e_res, e_title, e_resMD, e_res_clean, e_id))
                self.logger.debug(f"\tSonos Favorites: {e_id}, {e_title}, {e_res}")
            self.logger.info(f"Loaded Sonos Favorites... [{len(Sonos_Favorites)}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getPlaylistsDirect(self):
        try:
            global Sonos_Playlists
            list_count = 0
            Sonos_Playlists = []
            ZP  = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>SQ:</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"), 1)
            # self.logger.debug(f"ZP: {ZP}")
            ZPxml = ET.fromstring(ZP)
            # iter = ZPxml.getiterator()
            iter = list(ZPxml.iter())
            for element in iter:
                if str(element).find("}container") >= 0:
                    if element.keys():
                        for name, value in element.items():
                            if name == "id":
                                e_id = value
                    # for child in element.getchildren():
                    for child in list(element.iter()):
                        ctag = str(child.tag).split('}')
                        if ctag[1] == "title":
                            e_title = self.restoreString(child.text, 0)
                        elif ctag[1] == "res":
                            e_res = child.text
                    Sonos_Playlists.append((e_res, e_title, e_id))
                    self.logger.debug(f"\tPlaylist: {e_id}, {e_title}, {e_res}")
                    list_count = list_count + 1
            self.logger.info(f"Loaded Playlists... [{list_count}]")
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getRT_FavStationsDirect(self):
        try:
            global Sonos_RT_FavStations
            list_count = 0
            Sonos_RT_FavStations = []
            ZP  = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>R:0/0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"), 1)
            # self.logger.debug(f"ZP: {ZP}")
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
                    self.logger.debug(f"\tRadioTime Favorite Station: {e_id}, {e_title}, {e_res}")
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
        try:
            global Sonos_Pandora
            list_count = 0
            # Sonos_Pandora = []

            pandora = Pandora()
            pandora.authenticate(PandoraEmailAddress, PandoraPassword)
            for station in pandora.get_station_list():
                Sonos_Pandora.append((station['stationId'], station['stationName'], PandoraEmailAddress, PandoraNickname))
                self.logger.debug(f"\tPandora: {station['stationId']}, {station['stationName']}, {PandoraNickname}")
                list_count = list_count + 1
            self.logger.info(f"Loaded Pandora Stations for {PandoraNickname}... [{list_count}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getSiriusXM(self):
        try:
            global Sonos_SiriusXM
            # list_count = 0
            Sonos_SiriusXM = []

            # attempt 1 with website scraping
            # url = "https://www.siriusxm.com/userservices/cl/en-us/xml/lineup/250/client/ump"
            # response = requests.get(url)
            # if response.ok:
            # 	root = ET.fromstring(response.content)
            # 	for Channel in root.findall('.//channels'):
            # 		Sonos_SiriusXM.append((int(Channel.findtext('siriusChannelNo')), int(Channel.findtext('xmChannelNo')), Channel.findtext('channelKey'), Channel.findtext('contentId'), Channel.findtext('name')))
            #       self.logger.debug( f'\tSiriusXM: {Channel.findtext("siriusChannelNo")}|{Channel.findtext("xmChannelNo")}|{Channel.findtext("channelKey")}|{Channel.findtext("contentId")}|{Channel.findtext("name")}')
            #       list_count = list_count + 1
            #   Sonos_SiriusXM.sort(key=lambda x:x[0])
            #   self.logger.info(f"Loaded SiriusXM Stations.. [{list_count}]")
            # else:
            #   self.logger.error(f"[{time.asctime()}] Error getting SiriusXM Channel Lineup")

            # attempt 2 with MusicService
            # try:
            #   SiriusXMChannels = MusicService('SiriusXM').get_metadata(item='live_category:all_channels', count=500)
            #   for item in SiriusXMChannels:
            #       Sonos_SiriusXM.append((int(item.title.split('-')[0]), item.id, item.title))
            #       self.logger.debug(f'\tSiriusXM: {item.title}')
            #   Sonos_SiriusXM.sort(key=lambda x:x[0])
            #   self.logger.info(f"Loaded SiriusXM Stations.. [{len(SiriusXMChannels)}]")
            # except Exception as exception_error:
            #   self.logger.error(f"[{time.asctime()}] Error getting SiriusXM Channel Lineup")

            # attempt 3 with Sonos Music API
            headers = {'Content-Type': 'text/xml; charset="utf-8"',	 'Host': 'sonos.mountain.siriusxm.com', 'User-Agent': 'Indigo', 'CONNECTION': 'close', 'ACCEPT-ENCODING': 'gzip', 'ACCEPT-LANGUAGE': 'en-US'}
            base_url = 'http://sonos.mountain.siriusxm.com/server.php'
            namespaces = {'ns0': 'http://schemas.xmlsoap.org/soap/envelope', 'ns1': 'http://www.sonos.com/Services/1.1'}

            SoapMessage = (
                    '<?xml version="1.0" encoding="utf-8"?>'
                    '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
                    '<s:Header>'
                    '<credentials xmlns="http://www.sonos.com/Services/1.1">'
                    '<deviceId>' + self.SonosDeviceID + '</deviceId>'
                                                        '<deviceProvider>Sonos</deviceProvider>'
                                                        '</credentials>'
                                                        '</s:Header>'
                                                        '<s:Body>'
                                                        '<getSessionId xmlns="http://www.sonos.com/Services/1.1">'
                                                        '<username>' + self.SiriusXMID + '</username>'
                                                                                         '<password>' + self.SiriusXMPassword + '</password>'
                                                                                                                                '</getSessionId>'
                                                                                                                                '</s:Body>'
                                                                                                                                '</s:Envelope>')

            headers['SOAPACTION'] = 'http://www.sonos.com/Services/1.1#getSessionId'
            headers['Content-Length'] = str(len(SoapMessage))

            try:
                response = requests.post(base_url, headers=headers, data=SoapMessage.encode("utf-8"))
                root = ET.fromstring(response.content)
                SessionID = root.findtext('.//ns1:getSessionIdResult', namespaces=namespaces)
            except Exception as exception_error:
                self.logger.error(f"[{time.asctime()}] SiriusXM SessionID communications error: {exception_error}")
                return

            if SessionID is None:
                self.logger.error(f"[{time.asctime()}] SiriusXM SessionID error, check credentials")
                return

            SoapMessage = (
                    '<?xml version="1.0" encoding="utf-8"?>'
                    '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
                    '<s:Header>'
                    '<credentials xmlns="http://www.sonos.com/Services/1.1">'
                    '<sessionId>' + SessionID + '</sessionId>'
                                                '<deviceId>' + self.SonosDeviceID + '</deviceId>'
                                                                                    '<deviceProvider>Sonos</deviceProvider>'
                                                                                    '</credentials>'
                                                                                    '</s:Header>'
                                                                                    '<s:Body>'
                                                                                    '<getMetadata xmlns="http://www.sonos.com/Services/1.1">'
                                                                                    '<id>live_category:all_channels</id>'
                                                                                    '<index>0</index>'
                                                                                    '<count>500</count>'
                                                                                    '</getMetadata>'
                                                                                    '</s:Body>'
                                                                                    '</s:Envelope>')

            headers['SOAPACTION'] = 'http://www.sonos.com/Services/1.1#getMetadata'
            headers['Content-Length'] = str(len(SoapMessage))

            try:
                response = requests.post(base_url, headers=headers, data=SoapMessage.encode("utf-8"))
                root = ET.fromstring(response.content)
                for item in root.findall('.//ns1:mediaMetadata', namespaces):
                    xm_id = item.findtext('ns1:id', namespaces=namespaces)
                    xm_title = item.findtext('ns1:title', namespaces=namespaces)
                    Sonos_SiriusXM.append((int(xm_title.split('-')[0]), xm_id, xm_title))
                    self.logger.debug(f'\tSiriusXM: {xm_title}')
                Sonos_SiriusXM.sort(key=lambda x: x[0])
                self.logger.info(f"Loaded SiriusXM Stations.. [{len(Sonos_SiriusXM)}]")
            except Exception as exception_error:
                self.logger.error(f"[{time.asctime()}] Error getting SiriusXM Channel Lineup")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getSoundFiles(self):
        try:
            global Sound_Files
            list_count = 0
            Sound_Files = []

            for f in listdir(self.SoundFilePath):
                if ".mp3" in f:
                    Sound_Files.append(f)
                    self.logger.debug(f"\tSound File: {f}")
                    list_count = list_count + 1

            self.logger.info(f"Loaded Sound Files... [{list_count}]")
        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement
