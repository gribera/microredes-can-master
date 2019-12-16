import serial, queue

class Serial():
    connected = False

    def __init__(self):
        self.port = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=1
        )

        self.q = queue.Queue()

    def closePort(self):
        self.port.close()

    def sendCmd(self, comando):
        self.port.write(comando)

    def getQueue(self):
        return self.q.get()

    def read_from_port(self):
        while not self.connected:
            self.connected = True

            while True:
                self.q.put(self.port.readline().decode())