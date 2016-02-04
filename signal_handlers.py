#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from window_handler import YesNoDialog


class SignalHandlers(object):
	"""This class contains functions that are invoked when signals are emitted by widgets"""
	def __init__(self, floater):
		"""
		:param floater: the instance of the main app class. The main class may simply pass `self` here.
		:return: None
		"""
		super(SignalHandlers, self).__init__()
		self.floater = floater

	def tabReorder(self, widget, tab, new_index):
		"""
		Invoked when a tab is dragged to another position. It updates the `self.pages` and saves to file.
		:param widget:
		:param tab: The main widget of the moved page.
		:param new_index: the new position of the dragged page
		:return: None
		"""
		for n, i in enumerate(self.floater.pages):
			# Try to find the page by its child widget.
			# We're looking for the OLD page number, page_num won't return it after movement
			if self.floater.pages[n]['page_widget'] == tab:
				# Remove the page entry from pages
				page = self.floater.pages.pop(n)
				# Put it to new position
				self.floater.pages.insert(new_index, page)
				# Save the new order to file
				self.floater.file_saver.saveSymbols()
				break

	def tabClose(self, widget, page_widget):
		"""
		Invoked when the tab is being deleted on X button press. Removes the tab and the page from `self.pages`
		:param page_widget: the main child widget of the notebook page. Needed to get the page number.
		:param widget:
		:return: None
		"""
		# Get the page number
		page_number = self.floater.main_window_nb.page_num(page_widget)

		# Invoked when Yes is pressed
		def close_tab():
			# Delete the page
			self.floater.main_window_nb.remove_page(page_number)
			# Remove the page entry from pages
			self.floater.pages.pop(page_number)
			# Save the new order to file
			self.floater.file_saver.saveSymbols()

		dialog = YesNoDialog(parent=self.floater.main_window, dialog_title="Delete?",
				dialog_text="Are you sure you want to delete {0}?".format(self.floater.pages[page_number]['page_name']),
							yes_func=close_tab
							)
