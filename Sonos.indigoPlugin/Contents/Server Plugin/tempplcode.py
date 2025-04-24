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