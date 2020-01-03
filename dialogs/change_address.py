from tkinter import * 
import tkinter as tk 
# import comm as serial

class dlgCANAddress():
    def __init__(self, master, comm):
        self.master = master
        self.comm = comm

    def showDialog(self):
        modal = Toplevel(self.master)
        modal.geometry('310x160+480+198')
        modal.focus_set()
        modal.grab_set()
        modal.transient(master=self.master)
        modal.title("Setear dirección")

        frame = LabelFrame(modal)
        frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        self.esMaestro = tk.IntVar()
        Checkbutton(frame, text="Maestro", 
                    variable=self.esMaestro, command=self.cb).grid(row=0, 
                                                                   column=0, 
                                                                   pady=10,
                                                                   padx=10,
                                                                   sticky='W')

        Label(frame, text="Dirección").grid(row=1, column=0, pady=10, padx=10)
        self.canAddr = Entry(frame, state=tk.NORMAL)
        self.canAddr.grid(row=1, column=1, pady=10, padx=10)

        self.btnGuardar = Button(frame, text="Guardar", command=self.setAddr)
        self.btnGuardar.grid(row=3, column=0, pady=10, padx=10)
        self.btnCancelar = Button(frame, text="Cancelar", command=modal.destroy)
        self.btnCancelar.grid(row=3, column=1, pady=10, padx=10)

        modal.wait_window(modal)

    def cb(self):
        if (self.esMaestro.get() == 1):
            self.canAddr.config(state=tk.DISABLED) 
        else:
            self.canAddr.config(state=tk.NORMAL)

    def setAddr(self):
        self.comm.sendCmd('\x1b\x65\x0d'.encode())