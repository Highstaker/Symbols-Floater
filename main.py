#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gtk, GObject
import signal
from unity_applet import FloaterApplet


def main():
	# Catch CTRL-C
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	GObject.threads_init()

	floater = FloaterApplet()

	Gtk.main()

if __name__ == '__main__':
	main()