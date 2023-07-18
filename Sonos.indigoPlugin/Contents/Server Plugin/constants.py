#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging

# ============================== Custom Imports ===============================
try:
    import indigo  # noqa
except ImportError:
    pass

number = -1

debug_show_constants = False
debug_use_labels = True

# def constant_id(constant_label) -> int:  # Auto increment constant id

def constant_id(constant_label):  # Auto increment constant id

    global number
    if debug_show_constants and number == -1:
        indigo.server.log("Zigbee2MQTT Bridge Plugin internal Constant Name mapping ...", level=logging.DEBUG)
    number += 1
    if debug_show_constants:
        indigo.server.log(f"{number}: {constant_label}", level=logging.DEBUG)
    if debug_use_labels:
        return constant_label
    else:
        return number

# plugin Constants


try:
    # noinspection PyUnresolvedReferences
    import indigo
except ImportError:
    pass
ADDRESS = constant_id("ADDRESS")
API_VERSION = constant_id("API_VERSION")
PATH = constant_id("PATH")
PLUGIN_DISPLAY_NAME = constant_id("PLUGIN_DISPLAY_NAME")
PLUGIN_ID = constant_id("PLUGIN_ID")
PLUGIN_INFO = constant_id("PLUGIN_INFO")
PLUGIN_PREFS_FILE = constant_id("PLUGIN_PREFS_FILE")
PLUGIN_PREFS_FOLDER = constant_id("PLUGIN_PREFS_FOLDER")
PLUGIN_VERSION = constant_id("PLUGIN_VERSION")
PLUGIN_PACKAGES_FOLDER = constant_id("PLUGIN_PACKAGES_FOLDER")

LOG_LEVEL_NOT_SET = 0
LOG_LEVEL_DEBUGGING = 10
LOG_LEVEL_TOPIC = 15
LOG_LEVEL_INFO = 20
LOG_LEVEL_WARNING = 30
LOG_LEVEL_ERROR = 40
LOG_LEVEL_CRITICAL = 50

 # LOG_LEVEL_TRANSLATION = dict()
# LOG_LEVEL_TRANSLATION[LOG_LEVEL_NOT_SET] = "Not Set"
# LOG_LEVEL_TRANSLATION[LOG_LEVEL_DEBUGGING] = "Topic Filter Logging"
# LOG_LEVEL_TRANSLATION[LOG_LEVEL_INFO] = "Info"
# LOG_LEVEL_TRANSLATION[LOG_LEVEL_WARNING] = "Warning"
# LOG_LEVEL_TRANSLATION[LOG_LEVEL_ERROR] = "Error"
# LOG_LEVEL_TRANSLATION[LOG_LEVEL_CRITICAL] = "Critical"

# # QUEUE Priorities
# QUEUE_PRIORITY_STOP_THREAD    = 0
# QUEUE_PRIORITY_COMMAND_HIGH   = 100
# QUEUE_PRIORITY_COMMAND_MEDIUM = 200
# QUEUE_PRIORITY_POLLING        = 300
# QUEUE_PRIORITY_LOW            = 400

