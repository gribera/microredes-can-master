from tkinter import DISABLED, NORMAL, Button, IntVar, LabelFrame, StringVar, Toplevel
import tkinter as tk
from tkinter.ttk import Combobox

class Dialog_Connect():
    def __init__(self, master, parent, comm):
        self.master = master
        self.parent = parent
        self.modal = Toplevel(self.master)
        self.comm = comm
        self.ports = self.comm.getPorts()
        self.selectedPort = StringVar()
        self.baudios = IntVar()
        self.bitrate = IntVar()

    def showDialog(self):
        baudios = ['9600', '14400', '19200', '28800', '38400', '57600', '115200']
        bitrate = ['250000', '500000']
        self.modal.geometry('330x210+480+198')
        self.modal.focus_set()
        self.modal.grab_set()
        self.modal.transient(master=self.master)
        self.modal.title("Seleccionar puerto")

        frame = LabelFrame(self.modal)
        frame.grid(row=0, column=0, pady=10, padx=10)

        tk.Label(frame, text="Puerto").grid(row=1, column=0)
        cmbPS = Combobox(frame,
                             values=self.ports,
                             justify="center",
                             textvariable=self.selectedPort,
                             state="readonly")
        cmbPS.bind('<<ComboboxSelected>>', self.portSelect)
        cmbPS.grid(row=1, column=1, padx=10, pady=10)

        if len(self.ports) > 0:
            btnState = NORMAL
            cmbPS.current(0)
        else:
            btnState = DISABLED

        tk.Label(frame, text="Velocidad").grid(row=2, column=0)
        cmbBaudios = Combobox(frame,
                             values=baudios,
                             justify="center",
                             textvariable=self.baudios,
                             state="readonly")

        cmbBaudios.grid(row=2, column=1, padx=10, pady=10)
        cmbBaudios.current(6)

        tk.Label(frame, text="Velocidad Bus").grid(row=3, column=0)
        cmbBitrate = Combobox(frame,
                             values=bitrate,
                             justify="center",
                             textvariable=self.bitrate,
                             state="readonly")

        cmbBitrate.grid(row=3, column=1, padx=10, pady=10)
        cmbBitrate.current(0)

        self.btnConectar = Button(frame, text="Conectar",
                                command=lambda: self.connect(self.selectedPort.get(), self.baudios.get(), self.bitrate.get()),
                                state=btnState)
        self.btnConectar.grid(row=4, column=0, pady=10, padx=10)
        self.btnCancelar = Button(frame, text="Cancelar", command=self.modal.destroy)
        self.btnCancelar.grid(row=4, column=1, pady=10, padx=10)

        self.modal.wait_window(self.modal)

    def portSelect(self, event):
        self.btnConectar.configure(state=NORMAL)

    def connect(self, port, baudios, bitrate):
        self.comm.connect(port, baudios, bitrate)
        self.comm.initQueue()
        # self.parent.buttonStates()
        self.modal.destroy()