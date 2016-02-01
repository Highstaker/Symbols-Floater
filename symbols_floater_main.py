#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

from window_handler import WindowHandler as Win


class SymbolsFloater(object):
	"""docstring for SymbolsFloater"""
	def __init__(self):
		super(SymbolsFloater, self).__init__()
		self.pages = []
		self.initializeWindow()

		self.main_window.run()

	def initializeWindow(self):
		self.main_window = Win()
		self.main_window.resize(300, 150)
		box1 = self.main_window.addBox(parent=self.main_window, orientation="vertical")
		self.main_window.addButton(self.openAddPageDialog, label="Add Page", parent=box1)
		self.main_window_nb = self.main_window.addNotebook(parent=box1)

	def getCurrentPage(self):
		return self.main_window_nb.get_current_page()

	def openAddSymbolDialog(self, widget):
		def ok_button_handle(widget):
			text = textview.get_text()
			if text:
				for sym in text:
					self.addSymbolButton(sym)

				dialog_window.close()

		dialog_window = Win(type="dialog", title="Enter symbols to add")
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

		dialog_window = Win(type="dialog", title="Enter name for the new page")
		# self.addPage(widget, "test")
		grid = dialog_window.addGrid(parent=dialog_window)
		textview = dialog_window.addEntry()
		grid.attach(textview, 0, 0, 2, 1)
		ok_button = dialog_window.addButton(ok_button_handle, "OK")
		grid.attach(ok_button, 0, 1, 1, 2)
		cancel_button = dialog_window.addButton(lambda widget: dialog_window.close(), "Cancel")
		grid.attach(cancel_button, 1, 1, 1, 2)

		dialog_window.show_all()

	def addPage(self, page_label):
		page_grid = self.main_window.addGrid()
		self.pages += [(page_grid, [])]
		self.main_window.addNotebookPage(notebook=self.main_window_nb, page_widget=page_grid, label=page_label)

		# Show all elements. It's kinda refreshing.
		self.main_window_nb.show_all()

	def addSymbolButton(self, symbol):
		# get the grid widget on the current page
		page_grid = self.pages[self.getCurrentPage()][0]

		# Add a symbol to list of symbols for a page
		self.pages[self.getCurrentPage()][1].append(symbol)

		# Add the button
		self.main_window.addButton(self.HelloWorld, label=symbol, parent=page_grid)

	def HelloWorld(self, widget):
		print("Hello, World!")


def main():
	floater = SymbolsFloater()

if __name__ == '__main__':
	main()
