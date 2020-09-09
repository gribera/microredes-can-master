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

    dicDispDestino = {'Equipo 2': '0x02', 'Equipo 3': '0x03', 'Equipo 4': '0x04'}

    dicVariable = {'DIGITAL_OUT': '0x00', 'DIGITAL_IN': '0x01',
                    'ANALOG_OUT': '0x02', 'ANALOG_IN': '0x03',
                    'MODO_FUNC': '0x04', 'ANALOG': '0x05', 'IN-AMP': '0x06',
                    'AMP-INAMP': '0x07','PWM': '0x08', 'ECHO': '0x09',
                    'RTC1': '0x0A', 'PARADA': '0x0B', 'SOFT_RESET': '0x0C',
                    'U_A': '0x10', 'U_B': '0x11', 'U_C': '0x12',
                    'I_A': '0x13', 'I_B': '0x14', 'I_C': '0x15', 'I_N1': '0x16',
                    'PA_A': '0x17', 'PA_B': '0x18', 'PA_C': '0x19', 'PA_TOT': '0x1A',
                    'PR_A': '0x1B', 'PR_B': '0x1C', 'PR_C': '0x1D', 'PR_TOT': '0x1E',
                    'PS_A': '0x1F', 'PS_B': '0x20', 'PS_C': '0x21', 'PS_TOT': '0x22',
                    'FP_A': '0x23', 'FP_B': '0x24', 'FP_C': '0x25', 'FP_TOT': '0x26',
                    'THDU_A': '0x27', 'THDU_B': '0x28', 'THDU_C': '0x29',
                    'THDI_A': '0x2A', 'THDI_B': '0x2B', 'THDI_C': '0x2C',
                    'FREC': '0x2D', 'TEMP': '0x2E'}

    combos = [dicFunctions, dicDispOrigen, dicDispDestino, dicVariable,
                list(range(0,255)), list(range(0,255)), list(range(0,255)),
                list(range(0,255)), list(range(0,255)), list(range(0,255))]

    comboLabel = ['Función', 'Origen', 'Destino', 'Variable',
                  'Byte 1', 'Byte 2', 'Byte 3', 'Byte 4', 'Byte 5',
                  'Byte 6', 'Byte 7']

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
                       relief=tk.SUNKEN).grid(row=10, column=0, columnspan=10, sticky='WE')

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
        # frame = LabelFrame(self.master)
        # frame.grid(row=7, column=0, columnspan=10, pady=10, padx=10)

        self.valoresInt = [int(self.dicFunctions[self.selectedOption[0].get()], 0),
                          int(self.dicDispOrigen[self.selectedOption[1].get()], 0),
                          int(self.dicDispDestino[self.selectedOption[2].get()], 0),
                          int(self.dicVariable[self.selectedOption[3].get()], 0),
                          int(self.selectedOption[4].get()),
                          int(self.selectedOption[5].get()),
                          int(self.selectedOption[6].get()),
                          int(self.selectedOption[7].get()),
                          int(self.selectedOption[8].get()),
                          int(self.selectedOption[9].get())]

        for row in range(0, 3):
            for col in range(0, 10):
                if row == 0:
                    val = self.valoresInt[col]
                if row == 1:
                    val = bin(self.valoresInt[col])[2:].zfill(8)
                if row == 2:
                    val = hex(self.valoresInt[col])

                lb = tk.Label(self.master, text=val, font=("Fixedsys", 10))
                lb.grid(row=row+4, column=col)

    def drawSelect(self):
        row = 1
        col = 0
        for idx in range(0, len(self.combos)):
            self.selectedOption[idx] = tk.StringVar()

            if isinstance(self.combos[idx], dict):
                valores = list(self.combos[idx].keys())
            else:
                valores = self.combos[idx]

            if idx % 6 == 0 and idx != 0:
                row += 1
                col = 2

            # Agrega etiqueta
            lb = ttk.Label(self.master, text=self.comboLabel[idx])
            lb.grid(row=1, column=idx, padx=10, pady=10)
            # Agrega combo
            cmbFnc = ttk.Combobox(self.master,
                                  values=valores,
                                  justify="center",
                                  textvariable=self.selectedOption[idx],
                                  state="readonly", width=12)
            cmbFnc.bind("<<ComboboxSelected>>", self.drawValues)
            cmbFnc.grid(row=2, column=idx, padx=5, pady=10)
            cmbFnc.current(0)
            col += 1

    def drawTerminal(self):
        self.frame = Frame(self.master)
        self.frame.grid(row=8, column=0, columnspan=8, padx=10, pady=10)



        self.list = ttk.Treeview(self.frame, selectmode='browse', columns=("#0","#1", "#2", "#3"))
        self.list.pack(side=LEFT)
        # self.list.grid(row=8, column=0, padx=10, pady=10, columnspan=8)
        self.list.column("#0", width=100)
        self.list.column("#1", width=100)
        self.list.column("#2", width=100)
        self.list.column("#3", width=100)
        self.list.column("#4", width=300)
        self.list.heading('#0', text='Hora', anchor=CENTER)
        self.list.heading('#1', text='Función', anchor=CENTER)
        self.list.heading('#2', text='Origen', anchor=CENTER)
        self.list.heading('#3', text='Variable', anchor=CENTER)
        self.list.heading('#4', text='Data', anchor=CENTER)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.list.yview)
        self.scrollbar.pack(side=RIGHT, fill='y')
        self.list.configure(yscrollcommand=self.scrollbar.set)


        # self.scrollbar = tk.Scrollbar(self.frame)
        # self.txtTerminal = tk.Text(self.frame, height=14, width=130)
        # self.txtTerminal.config(yscrollcommand=self.scrollbar.set,
        #                         background="#000000",
        #                         foreground="#4DFF00",
        #                         font=("Fixedsys", 10),
        #                         padx=3, pady=3)
        # self.txtTerminal.grid(row=10, column=0, columnspan=10)

        # self.scrollbar.config(command=self.txtTerminal.yview)
        # self.scrollbar.grid(row=10, column=6, sticky='NSW')

    def insertTerminal(self, data):
        self.txtTerminal.insert(tk.END, data)
        self.txtTerminal.see("end")

    def insertList(self, data):
        # print(hex((msg.arbitration_id & 0x1F)))
        # print(hex(msg.arbitration_id >> 5))
        origen = data.arbitration_id & 0x1F
        funcion = data.arbitration_id >> 5
        lstData = []
        for x in data.data:
            lstData.append(hex(x))
            pass

        dataLow = lstData[0:4][::-1]
        dataHigh = lstData[4:8][::-1]
        strData = dataLow + dataHigh

        self.list.insert("", 'end', text=data.timestamp, values=(hex(funcion), hex(origen), "", strData))

    def clearList(self):
        for i in self.list.get_children():
            self.list.delete(i)
        # self.txtTerminal.delete("1.0", tk.END)

    def drawButtons(self):
        self.buttonFrame = Frame(self.master)
        self.buttonFrame.grid(row=8, column=0, columnspan=10)
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
