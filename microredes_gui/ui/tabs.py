from tkinter import Frame, Label, Menu
from tkinter import ttk

from microredes_gui.ui import test_window

class Tabs():
	def __init__(self, root):
		self.root = root
		self.tab_container = self.create_tab_container()
		tst1 = self.create_tab('Testing 1')
		tst2 = self.create_tab('Testing 2')

		t = test_window.Test_Window(tst1)
		t.draw_selects()
		t.draw_values(0)
		t.draw_terminal()
		t.draw_buttons()

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

	def create_tab_container(self):
		tab = ttk.Notebook(self.root)
		tab.pack()
		return tab

	def create_tab(self, title):
		frame = Frame(self.tab_container, width=800, height=550)
		frame.pack(fill="both", expand=1)
		self.tab_container.add(frame, text=title)
		return frame

	def create_footer(self):
		status = Label(self.root, text="v1.0.0", bd="1")
		status.pack()