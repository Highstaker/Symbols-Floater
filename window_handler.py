#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk


class YesNoDialog(Gtk.MessageDialog):
	"""Creates a simple Yes/No dialog"""
	def __init__(self, parent=None, dialog_title="Untitled Dialog", dialog_text="",
				yes_func=lambda: None, no_func=lambda: None):
		"""
		:param parent: A parent window of this dialog
		:param dialog_title: Title of this dialog
		:param dialog_text: Text to be put into the dialog window
		:param yes_func: a function invoked when Yes is pressed
		:param no_func: a function invoked when No is pressed
		:return:
		"""
		super(YesNoDialog, self).__init__(parent, 0, Gtk.MessageType.QUESTION,
		Gtk.ButtonsType.YES_NO, dialog_text)

		self.set_title(dialog_title)

		self.yes_func = yes_func
		self.no_func = no_func

		self.run_dialog()

	def run_dialog(self):
		response = self.run()

		if response == Gtk.ResponseType.YES:
			self.yes_func()
		elif response == Gtk.ResponseType.NO:
			self.no_func()

		self.destroy()


class ErrorMessageDialog(Gtk.MessageDialog):
	"""Creates a simple error message dialog"""
	def __init__(self, dialog_text="", dialog_text_secondary="", dialog_title="Untitled Error Dialog", parent=None):
		"""

		:param dialog_text: Text to be put into the dialog window, in bold
		:param dialog_text_secondary: Smaller text to be put into the dialog window
		:param dialog_title: Title of this dialog
		:param parent: A parent window of this dialog
		:return:
		"""
		super(ErrorMessageDialog, self).__init__(parent, 0, Gtk.MessageType.ERROR,
			Gtk.ButtonsType.OK, dialog_text)

		self.set_title(dialog_title)
		self.format_secondary_text(dialog_text_secondary)
		self.run_dialog()

	def run_dialog(self):
		self.run()
		self.destroy()


class WindowHandler(Gtk.Window):
	"""A handler for GTK windows"""
	def __init__(self, title="Untitled", topmost=False, resizable=True,
				initial_position=None, focusable=True, suppress_X=False):
		"""

		:param title: The window title
		:param topmost: If True, the window will always be above other windows
		:param resizable: If true, window can be resized.
		:param initial_position: if None, window will be placed by default
		:param focusable: If False, window cannot be focused on
		:param suppress_X: If True, pressing the window's "X" button does nothing.
		If False, it deletes the window.
		:return:
		"""
		super(WindowHandler, self).__init__(title=title)

		if suppress_X:
			self.connect("delete-event", lambda *args: 1)

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
		"""
		Adds a button.
		:param action: a method to be invoked on button click
		:param label: text on the button
		:param parent: parent widget
		:param args: arguments for `action`
		:param kwargs: keyword arguments for `action`
		:param min_size: the tuple (width,height) showing the minimum size for the button.
		:return:
		"""
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
		"""
		Adds the entry field
		:param parent: parent widget
		:return:
		"""
		entry = Gtk.Entry()
		if parent:
			parent.add(entry)

		return entry

	def addBox(self, parent=None, orientation="horizontal", spacing=0):
		"""
		Adds a box container
		:param parent: parent widget
		:param orientation: If "vertical", widgets will be arranged from top to bottom.
		Else, from left to right.
		:param spacing: distance between adjacent widgets
		:return:
		"""
		if orientation == "vertical":
			orientation = Gtk.Orientation.VERTICAL
		else:
			orientation = Gtk.Orientation.HORIZONTAL

		box = Gtk.Box(orientation=orientation, spacing=spacing)
		if parent:
			parent.add(box)

		return box

	def addGrid(self, parent=None):
		"""
		Adds a grid container
		:param parent: parent widget
		:return:
		"""
		grid = Gtk.Grid()
		if parent:
			parent.add(grid)

		return grid

	def addNotebook(self, parent=None):
		"""
		Adds a notebook container
		:param parent: parent widget
		:return:
		"""
		notebook = Gtk.Notebook()
		if parent:
			parent.add(notebook)

		return notebook

	def addNotebookPage(self, notebook, page_widget, label_title="",
						has_close_button=False, close_func=lambda: None,
						tab_double_click_func=lambda *args: None,
						tab_double_click_func_args=tuple()
						):
		"""
		Adds a notebook page
		:param notebook: the notebook container to add the page to.
		:param page_widget: the main widget of the page
		:param label_title:
		:param has_close_button: if True, adds an "X" button to page's tab
		:param close_func: A function to invoke on pressing "X"
		:param tab_double_click_func: A function to invoke on double-click on the tab
		:param tab_double_click_func_args: arguments for `tab_double_click_func`
		:return:
		"""
		def handleLabelDoubleClick(widget, event):
			if event.button == Gdk.BUTTON_PRIMARY:
				if event.type == Gdk.EventType._2BUTTON_PRESS:
					tab_double_click_func(widget, *tab_double_click_func_args)

		# a box containing both the label and the close button
		tab_label_box = self.addBox(orientation="horizontal", spacing=5)

		e = Gtk.EventBox()
		label = Gtk.Label(label_title)
		e.add(label)
		e.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		e.connect("button-press-event", handleLabelDoubleClick)

		tab_label_box.add(e)

		if has_close_button:
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

		return page_widget, label

	def run(self):
		"""
		Runs the main routine. Don't call it if it is already invoked by the program.
		:return:
		"""
		self.show_all()
		Gtk.main()
