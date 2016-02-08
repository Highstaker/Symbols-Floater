#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gdk
from clipboard_handler import ClipboardHandler
from file_saver import FileSaver
from signal_handlers import SignalHandlers
from text_dialog import TextDialog
from window_handler import WindowHandler as Win, ErrorMessageDialog


class SymbolsFloater(object):
	"""The class for main Floater window"""
	def __init__(self):
		super(SymbolsFloater, self).__init__()
		# The list containing info on pages and symbols
		self.pages = []

		self.signal_handlers = SignalHandlers(self)
		self.file_saver = FileSaver(self.pages)

		self.initializeWindow()
		self.initializeClipboard()

		self.file_saver.loadSymbolsFile()
		self.restorePages()

	def initializeClipboard(self):
		"""
		Initializes the ClipboardHandler class to handle clipboard manipulations.
		:return:
		"""
		self.clipboard = ClipboardHandler()

	def restorePages(self):
		"""
		Restores the pages in the window according to the `pages` list
		:return:
		"""
		for n, page in enumerate(self.pages):
			self.addPage(page['page_name'], mode= "restore", page_index=n)
			for sym in page['symbols']:
				self.addSymbolButton(sym, mode="restore")

	def initializeWindow(self):
		"""
		Initialization of window layout and connection of signals.
		:return:
		"""
		self.main_window = Win(topmost=True, resizable=False, title="Symbols Floater",
							   initial_position="center", focusable=False, suppress_X=True)
		# self.main_window.resize(300, 150)
		main_box = self.main_window.addBox(parent=self.main_window, orientation="vertical")
		button_row = self.main_window.addBox(parent=main_box, orientation="horizontal")
		self.main_window.addButton(lambda *args: self.main_window.hide(), label="X", parent=button_row)
		self.main_window.addButton(self.openAddPageDialog, label="Add Page", parent=button_row)
		self.main_window.addButton(self.openAddSymbolDialog, label="Add Symbols", parent=button_row)
		self.main_window_nb = self.main_window.addNotebook(parent=main_box)
		self.main_window_nb.connect("page_reordered", self.signal_handlers.tabReorder)

	def getCurrentPage(self):
		"""

		:return: The current page number
		"""
		return self.main_window_nb.get_current_page()

	def openAddSymbolDialog(self, widget):
		"""
		Opens the dialog for adding symbols.
		:param widget:
		:return:
		"""
		def ok_button_handle(widget, get_text_func):
			text = get_text_func()
			if text:
				for sym in text:
					self.addSymbolButton(sym)
				self.file_saver.saveSymbols()

		if self.main_window_nb.get_n_pages():
			dialog_window = TextDialog(ok_func=ok_button_handle, parent_window=self.main_window,
								title="Enter symbols to add")
		else:
			error_message = "Cannot create symbols without any pages!"
			small_message = "Please, create a page first!"
			dialog_window = ErrorMessageDialog(dialog_text=error_message, dialog_text_secondary=small_message,
											   dialog_title="Error!", parent=self.main_window)

	def openAddPageDialog(self, widget):
		"""
		Opens the dialog for adding pages.
		:param widget:
		:return:
		"""
		def ok_button_handle(widget, get_text_func):
			text = get_text_func()
			if text:
				self.addPage(text)
				self.file_saver.saveSymbols()

		dialog_window = TextDialog(ok_func=ok_button_handle, parent_window=self.main_window,
								title="Enter name for the new page")

	def openRenameDialog(self, widget, page_widget):
		"""
		Opens the dialog for page renaming
		:param widget:
		:param page_widget: the main widget of the page
		:return:
		"""
		def ok_button_handle(widget, get_text_func):
			text = get_text_func()
			if text:
				print(page_widget)
				self.renamePage(page_num=self.main_window_nb.page_num(page_widget), new_name=text)
				self.file_saver.saveSymbols()

		dialog_window = TextDialog(ok_func=ok_button_handle, parent_window=self.main_window,
								title="Enter new name for this page")

	def renamePage(self, page_num, new_name):
		"""
		Renames the dialog.
		:param page_num: Index of the page to rename
		:param new_name: A new name for the page
		:return:
		"""
		# Set it in the pages list
		self.pages[page_num]['page_name'] = new_name
		# Set the actual page label
		self.pages[page_num]['label_widget'].set_text(new_name)

	def addPage(self, page_label, mode=None, page_index=None):
		"""
		Add a page
		:param page_label: A text written in the label of the new page
		:param mode: if None, it simply adds a new page at the last position and updates the `pages` list.
		If 'restore', it doesn't create new entry in `pages`, only appends GTK-specific stuff there.
		This should be used when the page name and symbols are already present in the `pages` list, e.g. loaded from file.
		:param page_index: Used with `mode` set to 'restore', shows which page should be added to notebook.
		:return:
		"""
		# Remove @@ from page name, because it's in save file syntax
		page_label = page_label.replace("@@", "")

		page_grid = self.main_window.addBox(orientation="horizontal", spacing=3)
		page_widget, label_widget = self.main_window.addNotebookPage(notebook=self.main_window_nb,
																	page_widget=page_grid,
																	label_title=page_label, has_close_button=True,
																	close_func=self.signal_handlers.tabClose,
																	tab_double_click_func=self.openRenameDialog,
																	tab_double_click_func_args=(page_grid,)
																	)

		# Makes a tab draggable, so you could change order of tabs.
		self.main_window_nb.set_tab_reorderable(page_grid, True)

		if not mode:
			# Initialize a new page in `pages` list
			self.pages += [dict(page_name=page_label, symbols=list(), page_widget=page_grid, label_widget=label_widget)]
		elif mode == "restore":
			# Name and symbols already exist in `pages`. Add GTK specific stuff to a page with index `page_index`
			self.pages[page_index]["page_widget"] = page_grid
			self.pages[page_index]["label_widget"] = label_widget

		# Show all elements. It's kinda refreshing.
		self.main_window_nb.show_all()

		# Go to the newly created page. -1 means the last page, it is created in the end anyway
		# Had to put it after show_all() because it won't switch to a page with invisible child widgets
		self.main_window_nb.set_current_page(-1)

	def addSymbolButton(self, symbol, mode=None):
		"""
		Adds a symbol to a page.
		:param symbol: a symbol to add
		:param mode: If "restore", it doesn't add the symbol to `pages` list, only creates the button.
		This should be used when the symbols are already present in the `pages` list, e.g. loaded from file.
		:return:
		"""
		# get the grid widget on the current page
		page_grid = self.main_window_nb.get_nth_page(self.getCurrentPage())

		if not mode == "restore":
			# Add a symbol to list of symbols for a page
			self.pages[self.getCurrentPage()]['symbols'].append(symbol)

		# Add the button
		button = self.main_window.addButton(self.copySymbolToClipboard, label=symbol,
								parent=page_grid, args=(symbol,), min_size=(40, 40))
		# Make the button draggable with LMB, and thus - movable.
		button.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.MOVE)

		# Show all elements. It's kinda refreshing.
		self.main_window_nb.show_all()

	def copySymbolToClipboard(self, widget, symbol):
		"""
		Copies a given string to clipboard
		:param widget:
		:param symbol: string to copy
		:return:
		"""
		self.clipboard.copy_text(text=symbol)

	def HelloWorld(self, *args):
		print("Hello, World!")
		print("args:", args)

#
# def main():
# 	floater = SymbolsFloater()
#
# if __name__ == '__main__':
# 	main()
