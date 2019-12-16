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

        # Dibuja componentes
        self.components.drawSelect()
        self.components.drawValues(0)
        self.components.drawTerminal()
        self.drawButtons()

        # Se crea el objeto para la comunicación serial
        self.comm = serial.Serial()

        # Inicia thread para recibir datos por el puerto serial
        self.thread1 = threading.Thread(name="listen", target=self.comm.read_from_port)
        self.thread1.start()

        # Inicia thread para leer el queue (datos que entran por puerto serial)
        self.thread2 = threading.Thread(name="read", target=self.readQueue)
        self.thread2.start()

    def closeWindow(self):
        self.thread1.join()
        self.thread2.join()
        self.conn.closePort()
        self.master.quit()

    def readQueue(self):
        while True:
            data = self.comm.getQueue()
            self.components.txtTerminal.insert(tk.END, data)
            self.components.txtTerminal.see("end")

    def datosEquipo(self):
        self.comm.sendCmd('\x1b\x65\x0d'.encode())

    def callback(self):
        self.comm.sendCmd('\x04\x0d'.encode())
        # self.comm.sendCmd('\x04'.encode())
        # self.comm.sendCmd(33554944)
        # self.comm.sendCmd(0)


    def canSend(self):
        self.comm.sendCmd('\x1b\x33\x0d'.encode())
        # print(self.components.getValues())
        commands = self.components.getValues()

        self.comm.sendCmd(str(commands[0]).encode())
        time.sleep(1)
        self.comm.sendCmd(str(commands[1]).encode())
        time.sleep(1)
        self.comm.sendCmd(str(str(commands[2])+
                              str(commands[3])+
                              str(commands[4])+
                              str(commands[5])).encode())
        time.sleep(1)
        self.comm.sendCmd(str(0).encode())

    def drawButtons(self):
        self.btnSend = Button(self.master, text="Enviar", command=self.canSend)
        self.btnSend.grid(column=1, row=8, columnspan=2, padx=10, pady=10)
        self.btnSend = Button(self.master, text="Datos Equipo", command=self.datosEquipo)
        self.btnSend.grid(column=2, row=8, columnspan=2, padx=10, pady=10)
        self.btnSend = Button(self.master, text="Limpiar", command=self.components.clearTerminal)
        self.btnSend.grid(column=3, row=8, columnspan=2, padx=10, pady=10)


root = Tk()
main = MainWindow(root)
root.mainloop()