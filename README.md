# Sonos
This is the repo for the open-sourced Sonos plugin which is a Python 3 development of the Sonos plugin originally developed by Nick [@nlagaros on the Indigo forums].

A huge shoutout is due to Nick for originally providing this plugin and for supporting it for so many years!

This plugin is currently in  a very early beta and has had limited testing. Specially, Pandora and SiriusXM have not been tested and will likely not work at the moment.

As part of the migration to Python 3, the majority of the Python packages used by the plugin have to be installed via a *pip3.10 install \<package name\>* terminal command. In the fullness of time it is anticipated that Indigo will have a mechanism to install required packages.

The only exception to this is the SoCo package and Lame which are both included in the plugin. The reason for this is that SoCo package has been modified for this plugin's use and Lame would have to be installed by Homebrew. 

