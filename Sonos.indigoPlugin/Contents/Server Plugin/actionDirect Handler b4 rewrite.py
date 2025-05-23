
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
                "actionZP_addPlayerToZone": lambda p, d, z: self.handleAction_ZP_addPlayerToZone(p, d, z),                
                "actionZP_setStandalone": lambda p, d, z: self.handleAction_ZP_setStandalone(p, d, z),
                "actionQ_Shuffle": lambda p, d, z: self.handleAction_Q_Shuffle(p, d, z),
                "actionQ_Crossfade": lambda p, d, z: self.handleAction_Q_Crossfade(p, d, z),
            }

            if action_id in dispatch_table:
                dispatch_table[action_id](pluginAction, dev, zoneIP)
                return




            # Inline action handlers follow...
            #DT Added 052125


            if action_id != "setStandalones":

                dev = indigo.devices[pluginAction.deviceId]
                zoneIP = dev.pluginProps["address"]

                if dev.states["GROUP_Coordinator"] == "false":
                    Coordinator = dev.states["GROUP_Name"]
                    for idev in indigo.devices.iter("self.ZonePlayer"):
                        if idev.states["GROUP_Coordinator"] == "true" and idev.states["GROUP_Name"] == Coordinator:
                            CoordinatorIP = idev.pluginProps["address"]
                            CoordinatorDev = idev
                            break


            # Get the Indigo device and its IP
            dev = indigo.devices[pluginAction.deviceId]
            zoneIP = dev.pluginProps.get("address", "").strip()

            # Determine coordinator dynamically
            coordinator_dev = self.getCoordinatorDevice(dev)
            coordinator_ip = coordinator_dev.pluginProps.get("address", "").strip()

            # Redirect zoneIP to coordinator if dev is a grouped slave
            if coordinator_dev.id != dev.id:
                self.logger.debug(f"🔁 Redirecting action from {dev.name} to coordinator {coordinator_dev.name}")
                zoneIP = coordinator_ip
            else:
                self.logger.debug(f"✅ {dev.name} is the coordinator — executing command directly")

            # Handle action types
            if action_id == "Play":
                self.plugin.debugLog("Sonos Action: Play")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                indigo.server.log(f"ZonePlayer: {dev.name}, Play")

            elif action_id == "TogglePlay":
                self.plugin.debugLog("Sonos Action: Toggle Play")
                current_state = dev.states.get("ZP_STATE", "")
                if current_state == "PLAYING":
                    self.actionDirect(pluginAction, "Pause")
                    indigo.server.log(f"ZonePlayer: {dev.name}, Pause")
                else:
                    self.actionDirect(pluginAction, "Play")
                    indigo.server.log(f"ZonePlayer: {dev.name}, Play")

            elif action_id == "Pause":
                self.plugin.debugLog("Sonos Action: Pause")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                indigo.server.log(f"ZonePlayer: {dev.name}, Pause")

            elif action_id == "Stop":
                self.plugin.debugLog("Sonos Action: Stop")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                indigo.server.log(f"ZonePlayer: {dev.name}, Stop")

    

            elif action_id == "MuteToggle":
                self.plugin.debugLog("Sonos Action: Mute Toggle")
                if int(dev.states["ZP_MUTE"]) == 0:
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                    indigo.server.log("ZonePlayer: %s, Mute On" % dev.name)
                else:
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                    indigo.server.log("ZonePlayer: %s, Mute Off" % dev.name)
            elif action_id == "MuteOn":
                self.plugin.debugLog("Sonos Action: Mute On")
                self.SOAPSend (zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                indigo.server.log("ZonePlayer: %s, Mute On" % dev.name)
            elif action_id == "MuteOff":
                self.plugin.debugLog("Sonos Action: Mute Off")
                self.SOAPSend (zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                indigo.server.log("ZonePlayer: %s, Mute Off" % dev.name)

            elif action_id == "GroupMuteToggle":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP          
                self.plugin.debugLog("Sonos Action: Group Mute Toggle")
                if int(self.parseCurrentMute (self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", ""))) == 0:
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>1</DesiredMute>")
                    indigo.server.log("ZonePlayer Group: %s, Mute On" % dev.name)
                else:
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>0</DesiredMute>")
                    indigo.server.log("ZonePlayer Group: %s, Mute Off" % dev.name)
            elif action_id == "GroupMuteOn":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP          
                self.plugin.debugLog("Sonos Action: Group Mute On")
                self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>1</DesiredMute>")
                indigo.server.log("ZonePlayer Group: %s, Mute On" % dev.name)
            elif action_id == "GroupMuteOff":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP          
                self.plugin.debugLog("Sonos Action: Group Mute Off")
                self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>0</DesiredMute>")
                indigo.server.log("ZonePlayer Group: %s, Mute Off" % dev.name)
            elif action_id == "GroupVolume":
                self.plugin.debugLog("Sonos Action: Group Volume")
                current_volume = self.parseCurrentVolume (self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = int(eval(self.plugin.substitute(pluginAction.props.get("setting"))))
                if new_volume < 0 or new_volume > 100:
                    new_volume = current_volume
                self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume", "<DesiredVolume>"+str(new_volume)+"</DesiredVolume>")
                indigo.server.log(u"ZonePlayer Group: %s, Current Group Volume: %s, New Group Volume: %s" % (dev.name, current_volume, new_volume))
            elif action_id == "RelativeGroupVolume":
                self.plugin.debugLog("Sonos Action: Relative Group Volume")
                current_volume = self.parseCurrentVolume (self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                adjustment = pluginAction.props.get("setting")
                new_volume = int(current_volume) + int(adjustment)
                if new_volume < 0:
                    new_volume = 0
                if new_volume > 100:
                    new_volume = 100
                self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>"+adjustment+"</Adjustment>")
                indigo.server.log(u"ZonePlayer Group: %s, Current Group Volume: %s, New Group Volume: %s" % (dev.name, current_volume, new_volume))
            elif action_id == "GroupVolumeDown":
                self.plugin.debugLog("Sonos Action: Group Volume Down")
                current_volume = self.parseCurrentVolume (self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = int(current_volume) - 2
                if new_volume < 0:
                    new_volume = 0
                self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>-2</Adjustment>")
                indigo.server.log(u"ZonePlayer Group: %s, Current Group Volume: %s, New Group Volume: %s" % (dev.name, current_volume, new_volume))
            elif action_id == "GroupVolumeUp":
                self.plugin.debugLog("Sonos Action: Group Volume Up")
                current_volume = self.parseCurrentVolume (self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = int(current_volume) + 2
                if new_volume > 100:
                    new_volume = 100
                self.SOAPSend (zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>2</Adjustment>")
                indigo.server.log(u"ZonePlayer Group: %s, Current Group Volume: %s, New Group Volume: %s" % (dev.name, current_volume, new_volume))


            elif action_id == "Q_Crossfade":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                mode = pluginAction.props.get("setting")
                if mode == 0:
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>0</CrossfadeMode>")
                elif mode == 1:
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>1</CrossfadeMode>")
            elif action_id == "Q_Repeat":
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
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
            elif action_id == "Q_RepeatOne":
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
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
            elif action_id == "Q_RepeatToggle":
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
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
            elif action_id == "Q_Shuffle":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                shuffle = bool(int(pluginAction.props.get("setting")))
                repeat = self.boolConv(dev.states["Q_Repeat"])
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                PlayMode = self.QMode(repeat, repeat_one, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
            elif action_id == "Q_ShuffleToggle":
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
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
            elif action_id == "Q_Clear":
                self.SOAPSend (zoneIP, "/MediaRenderer", "/Queue", "RemoveAllTracks", "<QueueID>0</QueueID><UpdateID>0</UpdateID>")
                indigo.server.log("ZonePlayer: %s, Clear Queue" % dev.name)

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

            elif action_id == "CD_RemovePlaylist":
                ObjectID = pluginAction.props.get("setting")
                for plist in Sonos_Playlists:
                    if plist[2] == ObjectID:
                        PlaylistName = plist[1]
                        self.SOAPSend (zoneIP, "/MediaServer", "/ContentDirectory", "DestroyObject", "<ObjectID>" + ObjectID + "</ObjectID>")
                    indigo.server.log ("ZonePlayer: %s, Remove Playlist: %s" % (dev.name, PlaylistName))



            #End of DT Added 052125





            if action_id == "actionBassUp":
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

            elif action_id == "actionVolumeUp":
                self.safe_debug("🧪 Matched action_id == actionVolumeUp")
                current = int(dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = min(100, current + 5)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")
                self.logger.info(f"🔊 Volume UP for {dev.name}: {current} → {new_volume}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionVolumeDown":
                current = int(dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = max(0, current - 5)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")
                self.logger.info(f"🔉 Volume DOWN for {dev.name}: {current} → {new_volume}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionMuteToggle":
                raw_state = dev.states.get("ZP_MUTE", "unknown")
                mute_state = raw_state.lower() == "true"
                mute_val = "0" if mute_state else "1"
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              f"<Channel>Master</Channel><DesiredMute>{mute_val}</DesiredMute>")
                self.logger.info(f"🎚 Mute TOGGLE for {dev.name}: {'Off' if mute_state else 'On'}")
                self.refresh_transport_state(zoneIP)
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





            elif action_id == "setStandalone":
                indigo.server.log("remove zone from group: %s" % dev.name)
                if dev.states['GROUP_Coordinator'] == "true":
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev.states['ZP_LocalUID'])+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
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

            elif action_id == "setStandalones":
                zones = []
                x = 1
                while x <= 12:
                    ivar = 'zp' + str(x)
                    if pluginAction.props.get(ivar) not in ["", None, "00000"]: 
                        zones.append(pluginAction.props.get(ivar))
                    x = x + 1
                
                for item in zones:
                    indigo.server.log("remove zone from group: %s" % item)
                    dev = indigo.devices[int(item)]
                    if dev.states['GROUP_Coordinator'] == "true":
                        self.SOAPSend (dev.pluginProps["address"], "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")
                    self.SOAPSend (dev.pluginProps["address"], "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev.states['ZP_LocalUID'])+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")


### end of placeholder



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
