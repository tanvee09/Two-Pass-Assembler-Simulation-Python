from tables import *
import re


def callError(lineNo: int, errMessage: str) :
    print('\033[91m' + 'Error at line {}: {}'.format(lineNo, errMessage) + '\033[0m')
    exit(1)


def toBinary(n, b: int) -> str:
    binary = bin(int(str(n), b)).replace("0b", "")
    if binary[0] == '-':
        return '1' * (8 - len(binary) + 1) + ''.join(['1' if bit == '0' else '0' for bit in binary[1:]])
    else:
        return '0' * (8 - len(binary)) + binary


def findAddressingMode(address: str) -> str :
    if address[0] == '#':
        return addressingModes['immediate']
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
        return addressingModes['register']
    else:
        return addressingModes['direct']


def findAddressBits(address: str, addMode: str, addSymbol: dict, lineNo: int) -> str:
    if addMode == '1101': # Register
        if address not in generalPurposeRegs.keys():
            callError(lineNo, "Referenced Register does not exist")
        return generalPurposeRegs[address]

    elif addMode == '1110': # registerIndirect
        if address not in generalPurposeRegs.keys():
            callError(lineNo, "Referenced Register does not exist")
        return generalPurposeRegs[address[1:-1]]

    elif addMode == '1111': # autoInc
        if address not in generalPurposeRegs.keys():
            callError(lineNo, "Referenced Register does not exist")
        return generalPurposeRegs[address[1:-2]]

    elif addMode == '1000': # immediate
        if len(address) != 8 or re.fullmatch("[01]*", address) == None:
            callError(lineNo, "Address should be in binary")
        return toBinary(address[1:], 2)

    if addMode != '1001':# not direct
        address = address[1:]

    if len(address) == 8 and re.fullmatch("[01]*", address) != None:
        return toBinary(address, 2)
    elif address in addSymbol.keys():
        return toBinary(addSymbol[address], 10)
    else:
        callError(lineNo, "Address should be in binary")


def binaryForMRI(inst: list, LC: int, addSymbol: dict, lineNo: int) -> str:
    addMode = findAddressingMode(inst[-1])
    opcode = MRI[inst[0]]
    address = findAddressBits(inst[-1], addMode, addSymbol, lineNo)
    return [[toBinary(int(LC), 10), addMode + opcode], [toBinary(int(LC + 1), 10), address]]


def binaryForNMRI_acc(inst: list, LC: int) -> str:
    addMode = "0000"
    opcode = NMRI_acc[inst[0]]
    return [toBinary(int(LC), 10), addMode + opcode]


def binaryForNMRI_io(inst: list, LC: int) -> str:
    addMode = "0111"
    opcode = NMRI_io[inst[0]]
    return [toBinary(int(LC), 10), addMode + opcode]