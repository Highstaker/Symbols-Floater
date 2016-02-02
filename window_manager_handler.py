#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Wnck, Gtk

class ScreenHandler(object):
	"""docstring for ScreenHandler"""
	def __init__(self):
		super(ScreenHandler, self).__init__()

		self.wm_screen = Wnck.Screen.get_default()

	def getActiveWindow(self):
		self.wm_screen.force_update()
		self.wm_screen.get_active_window()

	def activateWindow(self, window):
		stamp = Gtk.get_current_event_time()
		window.activate(stamp)
