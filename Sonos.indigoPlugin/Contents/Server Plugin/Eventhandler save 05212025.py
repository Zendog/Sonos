
    #######################################################################################################################################
    ### Event Handler to process lightweight soco state changes (sound related kind of things) and retrieve current dynamic state updates
    #######################################################################################################################################


    def soco_event_handler(self, event_obj):
        import copy

        try:
            #self.logger.warning("📥 Raw Event Object Received:")
            #self.logger.warning(f"   ⤷ service: {getattr(event_obj.service, 'service_type', '?')}")
            #self.logger.warning(f"   ⤷ sid: {getattr(event_obj, 'sid', '?')}")
            soco_ip = getattr(getattr(event_obj, "soco", None), "ip_address", "(no soco)")
            #self.logger.warning(f"   ⤷ soco.ip: {soco_ip}")
            #self.logger.warning(f"   ⤷ variables: {event_obj.variables}")
        except Exception as log_err:
            self.logger.error(f"❌ Failed to log raw event object: {log_err}")

        service_type = getattr(event_obj.service, "service_type", "").lower()
        sid = getattr(event_obj, "sid", "").lower()
        zone_ip = getattr(getattr(event_obj, "soco", None), "ip_address", None)

        is_zgt_event = (
            "zonegrouptopology" in service_type or
            "zonegrouptopology" in sid or
            "zone_group_state" in event_obj.variables or
            "ZoneGroupState" in event_obj.variables
        )

        if is_zgt_event:
            self.logger.warning(f"🔎 ZoneGroupTopology event triggered by {zone_ip}")
            zone_state_xml = (
                event_obj.variables.get("zone_group_state") or
                event_obj.variables.get("ZoneGroupState") or
                ""
            )

            if not zone_state_xml:
                self.logger.warning(f"⚠️ ZoneGroupTopology event from {zone_ip} missing ZoneGroupState")
            else:
                #self.logger.warning(f"📄 ZoneGroupState XML 3 received from {zone_ip}:\n{zone_state_xml}")
                try:
                    parsed_groups = self.parse_zone_group_state(zone_state_xml)
                    if not parsed_groups:
                        self.logger.warning("⚠️ Parsed zone group data was empty.")
                    else:
                        self.logger.warning(f"🧪 Parsed {len(parsed_groups)} group(s) from XML. Caching now...")
                        with self.zone_group_state_lock:
                            self.zone_group_state_cache = copy.deepcopy(parsed_groups)
                            self.logger.warning(f"💾 zone_group_state_cache updated with {len(self.zone_group_state_cache)} group(s)")

                        self.logger.warning("📊 Parsed Zone Group Summary:")
                        for group_id, data in parsed_groups.items():
                            #self.logger.warning(f"🧩 Group ID: {group_id} (Coordinator UUID: {data['coordinator']})")
                            for m in data["members"]:
                                bonded_flag = " (Bonded)" if m["bonded"] else ""
                                coord_flag = " (Coordinator)" if m["coordinator"] else ""
                                self.logger.warning(f"   → {m['name']} @ {m['ip']}{bonded_flag}{coord_flag}")

                        self.logger.warning("📣 Calling evaluate_and_update_grouped_states() after ZoneGroupTopology change...")
                        self.evaluate_and_update_grouped_states()
                        # NEW: propagate the updated Grouped state to all Indigo devices
                        self.logger.warning("📣 Propagating updated Grouped states to all devices...")
                        for dev in indigo.devices.iter("self"):
                            self.updateZoneGroupStates(dev)                        
                except Exception as e:
                    self.logger.error(f"❌ Failed to parse ZoneGroupState XML: {e}")

        try:
            service_type = getattr(event_obj.service, "service_type", "UNKNOWN")
            sid = getattr(event_obj, "sid", "N/A")
            zone_ip = getattr(event_obj, "zone_ip", None)

            self.logger.warning(f"📥 RAW EVENT RECEIVED — service: {service_type} | sid: {sid}")

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
                self.logger.warning(f"⚠️ Event received with unknown SID {sid}. Cannot map to Indigo device.")
                return

            #self.logger.debug(f"📡 Event received from {zone_ip} — SID={sid} | Service={service_type}")
            #self.logger.debug(f"📦 Event variables: {getattr(event_obj, 'variables', {})}")

            if "GroupStateChanged" in getattr(event_obj, "variables", {}):
                self.logger.info("🔄 GroupStateChanged variable present — triggering group state refresh...")
                return

            if not zone_ip:
                zone_ip = "unknown"

            state_updates = {}

            self.safe_debug(f"🧪 Event handler fired! SID={getattr(event_obj, 'sid', 'N/A')} zone_ip={zone_ip} Type={type(event_obj)}")
            self.safe_debug(f"🧑‍💻 Full event variables: {getattr(event_obj, 'variables', {})}")

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

            def safe_call(val):
                try:
                    return val() if callable(val) else val
                except Exception:
                    return ""

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

            soco_device = self.getSoCoDeviceByIP(indigo_device.address)
            if soco_device:
                self.refresh_group_membership(indigo_device, soco_device)
                self.logger.debug(f"🔁 Forcing master state save and slave updates for {indigo_device.name}")
                self.evaluate_and_update_grouped_states()                
                #self.updateStateOnSlaves(indigo_device)
            else:
                self.logger.warning(f"⚠️ Could not refresh group membership: No SoCo device for {indigo_device.name}")


            # 🔄 Heavyweight event processing
            self.handle_heavyweight_updates(event_obj, indigo_device, dev_id, zone_ip, state_updates)




            # 🖼️ Only trigger artwork update if this is an AVTransport event and the device is known
            if service_type.lower() == "avtransport":
                if indigo_device:
                    try:
                        self.safe_debug(f"🎨 Attempting artwork update for {indigo_device.name} (IP: {indigo_device.address})")
                        self.update_album_artwork(event_obj=event_obj, dev=indigo_device)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to update album artwork: {e}")
                else:
                    self.logger.warning("⚠️ Skipping artwork update — indigo_device could not be resolved for AVTransport event")
            else:
                self.safe_debug(f"🎨 Skipping artwork update — event service_type={service_type} (only AVTransport allowed)")



        except Exception as e:
            self.logger.error(f"❌ Error in soco_event_handler: {e}")


