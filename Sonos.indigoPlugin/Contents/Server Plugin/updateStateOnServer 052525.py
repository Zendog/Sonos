

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


