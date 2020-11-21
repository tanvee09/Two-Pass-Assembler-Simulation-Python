from tables import *

def toBinary(n, b: int) -> str:
    binary = bin(int(str(n), b)).replace("0b", "")
    if binary[0] == '-':
        return '1' * (8 - len(binary) + 1) + ''.join(['1' if bit == '0' else '0' for bit in binary[1:]])
    else:
        return '0' * (8 - len(binary)) + binary

def findAddressingMode(address: str) -> str :
    if address[0] == '#':
        return addressingModes['direct']
    elif address[0] == '@':
        return addressingModes['indirect']
    elif address[0] == '$':
        return addressingModes['relativePC']
    elif address[0] == '+':
        return addressingModes['base']
    elif address[-1] == ')':
        return addressingModes['registerIndirect']
    elif address[-1] == '+':
        return addressingModes['autoInc']
    elif address in generalPurposeRegs:
        return addressingModes['regsiter']
    else:
        return addressingModes['direct']

def findAddressBits(address: str, addMode: str, addSymbol: dict) -> str:
    if addMode == '1101':
        return generalPurposeRegs[address]
    elif addMode == '1110':
        return generalPurposeRegs[address[1:-1]]
    elif addMode == '1111':
        return generalPurposeRegs[address[1:-2]]
    elif address.isdecimal() or (addMode != '1001' and address[1:].isdecimal()):
        return address
    elif addMode == '1001':
        return toBinary(addSymbol[address], 10)
    else:
        return toBinary(addSymbol[address[1:]], 10)

def binaryForMRI(inst: list, LC: int, addSymbol: dict) -> str:
    addMode = findAddressingMode(inst[-1])
    opcode = MRI[inst[0]]
    address = findAddressBits(inst[-1], addMode, addSymbol)
    return [[toBinary(int(LC), 10), addMode + opcode], [toBinary(int(LC + 1), 10), address]]

def binaryForNMRI_acc(inst: list, LC: int) -> str:
    addMode = "0000"
    opcode = NMRI_acc[inst[0]]
    return [toBinary(int(LC), 10), addMode + opcode]

def binaryForNMRI_io(inst: list, LC: int) -> str:
    addMode = "0111"
    opcode = NMRI_io[inst[0]]
    return [toBinary(int(LC), 10), addMode + opcode]
