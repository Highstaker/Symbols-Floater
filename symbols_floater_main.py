#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import logging

from clipboard_handler import ClipboardHandler
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
		def ok_button_handle(widget):
			text = textview.get_text()
			if text:
				for sym in text:
					self.addSymbolButton(sym)

				dialog_window.close()
				self.saveSymbols()

		dialog_window = Win(type="dialog", title="Enter symbols to add", resizable=False, topmost=True)
		# Set main window as parent to dialogs. This causes them to be spawned right above the main window.
		dialog_window.set_transient_for(self.main_window)
		# self.addPage(widget, "test")
		grid = dialog_window.addGrid(parent=dialog_window)
		textview = dialog_window.addEntry()
		grid.attach(textview, 0, 0, 2, 1)
		ok_button = dialog_window.addButton(ok_button_handle, "OK")
		grid.attach(ok_button, 0, 1, 1, 2)
		cancel_button = dialog_window.addButton(lambda widget: dialog_window.close(), "Cancel")
		grid.attach(cancel_button, 1, 1, 1, 2)

		dialog_window.show_all()

	def openAddPageDialog(self, widget):
		def ok_button_handle(widget):
			text = textview.get_text()
			if text:
				self.addPage(text)
				dialog_window.close()
				self.saveSymbols()

		dialog_window = Win(type="dialog", title="Enter name for the new page", resizable=False, topmost=True)
		# Set main window as parent to dialogs. This causes them to be spawned right above the main window.
		dialog_window.set_transient_for(self.main_window)
		# self.addPage(widget, "test")
		grid = dialog_window.addGrid(parent=dialog_window)
		textview = dialog_window.addEntry()
		grid.attach(textview, 0, 0, 2, 1)
		ok_button = dialog_window.addButton(ok_button_handle, "OK")
		grid.attach(ok_button, 0, 1, 1, 2)
		cancel_button = dialog_window.addButton(lambda widget: dialog_window.close(), "Cancel")
		grid.attach(cancel_button, 1, 1, 1, 2)

		dialog_window.show_all()

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
