from tkinter import BOTH, LEFT, RIGHT, X, Frame, Label, Menu, StringVar

from microredes_gui.ui import test_window, dialog_connect
from microredes_gui.core import comm as serial

class Main_Window():
	t = None

	def __init__(self, root):
		self.root = root
		self.comm = serial.Serial()

		self.connection_status = StringVar()

		self.frame_container = self.create_frame_container()

	def create_menu(self):
		self.menubar = Menu(self.root)
		self.root.config(menu=self.menubar)
		self.menu_funciones = Menu(self.menubar, tearoff=0)
		self.menu_pantallas = Menu(self.menubar, tearoff=0)
		self.menu_salir = Menu(self.menubar, tearoff=0)

		self.menu_funciones.add_command(label="Conectarse", command=self.connect_dialog)
		self.menu_funciones.add_command(label="Desconectarse", command=self.disconnect)

		self.menu_pantallas.add_command(label="Testing", command=self.create_test_window)

		self.menu_salir.add_command(label="Salir", command=self.root.destroy)

		self.menubar.add_cascade(label="Funciones", menu=self.menu_funciones)
		self.menubar.add_cascade(label="Pantallas", menu=self.menu_pantallas)
		self.menubar.add_cascade(label="Salir", menu=self.menu_salir)

	def destroy(self):
		self.t.destroy()

	def create_frame_container(self):
		frame = Frame(self.root)
		frame.pack(fill=BOTH, expand=True)
		return frame

	def create_test_window(self):
		self.t = test_window.Test_Window(self.frame_container, self.comm)
		self.t.draw_test_window()

	def connect_dialog(self):
		dlg = dialog_connect.Dialog_Connect(self.root, self, self.comm)
		dlg.show_dialog()
		self.set_connection_status()

	def disconnect(self):
		if self.comm.is_connected():
			self.comm.disconnect()
			self.set_connection_status()

	def create_footer(self):
		version = Label(self.root, text="v1.0.0", bd="1")
		version.pack(fill=X, side=LEFT, padx=10)
		status = Label(self.root, textvariable=self.connection_status, bd="1")
		status.bind("<Button-1>", self.connect_dialog)
		status.pack(fill=X, side=RIGHT, padx=10)

		self.set_connection_status()

	def set_connection_status(self):
		if self.comm.is_connected():
			self.connection_status.set("Conectado")
			self.menu_funciones.entryconfigure("Conectarse", state="disabled")
			self.menu_funciones.entryconfigure("Desconectarse", state="normal")
		else:
			self.connection_status.set("Desconectado")
			self.menu_funciones.entryconfigure("Conectarse", state="normal")
			self.menu_funciones.entryconfigure("Desconectarse", state="disabled")

		if self.t:
			self.t.refresh()
