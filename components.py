import tkinter as tk 
from tkinter import Frame, ttk

class Componentes:
    dicFunctions = {'ERR': '0x01', 'DO': '0x04', 'SET': '0x08', 'QRY': '0x0c', 'ACK': '0x10', 'POST': '0x14', 'HB': '0x18'}
    dicDispOrigen = {'Broadcast': '0x00', 'Master': '0x01'}
    dicDispDestino = {'Equipo 1': '0x02', 'Equipo 2': '0x03'}
    dicVariable = {'DIGITAL_OUT': '0x00', 'DIGITAL_IN': '0x01', 'ANALOG_OUT': '0x012', 'ANALOG_IN': '0x03'}
    combos = [dicFunctions, dicDispOrigen, dicDispDestino, dicVariable, list(range(0,255)), list(range(0,255))]

    comboLabel = ['Función', 'Dispositivo Origen', 'Dispositivo Destino', 'Variable', 'Byte 1', 'Byte 2']

    selectedOption = {}

    valoresInt = []

    def __init__(self, master):
        self.master = master


    def getValues(self):
        return self.valoresInt

    def drawValues(self, event):
        label = {}

        self.valoresInt = [int(self.dicFunctions[self.selectedOption[0].get()], 0),
                          int(self.dicDispOrigen[self.selectedOption[1].get()], 0),
                          int(self.dicDispDestino[self.selectedOption[2].get()], 0),
                          int(self.dicVariable[self.selectedOption[3].get()], 0),
                          int(self.selectedOption[4].get()),
                          int(self.selectedOption[5].get())]

        for row in range(0, 3):
            for col in range(0, len(self.valoresInt)):
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
            lb = tk.Label(self.master, text=self.comboLabel[idx])
            lb.grid(row=0, column=idx, padx=10, pady=10)
            # Agrega combo
            cmbFnc = ttk.Combobox(self.master, values=valores, justify="center", textvariable=self.selectedOption[idx], state="readonly")
            cmbFnc.bind("<<ComboboxSelected>>", self.drawValues)
            cmbFnc.grid(row=1, column=idx, padx=10, pady=10)
            cmbFnc.current(0)

    def drawTerminal(self):
        self.frame = Frame(self.master)
        self.frame.grid(column=0, row=9, columnspan=6, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.txtTerminal = tk.Text(self.frame, height=14, width=130)
        self.txtTerminal.config(yscrollcommand=self.scrollbar.set, 
                                background="#000000", 
                                foreground="#4DFF00",
                                font=("Fixedsys", 10))
        self.txtTerminal.grid(column=0, row=10, columnspan=6)

        self.scrollbar.config(command=self.txtTerminal.yview)
        self.scrollbar.grid(column=6, row=10, sticky='NSW')

    def clearTerminal(self):
        self.txtTerminal.delete("1.0", tk.END)