import tkinter as tk 
from tkinter import * 
from tkinter import ttk
from dialogs import change_address
from dialogs import connect
import comm as serial
# import commands as commands

class Componentes:
    dicFunctions = {'ERR': '0x01', 'DO': '0x04', 'SET': '0x08', 
                    'QRY': '0x0c', 'ACK': '0x10', 'POST': '0x14', 
                    'HB': '0x18'}

    dicDispOrigen = {'Broadcast': '0x00', 'Master': '0x01'}

    dicDispDestino = {'Equipo 1': '0x02', 'Equipo 2': '0x03'}

    dicVariable = {'DIGITAL_OUT': '0x00', 'DIGITAL_IN': '0x01', 
                    'ANALOG_OUT': '0x012', 'ANALOG_IN': '0x03'}

    combos = [dicFunctions, dicDispOrigen, dicDispDestino, dicVariable, 
                list(range(0,255)), list(range(0,255))]

    comboLabel = ['Función', 'Dispositivo Origen', 'Dispositivo Destino', 
                  'Variable', 'Byte 1', 'Byte 2']

    selectedOption = {}

    valoresInt = []

    selectedPort = {}

    def __init__(self, master, comm):
        self.master = master
        self.comm = comm
        self.esMaestro = ''
        # self.commands = Commands(self.comm)

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        status = Label(self.master, 
                       text="StatusbaR", 
                       bd=1, 
                       relief=tk.SUNKEN).grid(row=10, column=0, columnspan=6, sticky='WE')

        menuFunciones = Menu(menubar, tearoff=0)
        menuSalir = Menu(menubar, tearoff=0)

        menuFunciones.add_command(label="Conectarse", command=self.connect)
        menuFunciones.add_command(label="Cambiar dirección", command=self.changeAddress)
        menuSalir.add_command(label="Salir", command=master.quit)

        menubar.add_cascade(label="Funciones", menu=menuFunciones)
        menubar.add_cascade(label="Salir", menu=menuSalir)

    def changeAddress(self):
        dlg = change_address.dlgCANAddress(self.master, self.comm)
        dlg.showDialog()

    def connect(self):
        dlg = connect.dlgConnect(self.master, self, self.comm)
        dlg.showDialog()

    def getValues(self):
        return self.valoresInt

    def drawValues(self, event):
        self.valoresInt = [int(self.dicFunctions[self.selectedOption[0].get()], 0),
                          int(self.dicDispOrigen[self.selectedOption[1].get()], 0),
                          int(self.dicDispDestino[self.selectedOption[2].get()], 0),
                          int(self.dicVariable[self.selectedOption[3].get()], 0),
                          int(self.selectedOption[4].get()),
                          int(self.selectedOption[5].get()), 0, 0, 0, 0]

        for row in range(0, 3):
            for col in range(0, 6):
                if row == 0:
                    val = self.valoresInt[col]
                if row == 1:
                    val = bin(self.valoresInt[col])[2:].zfill(8)
                if row == 2:
                    val = hex(self.valoresInt[col])

                lb = tk.Label(self.master, text=val, font=("Fixedsys", 10))
                lb.grid(row=row+4, column=col)

    def drawSelect(self):
        for idx in range(0, len(self.combos)):
            self.selectedOption[idx] = tk.StringVar()

            if isinstance(self.combos[idx], dict):
                valores = list(self.combos[idx].keys())
            else:
                valores = self.combos[idx]

            # Agrega etiqueta
            lb = ttk.Label(self.master, text=self.comboLabel[idx])
            lb.grid(row=0, column=idx, padx=10, pady=10)
            # Agrega combo
            cmbFnc = ttk.Combobox(self.master, 
                                  values=valores, 
                                  justify="center", 
                                  textvariable=self.selectedOption[idx], 
                                  state="readonly")
            cmbFnc.bind("<<ComboboxSelected>>", self.drawValues)
            cmbFnc.grid(row=1, column=idx, padx=10, pady=10)
            cmbFnc.current(0)

    def drawTerminal(self):
        self.frame = Frame(self.master)
        self.frame.grid(row=9, column=0, columnspan=6, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.txtTerminal = tk.Text(self.frame, height=14, width=130)
        self.txtTerminal.config(yscrollcommand=self.scrollbar.set, 
                                background="#000000", 
                                foreground="#4DFF00",
                                font=("Fixedsys", 10),
                                padx=3, pady=3)
        self.txtTerminal.grid(row=10, column=0, columnspan=6)

        self.scrollbar.config(command=self.txtTerminal.yview)
        self.scrollbar.grid(row=10, column=6, sticky='NSW')

    def insertTerminal(self, data):
        self.txtTerminal.insert(tk.END, data)
        self.txtTerminal.see("end")

    def clearTerminal(self):
        self.txtTerminal.delete("1.0", tk.END)

    def drawButtons(self):
        self.buttonFrame = Frame(self.master)
        self.buttonFrame.grid(row=8, column=0, columnspan=6)        
        # self.btnSend = Button(self.buttonFrame, text="Enviar", command=self.canSend)
        # self.btnSend.pack(side=LEFT, padx=30, pady=10)
        # self.btnSend = Button(self.buttonFrame, text="Datos Equipo", command=self.datosEquipo)
        # self.btnSend.pack(side=LEFT, padx=30, pady=10)
        # self.btnSend = Button(self.buttonFrame, text="Limpiar", command=self.clearTerminal)
        # self.btnSend.pack(side=LEFT, padx=30, pady=10)

    def buttonStates(self):
        if self.comm.isConnected():
            for child in self.buttonFrame.winfo_children():
                child.configure(state=NORMAL)
        else:
            for child in self.buttonFrame.winfo_children():
                child.configure(state=DISABLED)
