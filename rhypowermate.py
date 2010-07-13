#!/usr/bin/python

import powermate
import dbus

EVENT_BUTTON_PRESS = 1
EVENT_RELATIVE_MOTION = 2

DBUS_START_REPLY_SUCCESS = 1
DBUS_START_REPLY_ALREADY_RUNNING = 2

bus = dbus.SessionBus()
(success, status) = bus.start_service_by_name('org.gnome.Rhythmbox')

session_bus = dbus.SessionBus()
proxy_obj = session_bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
         
player = dbus.Interface(proxy_obj, 'org.gnome.Rhythmbox.Player')


pm = powermate.PowerMate("/dev/powermate")
while 1:
	event = pm.WaitForEvent(-1)
	if (event[2] == EVENT_BUTTON_PRESS and event[4] == 0):
		player.playPause(1)
		if player.getPlaying():
			pm.SetLEDState((int)(player.getVolume() * 255), 0, 0, 0, 0);
		else:
			pm.SetLEDState(255, 252, 1, 1, 1);
	elif (event[2] == EVENT_RELATIVE_MOTION and player.getPlaying()):
		player.setVolumeRelative(event[4] * 0.02)
		pm.SetLEDState((int)(player.getVolume() * 255), 0, 0, 0, 0);
