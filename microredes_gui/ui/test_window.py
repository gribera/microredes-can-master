from tkinter import StringVar
from tkinter import ttk

from microredes_gui.core import consts

class Test_Window():
	def __init__(self, frame):
		self.frame = frame

		c = consts.Consts()
		self.functions = c.get_functions()
		self.disp_origen = c.get_disp_origen()
		self.disp_destino = c.get_disp_destino()
		self.variables = c.get_variables()

		self.combos = [self.functions, self.disp_origen, self.disp_destino, self.variables]
		for x in range(6):
			self.combos.append(list(range(0,255)))

		self.comboLabel = ['Función', 'Origen', 'Destino', 'Variable']
		for x in range(6):
			self.comboLabel.append('Byte ' + str(x + 1))

		self.selected_option = {}

	def me_llaman(self, event):
		print(event)

	def draw_values(self, event):
		val = 0
		valores_int = [int(self.functions[self.selected_option[0].get()], 0),
		int(self.disp_origen[self.selected_option[1].get()], 0),
		int(self.disp_destino[self.selected_option[2].get()], 0),
		int(self.variables[self.selected_option[3].get()], 0),
		int(self.selected_option[4].get()),
		int(self.selected_option[5].get()),
		int(self.selected_option[6].get()),
		int(self.selected_option[7].get()),
		int(self.selected_option[8].get()),
		int(self.selected_option[9].get())]

		for row in range(3, 6):
			for col in range(0, 10):
				if row == 3:
					val = valores_int[col]
				if row == 4:
					val = bin(valores_int[col])[2:].zfill(8)
				if row == 5:
					val = hex(valores_int[col])

				label = ttk.Label(self.frame, text=val, font=("Fixedsys", 10))
				label.grid(row=row, column=col)

	def draw_selects(self):
		for idx in range(0, len(self.combos)):
			self.selected_option[idx] = StringVar()

			if isinstance(self.combos[idx], dict):
				valores = list(self.combos[idx].keys())
			else:
				valores = self.combos[idx]

			# Agrega etiqueta
			lb = ttk.Label(self.frame, text=self.comboLabel[idx])
			lb.grid(row=1, column=idx, padx=10, pady=10)
			# Agrega combo
			cmbFnc = ttk.Combobox(self.frame, values=valores, justify="center",
				textvariable=self.selected_option[idx], state="readonly", width=12)
			cmbFnc.bind("<<ComboboxSelected>>", self.draw_values)
			cmbFnc.grid(row=2, column=idx, padx=5, pady=10)
			cmbFnc.current(0)
