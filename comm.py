import serial, queue

class Serial():
    connected = False

    def __init__(self):
        self.port = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=1
        )

        if self.port.isOpen():
            self.connected = True

        self.q = queue.Queue()

    def isConnected(self):
        return self.connected

    def closePort(self):
        self.port.close()
        self.connected = False

    def sendCmd(self, comando):
        self.port.write(comando)

    def getQueue(self):
        return self.q.get()

    def readFromPort(self):
        while self.connected:
            self.q.put(self.port.readline().decode())