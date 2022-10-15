from tkinter import ttk

class Test_Window():
	def __init__(self, frame):
		self.frame = frame

	def draw_values(self):
		val = ''
		for row in range(0, 3):
			for col in range(0, 10):
				if row == 0:
					val = '0'
				if row == 1:
					val = '1'
				if row == 2:
					val = '3'

				label = ttk.Label(self.frame, text=val, font=("Fixedsys", 10))
				label.grid(row=row, column=col)

	def draw_selects(self):
		pass