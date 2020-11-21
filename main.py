from tables import *
from helper import *


# FIRST PASS

LC = 0
addSymbol = dict()

with open("machineCode.txt", mode='r') as f:
    for line in f:
        inst = line.split()
        if line[0] == ".":
            addSymbol.update({inst[0][1:]:LC})
        else:
            oprn = inst[0]
            if oprn == 'ORG':
                LC = int(inst[1])
                continue
            elif oprn == 'END':
                LC += 1
                break
            elif oprn in MRI:
                LC += 1
        LC += 1


# SECOND PASS

LC = 0
binary_code = []

with open("machineCode.txt", mode='r') as f:
    for line in f:
        inst = line.split('/')[0].split()
        if line[0] == ".":
            if inst[1] == 'DEC':
                binary_code.append([toBinary(addSymbol[inst[0][1:]], 10), toBinary(inst[-1], 10)])
            elif inst[1] == 'HEX':
                binary_code.append([toBinary(addSymbol[inst[0][1:]], 10), toBinary(inst[-1], 16)])
        else:
            oprn = inst[0]
            if oprn == 'ORG':
                LC = int(inst[1])
                continue
            elif oprn == 'END':
                break
            elif oprn in MRI:
                binary_code += binaryForMRI(inst, LC, addSymbol)
                LC += 1
            elif oprn in NMRI_io:
                binary_code.append(binaryForNMRI_io(inst, LC))
            elif oprn in NMRI_acc:
                binary_code.append(binaryForNMRI_acc(inst, LC))
        LC += 1

with open("binarycode.txt", mode='w') as f:
    f.write('LOCATION\t\tCONTENT\n\n')
    f.writelines([ins[0] + '\t\t' + ins[1] + '\n' for ins in binary_code])
