#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from window_handler import WindowHandler


class TextDialog(WindowHandler):
	"""Creates a window consisting only of a text view and OK/Cancel buttons."""
	def __init__(self, ok_func, parent_window=None, title="Untitled Dialog"):
		"""

		:param ok_func: a function to be invoked on OK button press
		:param parent_window: A parent of this dialog
		:param title: Title of dialog window
		:return:
		"""
		super(TextDialog, self).__init__(title=title, type="dialog")

		# Set parent
		self.set_transient_for(parent_window)
		# Create main layout widget
		main_box = self.addBox(parent=self, orientation="vertical")
		# Create the text entry box
		textview = self.addEntry(parent=main_box)
		# Row of buttons
		buttons_row = self.addBox(parent=main_box, orientation="horizontal")
		# Initialize buttons
		ok_button = self.addButton(ok_func, label="OK", parent=buttons_row, args=(lambda: textview.get_text(),))
		cancel_button = self.addButton(lambda widget: self.close(), label="Cancel", parent=buttons_row)


		# Set signals to close the dialog when OK or Cancel is pressed
		# Nothing should happen if OK is pressed and there is nothing in text input.
		def ok_destructor():
			if textview.get_text():
				self.close()
		ok_button.connect("clicked", lambda *args: ok_destructor())
		cancel_button.connect("clicked", lambda *args: self.close())

		#Show everything
		self.show_all()
