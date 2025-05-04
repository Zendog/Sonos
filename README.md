# Sonos
This version (1.0.2):
1. Updated soco library to - 0.30.9 for better control function support and overall stability.
2. Rewrote and fixed subscription services, includes fallback subscription upon failure to address devices falling of network.
3. Added menu option for dumping subscribed devices to the log as diagnostic aid on subscripition failures.
4. Rewrote discover to facilitate VLAN access for dedicated SONOS VLAN network access and control.
5. Rewrote and corrected volume controls.
6. Rewrote and corrected Bass and Treble controls.
7. Implemented SiriusXM login and channel processing.
8. Added menu options for dumping registered available XM Channel list to the log.
9. Rewrote and corrected Pandora loging / crypto processing from python 2 to python 3 based calls.
10. Implemented Pandora login and channel processing.
11. Added additional modules to requirements.txt.
12. Added Artwork / Metadata server.
13. Added menu option for dumping group device inventory / master controller identification to the log (matrixed Sonos SOCO Name / IP ADDRESS / Indigo Name / Indigo Device ID) for device management insight clarification.
14. Updated group controls to copy master controller enriched metadata states to all associated devices in the current device grouping.
