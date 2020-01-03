import comm as serial

class Commands():
	def __init__(self, comm):
		self.comm = comm

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

        # self.comm.sendCmd('\x1b\x34'.encode())
        # envio = '\x04\x01\x03\x00\x02\x00\x00\x00\x00\x00'
        # self.comm.sendCmd(envio.encode())
        # self.comm.sendCmd('\x0d'.encode())
