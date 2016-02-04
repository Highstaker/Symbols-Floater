#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk


class ClipboardHandler(object):
	"""Class that handles clipboard manipulations"""
	def __init__(self):
		super(ClipboardHandler, self).__init__()
		# Get the Ctrl+C/Ctrl+V clipboard
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

	def copy_text(self, text):
		"""
		Puts the text to clipboard
		:param text: Text to put to clipboard
		:return: None
		"""
		# -1 means that length is determined automatically
		self.clipboard.set_text(text, -1)
