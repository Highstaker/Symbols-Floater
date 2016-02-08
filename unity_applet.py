#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from os import path
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
from symbols_floater_window import SymbolsFloater

SCRIPT_DIRECTORY = path.dirname(path.realpath(__file__))


class FloaterApplet:
	"""Class defining the taskbar applet"""
	def __init__(self):
		super(FloaterApplet, self).__init__()

		# Path to applet icon
		icon_path = path.join(SCRIPT_DIRECTORY, "icons", "indicator_icon.svg")
		# Init the indicator
		self.ind = appindicator.Indicator.new("floater", icon_path, appindicator.IndicatorCategory.OTHER)
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

		self._setMenus()

		self.floaterWindow = SymbolsFloater()

		# Opens the Floater when you scroll mouse wheel over the applet icon
		self.ind.connect("scroll-event", self._showWindow)

	def _showWindow(self, *args):
		"""
		Shows the floater window.
		:param args: Nothing
		:return:
		"""
		self.floaterWindow.main_window.show_all()

	def _hideWindow(self, *args):
		"""
		Hides the floater window.
		:param args: Nothing
		:return:
		"""
		self.floaterWindow.main_window.hide()

	def toggleWindow(self, *args):
		"""
		Toggles the floater window.
		:param args: Nothing
		:return:
		"""
		if self.floaterWindow.main_window.is_visible():
			self._hideWindow()
		else:
			self._showWindow()

	def _setMenus(self):
		"""
		Sets the menus of the indicator
		:return:
		"""
		menu = Gtk.Menu()

		menu_items = Gtk.MenuItem("Toggle Floater")
		menu.append(menu_items)
		menu_items.connect("activate", self.toggleWindow)
		# Activate this menu entry when indicator is MMB-clicked
		self.ind.set_secondary_activate_target(menu_items)

		menu_items = Gtk.MenuItem("Exit")
		menu.append(menu_items)
		menu_items.connect("activate", self.on_quit)

		self.ind.set_menu(menu)
		menu.show_all()

	def on_quit(self, *args):
		"""
		Called when 'Exit' is pressed
		:param args: Nothing
		:return:
		"""
		Gtk.main_quit()
