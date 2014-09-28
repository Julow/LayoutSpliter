import sublime, sublime_plugin

class Case():

	left = 0
	top = 0
	right = 0
	bottom = 0

	def __init__(self, left, top, right, bottom):
		self.left = left
		self.top = top
		self.right = right
		self.bottom = bottom

	def split_vertical(self):
		middle = round((self.right - self.left) / 2 + self.left, 2)
		case = Case(middle, self.top, self.right, self.bottom)
		self.right = middle
		return case

	def split_horizontal(self):
		middle = round((self.bottom - self.top) / 2 + self.top, 2)
		case = Case(self.left, middle, self.right, self.bottom)
		self.bottom = middle
		return case

	def merge(self, cases):
		for c in cases:
			if c.right == self.right and c.left == self.left and ((c.top == self.bottom) or (c.bottom == self.top)):
				self.top = min(c.top, self.top)
				self.bottom = max(c.bottom, self.bottom)
			elif c.top == self.top and c.bottom == self.bottom and ((c.right == self.left) or (c.left == self.right)):
				self.left = min(c.left, self.left)
				self.right = max(c.right, self.right)
			else:
				continue
			c.left = 0
			c.top = 0
			c.right = 0
			c.bottom = 0
			cases.remove(c)
			return

class JulooLayoutSpliterCommand(sublime_plugin.WindowCommand):

	def cases_to_layout(self, cases):
		cols = []
		rows = []
		for c in cases:
			if not c.right in cols:
				cols.append(c.right)
			if not c.left in cols:
				cols.append(c.left)
			if not c.top in rows:
				rows.append(c.top)
			if not c.bottom in rows:
				rows.append(c.bottom)
		cols.sort()
		rows.sort()
		cells = []
		for c in cases:
			cells.append([cols.index(c.left), rows.index(c.top), cols.index(c.right), rows.index(c.bottom)]);
		return {"cols": cols, "rows": rows, "cells": cells};

	def layout_to_cases(self, layout):
		cases = []
		cols = layout["cols"]
		rows = layout["rows"]
		cells = layout["cells"]
		for c in cells:
			cases.append(Case(cols[c[0]], rows[c[1]], cols[c[2]], rows[c[3]]))
		return cases

	def run(self, **args):
		cases = self.layout_to_cases(self.window.get_layout())
		curr_case = cases[self.window.active_group()]
		if args["action"] == "split":
			if args["direction"] == "vertical":
				cases.append(curr_case.split_vertical())
			elif args["direction"] == "horizontal":
				cases.append(curr_case.split_horizontal())
		elif args["action"] == "merge":
			curr_case.merge(cases)
		elif args["action"] == "reset":
			cases = [Case(0, 0, 1, 1)]
		self.window.run_command("set_layout", self.cases_to_layout(cases))
