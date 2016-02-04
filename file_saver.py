#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import logging

SAVE_FILENAME = "symbols.save"


class FileSaver(object):
	"""A class that handles saving of the symbols to file."""

	def __init__(self, pages):
		"""
		:param pages: the `self.pages` from the main class. It should be a list of dictionaries.
		A dict. should contain "page_name", which is the label of a page (a string),
		and "symbols", which is a list of stmbols on that page.
		:return: None
		"""
		super(FileSaver, self).__init__()
		self.pages = pages

	def saveSymbols(self):
		"""
		Saves the pages and symbols to a text file.
		:return: None
		"""
		with open(SAVE_FILENAME, "w") as f:
			for page in self.pages:
				f.write(page["page_name"] + "@@" + "".join(page['symbols']) + "\n")

	def loadSymbolsFile(self):
		"""
		Loads the pages and symbols from a file
		and passes the page name and symbols list to `self.pages` of the main class.
		:return:
		"""
		try:
			with open(SAVE_FILENAME, 'r') as f:
				parse = f.readlines()
				for page in parse:
					page_name, symbols = page.split(sep="@@", maxsplit=1)
					self.pages += [dict(page_name=page_name, symbols=list(symbols.replace("\n", "")))]
				logging.warning(("self.pages", self.pages))
		except FileNotFoundError:
			# There is no restore file. Start with empty window
			logging.warning("Restore file not found!")
