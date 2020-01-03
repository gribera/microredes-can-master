from tkinter import * 
import tkinter as tk 
import comm as serial
import components
import time
import threading

from tkinter import Button, Tk

class MainWindow:
    def __init__(self, master):
        self.master = master
        
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)

        self.master.resizable(0,0)

        # Título de la ventana
        self.master.title("CAN Sender-Receiver")

        # Dimensión de la pantalla
        self.master.geometry("1184x466")

        self.thread2 = threading.Thread(name="read", target=self.readQueue)

        # Se crea el objeto para la comunicación serial
        self.comm = serial.Serial(self.thread2)

        # Instancia la clase con los componentes que se verán en pantalla
        self.components = components.Componentes(self.master, self.comm)

        # Dibuja componentes
        self.components.drawSelect()
        self.components.drawValues(0)
        self.components.drawTerminal()
        # self.components.drawPortSelect(self.comm.getPorts())
        self.components.drawButtons()
        self.components.buttonStates()

        self.drawButtons()

    def closeWindow(self):
        if self.comm.isConnected():
            print('CLOSING PORT')
            self.comm.closePort()
        print('DESTROY')
        # self.thread2.join()
        self.master.destroy()

    def readQueue(self):
        while self.comm.isConnected():
            self.components.insertTerminal(self.comm.getQueue())
        print('QUEUE STOPPED')


    def datosEquipo(self):
        self.comm.sendCmd('\x1b\x65\x0d'.encode())

    def canSend(self):
        self.comm.sendCmd('\x1b\x34'.encode())
        commands = self.components.getValues()

        envio = ''
        for x in range(0,9):
            envio = envio + hex(commands[x])[2:].zfill(2)

        self.comm.sendCmd(bytes.fromhex(envio))
        self.comm.sendCmd('\x0d'.encode())

    def drawButtons(self):
        self.buttonFrame = Frame(self.master)
        self.buttonFrame.grid(row=8, column=0, columnspan=6)        
        self.btnSend = Button(self.buttonFrame, text="Enviar", command=self.canSend)
        self.btnSend.pack(side=LEFT, padx=30, pady=10)
        self.btnSend = Button(self.buttonFrame, text="Datos Equipo", command=self.datosEquipo)
        self.btnSend.pack(side=LEFT, padx=30, pady=10)
        self.btnSend = Button(self.buttonFrame, text="Limpiar", command=self.components.clearTerminal)
        self.btnSend.pack(side=LEFT, padx=30, pady=10)


root = Tk()
main = MainWindow(root)
root.mainloop()