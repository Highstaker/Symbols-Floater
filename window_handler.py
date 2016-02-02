#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from gi.repository import Gtk


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

	def addNotebookPage(self, notebook, page_widget, label=""):
		notebook.append_page(page_widget, Gtk.Label(label))
		return page_widget

	def run(self):
		self.show_all()
		Gtk.main()
