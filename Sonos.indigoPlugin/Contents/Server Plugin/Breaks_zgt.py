
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
            sid = getattr(event_obj, "sid", "").lower()
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
            "zonegrouptopology" in sid or
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

            if "GroupStateChanged" in getattr(event_obj, "variables", {}):
                self.logger.info("🔄 GroupStateChanged variable present — triggering group state refresh...")
                return

            if not zone_ip:
                zone_ip = "unknown"

            state_updates = {}

            self.safe_debug(f"🧪 Event handler fired! SID={getattr(event_obj, 'sid', 'N/A')} zone_ip={zone_ip} Type={type(event_obj)}")
            self.safe_debug(f"🧑‍💻 Full event variables: {getattr(event_obj, 'variables', {})}")
