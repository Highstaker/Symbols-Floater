#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gtk


class YesNoDialog(Gtk.Dialog):
	"""Creates a simple Yes/No dialog"""
	def __init__(self, parent, dialog_title="Untitled Dialog", dialog_text="",
				yes_func=lambda: None, no_func=lambda: None):
		"""
		:param parent: A parent of this dialog
		:param dialog_title: Title of this dialog
		:param dialog_text: Text to be put into the dialog window
		:param yes_func: a function invoked when Yes is pressed
		:param no_func: a function invoked when No is pressed
		:return:
		"""
		Gtk.Dialog.__init__(self, dialog_title, None, 0,
			(Gtk.STOCK_NO, Gtk.ResponseType.NO,
			Gtk.STOCK_YES, Gtk.ResponseType.YES))

		self.yes_func = yes_func
		self.no_func = no_func

		self.set_default_size(150, 100)

		label = Gtk.Label(dialog_text)

		box = self.get_content_area()
		box.add(label)
		self.show_all()

		self.run_dialog()

	def run_dialog(self):
		response = self.run()

		if response == Gtk.ResponseType.YES:
			self.yes_func()
		elif response == Gtk.ResponseType.NO:
			self.no_func()

		self.destroy()

class ErrorMessageDialog(Gtk.MessageDialog):
	"""docstring for ErrorMessageDialog"""
	def __init__(self, message="", secondary_message="", title="Untitled Error Dialog", parent=None):
		super(ErrorMessageDialog, self).__init__(parent, 0, Gtk.MessageType.ERROR,
			Gtk.ButtonsType.OK, message)

		self.set_title(title)
		self.format_secondary_text(secondary_message)
		self.run_dialog()

	def run_dialog(self):
		self.run()
		self.destroy()

class WindowHandler(Gtk.Window):
	"""docstring for WindowHandler"""
	def __init__(self, title="Untitled", type="main", topmost=False, resizable=True, initial_position=None, focusable=True):
		super(WindowHandler, self).__init__(title=title)
		self._createWindow(type, topmost=topmost, resizable=resizable,
						initial_position=initial_position, focusable=focusable)

	def _createWindow(self, type, topmost=False, resizable=True, initial_position=None, focusable=True):
		if type == "main":
			self.connect("delete-event", Gtk.main_quit)
		elif type == "dialog":
			pass

		if initial_position == "center":
			self.set_position(Gtk.WindowPosition.CENTER)

		if topmost:
			self.set_keep_above(True)

		if resizable:
			self.set_resizable(True)
		else:
			self.set_resizable(False)

		if focusable:
			self.set_accept_focus(True)
		else:
			self.set_accept_focus(False)

	def addButton(self, action, label="", parent=None, args=None, kwargs=None, min_size=None):
		if not args:
			args = tuple()
		if not kwargs:
			kwargs = dict()

		button = Gtk.Button(label=label)
		if min_size:
			button.set_size_request(*min_size)
		button.connect("clicked", action, *args, **kwargs)
		if parent:
			parent.add(button)

		return button

	def addEntry(self, parent=None):
		entry = Gtk.Entry()
		if parent:
			parent.add(entry)

		return entry

	def addBox(self, parent=None, orientation="horizontal", spacing=0):
		if orientation == "vertical":
			orientation = Gtk.Orientation.VERTICAL
		else:
			orientation = Gtk.Orientation.HORIZONTAL

		box = Gtk.Box(orientation=orientation, spacing=spacing)
		if parent:
			parent.add(box)

		return box

	def addGrid(self, parent=None):
		grid = Gtk.Grid()
		if parent:
			parent.add(grid)

		return grid

	def addNotebook(self, parent=None):
		notebook = Gtk.Notebook()
		if parent:
			parent.add(notebook)

		return notebook

	def addNotebookPage(self, notebook, page_widget, label_title="", has_close_button=False, close_func=lambda: None):
		if not has_close_button:
			notebook.append_page(page_widget, Gtk.Label(label_title))
		else:
			# a box containing both the label and the close button
			tab_label_box = self.addBox(orientation="horizontal", spacing=5)
			label = Gtk.Label(label_title)
			tab_label_box.add(label)

			# get a stock close button image
			close_image = Gtk.Image()
			close_image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)

			# make the close button
			btn = Gtk.Button()
			btn.set_relief(Gtk.ReliefStyle.NONE)
			btn.set_focus_on_click(False)
			btn.set_image(close_image)

			# connect the function that will close the tab and pass the page widget to it.
			# This is needed to get the page index
			btn.connect("clicked", close_func, page_widget)

			tab_label_box.add(btn)

			# have to show it all before appending the page
			tab_label_box.show_all()

			notebook.append_page(page_widget, tab_label_box)

		return page_widget

	def run(self):
		self.show_all()
		Gtk.main()
