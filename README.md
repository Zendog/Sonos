# Sonos
This is the repo for the open-sourced Sonos plugin which is a Python 3 development of the Sonos plugin originally developed by Nick [@nlagaros on the Indigo forums].

A huge shoutout is due to Nick for originally providing this plugin and for supporting it for so many years!

This plugin is has now been released to the Indigo Plugin Store and has moved out of beta.

There are some outstanding issues: SiriusXM doesn't work and some player states aren't updating.

As part of the migration to Python 3, the majority of the Python packages used by the plugin have to be installed via a *pip3.10 install \<package name\>* terminal command. In the fullness of time it is anticipated that Indigo will have a mechanism to install required packages. Missing packages are identified in the Indigo Event Log and the required pip3.10 commands can be copied from the Indigo Event Log and pasted into a terminal session.

The only exception to this is the SoCo package and Lame which are both included in the plugin. The reason for this is that SoCo package has been modified for this plugin's use and Lame would have to be installed by Homebrew. 

