class Microredes:

    def __init__(self):
        pass

    def calcularValor(self, variable, dataLow, dataHigh):
        calcUrms = [0x10, 0x11, 0x12]
        calcIrms = [0x13, 0x14, 0x15]
        calcIrmsN = [0x16]
        calcPmean = [0x17, 0x18, 0x19]
        calcPmeanT = [0x1a]
        calcQmean = [0x1b, 0x1c, 0x1d]
        calcQmeanT = [0x1e]
        calcSmean = [0x1f, 0x20, 0x21]
        calcSmeanT = [0x22]
        calcPFmean = [0x23, 0x24, 0x25, 0x26]
        calcTHDU = [0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c]
        calcFrec = [0x2d]
        calcTemp = [0x2e]

        valor = 0
        valueLow = int('0x' + ''.join([format(int(c, 16), '02X') for c in dataLow[2:4]]), 16)
        valueHigh = int('0x' + ''.join([format(int(c, 16), '02X') for c in dataHigh[0:1]]), 16)

        if variable in calcUrms:
            valor = 0.01*valueLow+valueHigh/256
            unidad = 'v'
        elif variable in calcIrms:
            valor = 0.001*valueLow+valueHigh/256
            unidad = 'A'
        elif variable in calcIrmsN:
            valor = 0.001*valueLow
            unidad = 'A'
        elif variable in calcPmean:
            sign, valueLow, valueHigh = self.calc(dataLow[2:4], dataHigh[0:2])
            valor = valueLow + valueHigh / 256
            unidad = 'W'
        elif variable in calcPmeanT:
            sign, valueLow, valueHigh = self.calc(dataLow[2:4], dataHigh[0:2])
            valor = 4*(valueLow + valueHigh / 256)
            unidad = 'W'
        elif variable in calcQmean:
            sign, valueLow, valueHigh = self.calc(dataLow[2:4], dataHigh[0:2])
            valor = valueLow + valueHigh / 256
            unidad = 'VAr'
        elif variable in calcQmeanT:
            sign, valueLow, valueHigh = self.calc(dataLow[2:4], dataHigh[0:2])
            valor = 4*(valueLow + valueHigh / 256)
            unidad = 'VAr'
        elif variable in calcSmean:
            sign, valueLow, valueHigh = self.calc(dataLow[2:4], dataHigh[0:2])
            valor = valueLow + valueHigh / 256
            unidad = 'VA'
        elif variable in calcSmeanT:
            sign, valueLow, valueHigh = self.calc(dataLow[2:4], dataHigh[0:2])
            valor = 4*(valueLow + valueHigh / 256)
            unidad = 'VA'
        elif variable in calcPFmean:
            sign, valueLow, valueHigh = self.calc(dataLow[2:4], dataHigh[0:2])
            valor = 0.001*(valueLow + valueHigh / 256)
            unidad = 'W'
        elif variable in calcTHDU:
            valor = 0.01*(valueLow)
            unidad = '%'
        elif variable in calcFrec:
            valor = valueLow/100
            unidad = 'Hz'
        elif variable in calcTemp:
            valor = valueLow
            unidad = 'C'
        else:
            print("La función " + str(variable) + " es incorrecta")
            return

        # Redondea el valor a 3 decimales y lo devuelve en formato string junto con su unidad de medida
        valorFinal = sign + str(round(valor, 3)) + ' ' + unidad

        return valorFinal

    def calc(self, dataLow, dataHigh):
        sign, val = self.twosComplement(dataLow + dataHigh, 32)
        rsl = self.strToHex(val)
        val1 = int('0x' + ''.join([format(int(c, 16), '02X') for c in rsl[0:2]]), 16)
        val2 = int('0x' + ''.join([format(int(c, 16), '02X') for c in rsl[2:4]]), 16)
        return sign, val1, val2

    def twosComplement(self, value, bits):
        # Se pasa a hexa el valor recibido
        val = int('0x' + ''.join([format(int(c, 16), '02X') for c in value]), 16)
        # Cálculo del complemento a 2
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)

        sign = '-' if val < 0 else ''

        return sign, abs(val)

    def strToHex(self, value):
        # Convierto a hexadecimal y elimino '0x' del string
        valor = hex(value)[2:]
        # Agrego ceros a la izquierda para completar los 4 bytes
        valorFilled = valor.zfill(8)
        # Devuelve array de valores agrupado de a dos
        return [hex(int(valorFilled[i:i+2], 16)) for i in range(0, len(valorFilled), 2)]
