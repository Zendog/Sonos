
    def refresh_group_membership(self, indigo_device, soco_device):
        try:
            group = soco_device.group
            coordinator = group.coordinator
            devices_in_group = group.members

            coordinator_ip = coordinator.ip_address.strip()
            is_coordinator = (coordinator_ip == indigo_device.address.strip())
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

                indigo_device.updateStateOnServer("ZP_STATE", zp_state)
                indigo_device.updateStateOnServer("ZP_TRACK", current_title or "")
                indigo_device.updateStateOnServer("ZP_ARTIST", current_artist or "")
                indigo_device.updateStateOnServer("ZP_CurrentTrackURI", current_track_uri or "")

                self.safe_debug(f"🔄 Refreshed standalone states for {indigo_device.name} → State: {zp_state}, Track: {current_title}, Artist: {current_artist}")

            else:
                # === Sync slave states from coordinator device ===
                master_dev = next(
                    (dev for dev in indigo.devices if dev.address.strip() == coordinator_ip),
                    None
                )

                if master_dev:
                    for state_key in ["ZP_STATE", "ZP_TRACK", "ZP_ARTIST", "ZP_CurrentTrackURI", "ZP_ART"]:
                        master_value = master_dev.states.get(state_key, "")
                        indigo_device.updateStateOnServer(state_key, master_value)
                        self.safe_debug(f"🔄 Synced slave {indigo_device.name} {state_key} → {master_value}")
                else:
                    self.logger.warning(f"⚠️ Could not find master device {coordinator_ip} to sync states for slave {indigo_device.name}")

        except Exception as e:
            self.logger.error(f"❌ Exception in refresh_group_membership for {indigo_device.name}: {e}")
