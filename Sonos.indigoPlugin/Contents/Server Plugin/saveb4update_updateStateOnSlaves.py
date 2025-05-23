
    def updateStateOnSlaves(self, dev):
        self.logger.info(f"✅ Update States On Slaves 1")

        try:
            self.safe_debug("Update all states to slave ZonePlayers...")

            device_ip = dev.address.strip()
            soco_device = self.soco_by_ip.get(device_ip)
            if not soco_device:
                self.logger.warning(f"⚠️ No SoCo device found for IP {device_ip}")
                return

            group = soco_device.group
            coordinator = group.coordinator
            devices_in_group = group.members
            coordinator_ip = coordinator.ip_address.strip()

            self.safe_debug(f"🧑‍💻 Devices in group: {[device.ip_address for device in devices_in_group]}")

            coordinator_dev = self.ip_to_indigo_device.get(coordinator_ip)
            if not coordinator_dev:
                self.logger.warning(f"⚠️ Coordinator Indigo device not found for IP {coordinator_ip}; skipping slave updates")
                return

            master_group_name = coordinator.player_name or "Unknown Group"

            # Ensure coordinator ZP_ART state is initialized
            art_url = coordinator_dev.states.get("ZP_ART", "")
            if not art_url or "default" in art_url:
                self.logger.warning(f"📸 Coordinator {coordinator_dev.name} missing or using default artwork — triggering refresh")
                self.update_album_artwork(dev=coordinator_dev)

            # Identify all slave devices in the group
            slave_devices = []
            group_member_ips = {member.ip_address.strip() for member in devices_in_group}

            for indigo_device in indigo.devices:
                dev_ip = indigo_device.address.strip()
                if dev_ip != coordinator_ip and dev_ip in group_member_ips:
                    slave_devices.append(indigo_device)

            # Update slave group metadata and sync artwork
            for slave_dev in slave_devices:
                slave_dev.updateStateOnServer("GROUP_Coordinator", "false")
                slave_dev.updateStateOnServer("GROUP_Name", master_group_name)

            # Update devices that are now standalone
            # Update devices that are now standalone
            for indigo_device in indigo.devices.iter("self"):  # Ensures only Sonos plugin devices
                ip_clean = indigo_device.address.strip()
                soco_dev = self.soco_by_ip.get(ip_clean)

                if not soco_dev or not soco_dev.group:
                    continue  # Skip if this Sonos device is not in the group map

                if ip_clean not in group_member_ips and ip_clean != coordinator_ip:
                    try:
                        if soco_dev.group.coordinator.ip_address.strip() == ip_clean:
                            indigo_device.updateStateOnServer("GROUP_Coordinator", "true")
                            indigo_device.updateStateOnServer("GROUP_Name", soco_dev.player_name)
                            self.safe_debug(f"🔄 Updated standalone device {indigo_device.name} → Coordinator: true, Group Name: {soco_dev.player_name}")
                    except Exception as e:
                        self.logger.warning(f"⚠️ Error updating standalone device {indigo_device.name}: {e}")

            # Sync all group artwork using centralized logic
            self.update_album_artwork(dev=coordinator_dev)

        except Exception as e:
            self.exception_handler(e, True)