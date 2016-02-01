#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk

class ClipboardHandler(object):
	"""docstring for ClipboardHandler"""
	def __init__(self):
		super(ClipboardHandler, self).__init__()
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

	def copy_text(self, text):
		# -1 means that length is determined automatically
		self.clipboard.set_text(text, -1)
