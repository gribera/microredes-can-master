class Microredes:

    def __init__(self):
        pass

    def calcularValor(self, fnc, dataLow, dataHigh):
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
        valueHigh = int(str(dataHigh[0]), 16)

        if fnc in calcUrms:
            valor = 0.01*valueLow+valueHigh/256
            unidad = 'v'
        elif fnc in calcIrms:
            valor = 0.001*valueLow+valueHigh/256
            unidad = 'A'
        elif fnc in calcIrmsN:
            valor = 0.001*valueLow
            unidad = 'A'
        elif fnc in calcPmean:
            valor = valueLow+valueHigh/256
            unidad = 'W'
        elif fnc in calcPmeanT:
            valor = 4*(valueLow+valueHigh/256)
            unidad = 'W'
        elif fnc in calcQmean:
            valor = valueLow+valueHigh/256
            unidad = 'VAr'
        elif fnc in calcQmeanT:
            valor = 4*(valueLow+valueHigh/256)
            unidad = 'VAr'
        elif fnc in calcSmean:
            valor = valueLow+valueHigh/256
            unidad = 'VA'
        elif fnc in calcSmeanT:
            valor = 4*(valueLow+valueHigh/256)
            unidad = 'VA'
        elif fnc in calcPFmean:
            valor = 0.001*valueLow
            unidad = ''
        elif fnc in calcTHDU:
            valor = 0.01*(valueLow)
            unidad = '%'
        elif fnc in calcFrec:
            valor = valueLow/100
            unidad = 'Hz'
        elif fnc in calcTemp:
            valor = valueLow
            unidad = 'C'
        else:
            print("La función es incorrecta")

        # Redondea el valor a 3 decimales y lo devuelve en formato string junto con su unidad de medida
        valorFinal = str(round(valor, 3)) + ' ' + unidad

        return valorFinal