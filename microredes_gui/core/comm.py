import can, serial.tools.list_ports, threading
from queue import Queue


class Serial():
	connected = False
	port = None
	q = Queue()
	queue_thread = None
	bus_thread = None

	def __init__(self):
		pass

	def connect(self, port, baudrate, bitrate):
		self.bus = can.interface.Bus(bustype='robotell',
		                             channel=port,
		                             ttyBaudrate=baudrate,
		                             bitrate=bitrate)


		self.connected = True

		# Inicia thread para recibir datos por el puerto serial
		self.init_bus_thread()

	def init_bus_thread(self):
		self.bus_thread = threading.Thread(name="listen", target=self.read_from_bus)
		self.bus_thread.start()

	def disconnect(self):
		self.connected = False
		self.send_cmd(385, [0, 0, 1, 2, 0, 0, 0, 0])

	def is_connected(self):
		return self.connected

	def get_ports(self):
		ports = []
		for x in serial.tools.list_ports.comports():
			ports.append(x.device)

		return ports

	def send_cmd(self, id, comando):
		msg = can.Message(arbitration_id=id,
		data=comando,
		is_extended_id=False)

		self.bus.send(msg)

	def get_queue(self):
		return self.q.get()

	def read_from_bus(self):
		while self.is_connected():
			msg = self.bus.recv()
			self.q.put(msg)
