from tkinter import DISABLED, NORMAL, Button, IntVar, LabelFrame, StringVar, Toplevel
import tkinter as tk
from tkinter.ttk import Combobox

class Dialog_Connect():
    def __init__(self, master, parent, comm):
        self.master = master
        self.parent = parent
        self.modal = Toplevel(self.master)
        self.comm = comm
        self.ports = self.comm.get_ports()
        self.selected_port = StringVar()
        self.baudios = IntVar()
        self.bitrate = IntVar()

    def show_dialog(self):
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
        cmb_ps = Combobox(frame,
                             values=self.ports,
                             justify="center",
                             textvariable=self.selected_port,
                             state="readonly")
        cmb_ps.bind('<<ComboboxSelected>>', self.port_select)
        cmb_ps.grid(row=1, column=1, padx=10, pady=10)

        if len(self.ports) > 0:
            btn_state = NORMAL
            cmb_ps.current(0)
        else:
            btn_state = DISABLED

        tk.Label(frame, text="Velocidad").grid(row=2, column=0)
        cmb_baudios = Combobox(frame,
                             values=baudios,
                             justify="center",
                             textvariable=self.baudios,
                             state="readonly")

        cmb_baudios.grid(row=2, column=1, padx=10, pady=10)
        cmb_baudios.current(6)

        tk.Label(frame, text="Velocidad Bus").grid(row=3, column=0)
        cmb_bitrate = Combobox(frame,
                             values=bitrate,
                             justify="center",
                             textvariable=self.bitrate,
                             state="readonly")

        cmb_bitrate.grid(row=3, column=1, padx=10, pady=10)
        cmb_bitrate.current(0)

        self.btn_conectar = Button(frame, text="Conectar",
                                command=lambda: self.connect(self.selected_port.get(), self.baudios.get(), self.bitrate.get()),
                                state=btn_state)
        self.btn_conectar.grid(row=4, column=0, pady=10, padx=10)
        self.btn_cancelar = Button(frame, text="Cancelar", command=self.modal.destroy)
        self.btn_cancelar.grid(row=4, column=1, pady=10, padx=10)

        self.modal.wait_window(self.modal)

    def port_select(self, event):
        self.btn_conectar.configure(state=NORMAL)

    def connect(self, port, baudios, bitrate):
        self.comm.connect(port, baudios, bitrate)
        # self.comm.initQueue()
        # self.parent.buttonStates()
        self.modal.destroy()