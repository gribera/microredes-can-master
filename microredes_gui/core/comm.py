import can, queue, serial.tools.list_ports, threading

class Serial():
	connected = False
	port = None
	q = None
	thread = None

	def __init__(self, thread):
		self.thread = thread

	def connect(self, port, baudrate, bitrate):
		self.bus = can.interface.Bus(bustype='robotell',
		                             channel=port,
		                             ttyBaudrate=baudrate,
		                             bitrate=bitrate)

		self.connected = True
		self.initQueue()

		# Inicia thread para recibir datos por el puerto serial
		self.thread1 = threading.Thread(name="listen", target=self.readFromBus)
		self.thread1.start()

		# Inicia thread para leer el queue (datos que entran por puerto serial)
		self.thread.start()

	def initQueue(self):
		self.q = queue.Queue()

	def isConnected(self):
		return self.connected

	def closePort(self):
		self.connected = False
		self.thread.join()
		self.thread1.join()

	def getPorts(self):
		ports = []
		for x in serial.tools.list_ports.comports():
			ports.append(x.device)

		return ports

	def sendCmd(self, id, comando):
		msg = can.Message(arbitration_id=id,
		data=comando,
		is_extended_id=False)

		self.bus.send(msg)

	def getQueueEmpty(self):
		return self.q.empty()

	def getQueue(self):
		return self.q.get()

	def readFromBus(self):
		while self.connected:
			msg = self.bus.recv()
			if msg is not None:
				self.q.put(msg)