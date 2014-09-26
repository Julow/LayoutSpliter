import sublime, sublime_plugin, time

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

	def split_orizontal(self):
		middle = round((self.bottom - self.top) / 2 + self.top, 2)
		case = Case(self.left, middle, self.right, self.bottom)
		self.bottom = middle
		return case

	def __repr__(self):
		return str(self.left) +" "+ str(self.top) +" "+ str(self.right) +" "+ str(self.bottom)

class JulooSublimeLayoutCommand(sublime_plugin.WindowCommand):

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
				cases.append(curr_case.split_orizontal())
		elif args["action"] == "reset":
			cases = [Case(0, 0, 1, 1)]
		self.window.run_command("set_layout", self.cases_to_layout(cases))
