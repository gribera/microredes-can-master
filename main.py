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
        # self.master.geometry("1230x466")

        # self.master.attributes("-fullscreen", True)

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
            time.sleep(0.1)
            # print('queueRead')
            queueRead = self.comm.getQueue()
            print("TIPO")
            print(type(queueRead))
            self.components.insertList(queueRead)
            # self.components.insertTerminal(str(queueRead))
            # self.components.insertTerminal('\n')
        print('QUEUE STOPPED')


    def datosEquipo(self):
        pass
        # self.comm.sendCmd('\x1b\x65\x0d'.encode())

    def canSend(self):
        commands = self.components.getValues()

        arbitrationId = (commands[0] << 5) | commands[1]

        dataLow = commands[2:6][::-1]
        dataHigh = commands[6:10][::-1]
        envio = dataLow + dataHigh

        self.comm.sendCmd(arbitrationId, envio)

    def drawButtons(self):
        self.buttonFrame = Frame(self.master)
        self.buttonFrame.grid(row=8, column=8, columnspan=2)        
        self.btnSend = Button(self.buttonFrame, text="Enviar", command=self.canSend)
        self.btnSend.pack(side=TOP, padx=30, pady=10)
        self.btnSend = Button(self.buttonFrame, text="Datos Equipo", command=self.datosEquipo)
        self.btnSend.pack(side=TOP, padx=30, pady=10)
        self.btnSend = Button(self.buttonFrame, text="Limpiar", command=self.components.clearList)
        self.btnSend.pack(side=TOP, padx=30, pady=10)


root = Tk()
main = MainWindow(root)
root.mainloop()