from tkinter import Frame, Label, Menu
from tkinter import ttk

from microredes_gui.ui import test_window

class Tabs():
	def __init__(self, root):
		self.root = root

	def create_menu(self):
		menubar = Menu(self.root)
		self.root.config(menu=menubar)
		menuFunciones = Menu(menubar, tearoff=0)
		menuSalir = Menu(menubar, tearoff=0)

		menuFunciones.add_command(label="Conectarse")
		menuFunciones.add_command(label="Cambiar dirección")
		menuSalir.add_command(label="Salir")

		menubar.add_cascade(label="Funciones", menu=menuFunciones)
		menubar.add_cascade(label="Salir", menu=menuSalir)

	def create_tabs(self):
		tabs = ttk.Notebook(self.root)
		tabs.pack()

		frame1 = Frame(tabs, width=800, height=600)
		frame2 = Frame(tabs, width=800, height=600)

		frame1.pack(fill="both", expand=1)
		frame2.pack(fill="both", expand=1)

		tabs.add(frame1, text="Tab1")
		tabs.add(frame2, text="Tab2")

	def create_footer(self):
		status = Label(self.root, text="v1.0.0", bd="1")
		status.pack()