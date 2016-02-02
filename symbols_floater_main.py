#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import logging

from clipboard_handler import ClipboardHandler
from text_dialog import TextDialog
from window_handler import WindowHandler as Win
import pickle

SAVE_FILENAME = "symbols.save"

class SymbolsFloater(object):
	"""docstring for SymbolsFloater"""
	def __init__(self):
		super(SymbolsFloater, self).__init__()
		self.pages = []
		self.initializeWindow()
		self.initializeClipboard()
		self.loadSymbolsFile()
		self.main_window.run()

	def initializeClipboard(self):
		self.clipboard = ClipboardHandler()

	def saveSymbols(self):
		with open(SAVE_FILENAME, "wb") as f:
			pickle.dump(self.pages, f, pickle.HIGHEST_PROTOCOL)

	def loadSymbolsFile(self):
		try:
			with open(SAVE_FILENAME,'rb') as f:
				self.pages = pickle.load(f)
				logging.warning(("self.pages", self.pages))
				self.restorePages()
		except FileNotFoundError:
			logging.warning("Restore file not found!")

	def restorePages(self):
		for page in self.pages:
			self.addPage(page['page_name'], mode= "restore")
			for sym in page['symbols']:
				self.addSymbolButton(sym, mode="restore")

	def initializeWindow(self):
		self.main_window = Win(topmost=True, resizable=False, title="Symbols Floater" , initial_position="center")
		# self.main_window.resize(300, 150)
		main_box = self.main_window.addBox(parent=self.main_window, orientation="vertical")
		button_row = self.main_window.addBox(parent=main_box, orientation="horizontal")
		self.main_window.addButton(self.openAddPageDialog, label="Add Page", parent=button_row)
		self.main_window.addButton(self.openAddSymbolDialog, label="Add Symbols", parent=button_row)
		self.main_window_nb = self.main_window.addNotebook(parent=main_box)

	def getCurrentPage(self):
		return self.main_window_nb.get_current_page()

	def openAddSymbolDialog(self, widget):
		def ok_button_handle(widget, get_text_func):
			text = get_text_func()
			if text:
				for sym in text:
					self.addSymbolButton(sym)

				dialog_window.close()
				self.saveSymbols()

		dialog_window = TextDialog(ok_func=ok_button_handle, parent_window=self.main_window,
								title="Enter symbols to add")

	def openAddPageDialog(self, widget):
		def ok_button_handle(widget, get_text_func):
			text = get_text_func()
			if text:
				self.addPage(text)
				dialog_window.close()
				self.saveSymbols()

		dialog_window = TextDialog(ok_func=ok_button_handle, parent_window=self.main_window,
								title="Enter name for the new page")

	def addPage(self, page_label, mode=None):
		page_grid = self.main_window.addBox(orientation="horizontal", spacing=3)
		self.main_window.addNotebookPage(notebook=self.main_window_nb, page_widget=page_grid, label=page_label)

		if not mode == "restore":
			self.pages += [dict(page_name=page_label, symbols=list())]

		# Show all elements. It's kinda refreshing.
		self.main_window_nb.show_all()

	def addSymbolButton(self, symbol, mode=None):
		# get the grid widget on the current page
		page_grid = self.main_window_nb.get_nth_page(self.getCurrentPage())

		if not mode == "restore":
			# Add a symbol to list of symbols for a page
			self.pages[self.getCurrentPage()]['symbols'].append(symbol)

		# Add the button
		self.main_window.addButton(self.copySymbolToClipboard, label=symbol,
								parent=page_grid, args=(symbol,), min_size=(40, 40))

		# Show all elements. It's kinda refreshing.
		self.main_window_nb.show_all()

	def copySymbolToClipboard(self, widget, symbol):
		self.clipboard.copy_text(text=symbol)

	def HelloWorld(self, widget):
		print("Hello, World!")


def main():
	floater = SymbolsFloater()

if __name__ == '__main__':
	main()
