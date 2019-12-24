import tkinter as tk 
import threading
import comm as serial
import components
import time

from tkinter import Button, Tk

class MainWindow:
    def __init__(self, master):
        self.master = master
        
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)

        # Título de la ventana
        self.master.title("CAN Sender-Receiver")

        # Dimensión de la pantalla
        self.master.geometry("1190x500")

        # Instancia la clase con los componentes que se verán en pantalla
        self.components = components.Componentes(self.master)

        # Se crea el objeto para la comunicación serial
        self.comm = serial.Serial()

        # Dibuja componentes
        self.components.drawSelect()
        self.components.drawValues(0)
        self.components.drawTerminal()
        # self.components.drawPortSelect(self.comm.getPorts())
        self.drawButtons()

        self.comm.getPorts()

        # Inicia thread para recibir datos por el puerto serial
        self.thread1 = threading.Thread(name="listen", target=self.comm.readFromPort)
        self.thread1.start()

        # # Inicia thread para leer el queue (datos que entran por puerto serial)
        self.thread2 = threading.Thread(name="read", target=self.readQueue)
        self.thread2.start()

    def closeWindow(self):
        self.master.destroy()
        self.comm.closePort()
        self.thread2.join()
        self.thread1.join()

    def readQueue(self):
        while self.comm.isConnected():
            self.components.insertTerminal(self.comm.getQueue())

    def datosEquipo(self):
        self.comm.sendCmd('\x1b\x65\x0d'.encode())

    def canSend(self):
        self.comm.sendCmd('\x1b\x34'.encode())
        commands = self.components.getValues()

        print(commands)

        envio = ''
        for x in range(0,9):
            envio = envio + hex(commands[x])[2:].zfill(2)

        print(envio)
        self.comm.sendCmd(bytes.fromhex(envio))
        self.comm.sendCmd('\x0d'.encode())

    def drawPorts(self):
        for p in self.comm.getPorts():
            print(p.device)

    def drawButtons(self):
        self.btnSend = Button(self.master, text="Enviar", command=self.canSend)
        self.btnSend.grid(row=8, column=1, columnspan=2, padx=10, pady=10)
        self.btnSend = Button(self.master, text="Datos Equipo", command=self.datosEquipo)
        self.btnSend.grid(row=8, column=2, columnspan=2, padx=10, pady=10)
        self.btnSend = Button(self.master, text="Limpiar", command=self.components.clearTerminal)
        self.btnSend.grid(row=8, column=3, columnspan=2, padx=10, pady=10)

root = Tk()
main = MainWindow(root)
root.mainloop()