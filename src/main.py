import re
from tables import *
from helper import *




# FIRST PASS

LC = 0
addSymbol = dict()

lineNo = 0

with open("../examples/machineCode.txt", mode='r') as f:
    for line in f:
        lineNo += 1
        inst = line.split('/')[0].split()
        if line[0] == ".":
            label = inst[0][1:]
            # label repeated
            if label in addSymbol:
                callError(lineNo, "Labels cannot be repeated ")
            # label length > 3
            elif len(label) > 3:
                callError(lineNo, "Labels cannot exceed length 3")
            # Same as register names (R1, R2, R3, R4)
            x = re.fullmatch("R1|R2|R3|R4", label)
            if x:
                callError(lineNo, "Label can not be Register name")
            # Should be alphanumeric and should start with an alphabet
            x = re.fullmatch("[a-zA-Z][a-zA-Z0-9]*", label)
            if x == None:
                callError(lineNo, "Label should be alphanumeric and should start with an alphabet")
            addSymbol.update({label:LC})
        else:
            if len(inst) == 0 :
                callError(lineNo,"Line can not be empty or can not start with a comment, it must start with an instruction or a label")
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

lineNo = 0

with open("../examples/machineCode.txt", mode='r') as f:
    for line in f:
        lineNo += 1
        inst = line.split('/')[0].split()

        if len(inst) == 0 :
            callError(lineNo,"Line can not be empty or can not start with a comment, it must start with an instruction or a label")

        #

        if line[0] == ".":
            if inst[1] == 'DEC':
                try:
                    int(inst[-1])
                except:
                    callError(lineNo, "Value at label should be decimal")
                if int(inst[-1]) > (2**7 - 1) or int(inst[-1]) < -2**7 + 1:
                    callError(lineNo, "Value out of bounds")
                binary_code.append([toBinary(addSymbol[inst[0][1:]], 10), toBinary(inst[-1], 10)])
                continue
            elif inst[1] == 'HEX':
                try:
                    int(inst[-1], 16)
                except:
                    callError(lineNo, "Value at label should be hexadecimal")
                if int(inst[-1], 16) > (2**7 - 1) or int(inst[-1], 16) < -2**7 + 1: # -7F FF
                    callError(lineNo, "Value out of bounds")
                binary_code.append([toBinary(addSymbol[inst[0][1:]], 10), toBinary(inst[-1], 16)])
                continue
            else:
                inst = inst[1:]


        oprn = inst[0]
        if oprn == 'ORG':
            LC = int(inst[1])
            continue
        elif oprn == 'END':
            break
        elif oprn in MRI:
            if len(inst) != 2:
                callError(lineNo, "Invalid number of operands")
            binary_code += binaryForMRI(inst, LC, addSymbol, lineNo)
            LC += 1
        elif oprn in NMRI_io:
            if len(inst) > 1:
                callError(lineNo, "Invalid number of operands")
            binary_code.append(binaryForNMRI_io(inst, LC))
        elif oprn in NMRI_acc:
            if len(inst) > 1:
                callError(lineNo, "Invalid number of operands")
            binary_code.append(binaryForNMRI_acc(inst, LC))
        else:
            callError(lineNo, "Opcode not found")
        LC += 1
        if LC >= 2**8:
            callError(lineNo, "Program memory out of bounds")

    else:
        callError(lineNo, "END not found. Machine program should end with END")


with open("../examples/binaryCode.txt", mode='w') as f:
    f.write('LOCATION\t\tCONTENT\n\n')
    f.writelines([ins[0] + '\t\t' + ins[1] + '\n' for ins in binary_code])

print('\033[92m' + 'Program has been successfully assembled' + '\033[0m')