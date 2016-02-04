#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gdk
from clipboard_handler import ClipboardHandler
from file_saver import FileSaver
from signal_handlers import SignalHandlers
from text_dialog import TextDialog
from window_handler import WindowHandler as Win, ErrorMessageDialog


class SymbolsFloater(object):
	"""docstring for SymbolsFloater"""
	def __init__(self):
		super(SymbolsFloater, self).__init__()
		self.pages = []

		self.signal_handlers = SignalHandlers(self)
		self.file_saver = FileSaver(self.pages)

		self.initializeWindow()
		self.initializeClipboard()

		self.file_saver.loadSymbolsFile()
		self.restorePages()

		self.main_window.run()

	def initializeClipboard(self):
		self.clipboard = ClipboardHandler()

	def restorePages(self):
		print(self.pages)#debug
		for n, page in enumerate(self.pages):
			self.addPage(page['page_name'], mode= "restore", page_index=n)
			for sym in page['symbols']:
				self.addSymbolButton(sym, mode="restore")

	def initializeWindow(self):
		self.main_window = Win(topmost=True, resizable=False, title="Symbols Floater",
							   initial_position="center", focusable=False)
		# self.main_window.resize(300, 150)
		main_box = self.main_window.addBox(parent=self.main_window, orientation="vertical")
		button_row = self.main_window.addBox(parent=main_box, orientation="horizontal")
		self.main_window.addButton(self.openAddPageDialog, label="Add Page", parent=button_row)
		self.main_window.addButton(self.openAddSymbolDialog, label="Add Symbols", parent=button_row)
		self.main_window_nb = self.main_window.addNotebook(parent=main_box)
		self.main_window_nb.connect("page_reordered", self.signal_handlers.tabReorder)

	def getCurrentPage(self):
		return self.main_window_nb.get_current_page()

	def openAddSymbolDialog(self, widget):
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
		def ok_button_handle(widget, get_text_func):
			text = get_text_func()
			if text:
				self.addPage(text)
				self.file_saver.saveSymbols()

		dialog_window = TextDialog(ok_func=ok_button_handle, parent_window=self.main_window,
								title="Enter name for the new page")

	def renamePage(self, page_num, new_name):
		self.pages[page_num]['page_name'] = new_name
		self.pages[page_num]['label_widget'].set_text(new_name)

	def openRenameDialog(self, widget, page_widget):
		def ok_button_handle(widget, get_text_func):
			text = get_text_func()
			if text:
				print(page_widget)
				self.renamePage(page_num=self.main_window_nb.page_num(page_widget), new_name=text)
				self.file_saver.saveSymbols()

		dialog_window = TextDialog(ok_func=ok_button_handle, parent_window=self.main_window,
								title="Enter new name for this page")

	def addPage(self, page_label, mode=None, page_index=None):
		#Remove @@ from page name, because it's in save file syntax
		page_label = page_label.replace("@@", "")

		page_grid = self.main_window.addBox(orientation="horizontal", spacing=3)
		page_widget, label_widget = self.main_window.addNotebookPage(notebook=self.main_window_nb, page_widget=page_grid,
										label_title=page_label, has_close_button=True,
										close_func=self.signal_handlers.tabClose,
										 tab_double_click_func=self.openRenameDialog,
										tab_double_click_func_args=(page_grid,)
										 )

		# Makes a tab draggable, so you could change order of tabs.
		self.main_window_nb.set_tab_reorderable(page_grid, True)

		if not mode:
			self.pages += [dict(page_name=page_label, symbols=list(), page_widget=page_grid, label_widget=label_widget)]
		elif mode == "restore":
			self.pages[page_index]["page_widget"] = page_grid
			self.pages[page_index]["label_widget"] = label_widget

		# Show all elements. It's kinda refreshing.
		self.main_window_nb.show_all()

		# Go to the newly created page. -1 means the last page, it is created in the end anyway
		# Had to put it after show_all() because it won't switch to a page with invisible child widgets
		self.main_window_nb.set_current_page(-1)

	def addSymbolButton(self, symbol, mode=None):
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
		self.clipboard.copy_text(text=symbol)

	def HelloWorld(self, *args):
		print("Hello, World!")
		print("args:", args)


def main():
	floater = SymbolsFloater()

if __name__ == '__main__':
	main()
