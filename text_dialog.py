#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from window_handler import WindowHandler


class TextDialog(WindowHandler):
	"""docstring for TextDialog"""
	def __init__(self, ok_func, parent_window, title="Untitled Dialog", args=None, kwargs=None):
		super(TextDialog, self).__init__(title=title, type="dialog")

		self._initializeWindow(ok_func, parent_window, args, kwargs)

	def _initializeWindow(self, ok_func, parent_window, args, kwargs):
		self.set_transient_for(parent_window)
		main_box = self.addBox(parent=self, orientation="vertical")
		textview = self.addEntry(parent=main_box)
		buttons_row = self.addBox(parent=main_box, orientation="horizontal")
		ok_button = self.addButton(ok_func, label="OK", parent=buttons_row, args=(lambda: textview.get_text(),))
		cancel_button = self.addButton(lambda widget: self.close(), label="Cancel", parent=buttons_row)
		self.show_all()