import threading
from tkinter import StringVar, NO, CENTER, END, RIGHT, LEFT
from tkinter import ttk
from datetime import datetime

from microredes_gui.core import consts
from microredes_gui.core import comm as serial

class Test_Window():
	valores_int = []

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

		self.thread2 = threading.Thread(name="read", target=self.readQueue)

		# Se crea el objeto para la comunicación serial
		self.comm = serial.Serial(self.thread2)
		self.comm.connect('/dev/ttyACM0', '115200', '250000')

	def draw_values(self, event):
		val = 0
		self.valores_int = [int(self.functions[self.selected_option[0].get()], 0),
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
					val = self.valores_int[col]
				if row == 4:
					val = bin(self.valores_int[col])[2:].zfill(8)
				if row == 5:
					val = hex(self.valores_int[col])

				label = ttk.Label(self.frame, text=val, font=("Fixedsys", 10))
				label.grid(row=row, column=col)

		container = ttk.Frame(self.frame)
		container.grid(row=6, columnspan=11, pady=20)


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

	def draw_terminal(self):
		container = ttk.Frame(self.frame)
		container.grid(row=7, column=0, columnspan=8, padx=10, pady=10)

		self.lista = ttk.Treeview(container, selectmode='browse',
						columns=("#0","#1", "#2", "#3"), height=15)
		self.lista.pack(side=LEFT)
		self.lista.column("#0", width=120, stretch=NO)
		self.lista.column("#1", width=120, stretch=NO)
		self.lista.column("#2", width=120, stretch=NO)
		self.lista.column("#3", width=350, stretch=NO)
		self.lista.column("#4", width=120, stretch=NO)
		self.lista.heading('#0', text='Hora', anchor=CENTER)
		self.lista.heading('#1', text='Función', anchor=CENTER)
		self.lista.heading('#2', text='Origen', anchor=CENTER)
		self.lista.heading('#3', text='Data', anchor=CENTER)
		self.lista.heading('#4', text='Valor', anchor=CENTER)

		scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.lista.yview)
		scrollbar.pack(side=RIGHT, fill='y')
		self.lista.configure(yscrollcommand=scrollbar.set)
		self.lista.pack()

	def draw_buttons(self):
		buttonFrame = ttk.Frame(self.frame)
		buttonFrame.grid(row=7, column=7, columnspan=3)

		btnSend = ttk.Button(buttonFrame, text="Enviar", command=self.can_send)
		btnSend.pack(pady=10)
		btnSend = ttk.Button(buttonFrame, text="Limpiar", command=self.clear_terminal)
		btnSend.pack(pady=10)

	def can_send(self):
		commands = self.valores_int

		arbitrationId = (commands[0] << 5) | commands[1]

		dataLow = commands[2:6][::-1]
		dataHigh = commands[6:10][::-1]
		envio = dataLow + dataHigh

		self.comm.sendCmd(arbitrationId, envio)

	def insert_list(self, data):
		origen = data.arbitration_id & 0x1F
		funcion = data.arbitration_id >> 5
		lst_data = []
		# data = [0x64, 0x06, 0x2e, 0x01, 0x00, 0x00, 0x00, 0xa2]
		for x in data.data:
			lst_data.append(hex(x))

		# Se separa la parte baja y la parte alta y se invierte
		data_low = lst_data[0:4][::-1]
		data_high = lst_data[4:8][::-1]
		str_data = data_low + data_high

		# Recupero el nombre de la función de respuesta
		str_funcion = list(self.functions.keys())[list(self.functions.values()).index(hex(funcion))]

		# Parsea la fecha
		timestamp = datetime.fromtimestamp(data.timestamp).strftime('%H:%M:%S')

		# Posición donde se encuentra la variable consultada dentro de la cadena con la respuesta
		variable = data.data[2]
		# Calcula el valor
		valor = self.microredes.calcularValor(variable, data_low, data_high)

		self.list.insert("", 'end', text=timestamp, values=(str_funcion, hex(origen), str_data, valor))

	def clear_terminal(self):
		for i in self.list.get_children():
			self.list.delete(i)

	def readQueue(self):
		while self.comm.isConnected():
			# print('queueRead')
			queue_read = self.comm.getQueue()
			self.insert_list(queue_read)
			# self.components.insertTerminal(str(queueRead))
			# self.components.insertTerminal('\n')
