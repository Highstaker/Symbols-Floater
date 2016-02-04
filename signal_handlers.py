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
		print("Tabs reordered", tab, new_index)
		print(self.floater.main_window_nb.get_current_page())
		for n, i in enumerate(self.floater.pages):
			print(n, self.floater.pages[n]['page_widget'])
			if self.floater.pages[n]['page_widget'] == tab:
				print("Popping the page")#debug
				page = self.floater.pages.pop(n)
				self.floater.pages.insert(new_index, page)
				print(self.floater.pages)#debug
				self.floater.file_saver.saveSymbols()
				break

	def tabClose(self, widget, page_widget):
		"""
		Invoked when the tab is being deleted on X button press. Removes the tab and the page from `self.pages`
		:param widget:
		:return: None
		"""
		page_number = self.floater.main_window_nb.page_num(page_widget)

		def close_tab():
			print("The Yes button was clicked")#debug
			print(widget)#debug
			print("page_number", page_number)#debug
			self.floater.main_window_nb.remove_page(page_number)
			self.floater.pages.pop(page_number)
			self.floater.file_saver.saveSymbols()

		dialog = YesNoDialog(parent=self.floater, dialog_title="Delete?",
				dialog_text="Are you sure you want to delete {0}?".format(self.floater.pages[page_number]['page_name']),
							yes_func=close_tab
							)
