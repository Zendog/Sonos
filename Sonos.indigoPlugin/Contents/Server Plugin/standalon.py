

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
                return