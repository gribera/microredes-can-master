import queue, serial.tools.list_ports,threading


class Serial():
    connected = False
    port = None
    q = None
    thread = None

    def __init__(self, thread):
        self.thread = thread

    def connect(self, port, baudrate):
        self.port = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=1
        )

        if self.port.isOpen():
            self.connected = True

        self.initQueue()

        # Inicia thread para recibir datos por el puerto serial
        self.thread1 = threading.Thread(name="listen", target=self.readFromPort)
        self.thread1.start()

        # Inicia thread para leer el queue (datos que entran por puerto serial)
        self.thread.start()


    def initQueue(self):
        self.q = queue.Queue()

    def isConnected(self):
        return self.connected

    def closePort(self):
        self.connected = False
        self.port.close()
        self.thread1.join()
        self.thread.join()

    def getPorts(self):
        ports = []
        for x in serial.tools.list_ports.comports():
            ports.append(x.device)

        return ports

    def sendCmd(self, comando):
        self.port.write(comando)

    def getQueueEmpty(self):
        return self.q.empty()

    def getQueue(self):
        return self.q.get()

    def readFromPort(self):
        while self.connected:
            self.q.put(self.port.readline().decode())