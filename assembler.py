from instructions import opcodes
import sys
from iic2343 import Basys3

def limpiar(nombre, nombre_limpio):
    data = ""
    with open(nombre, "r") as archivo:
        for line in archivo.readlines():
            #sacar comentarios despues de "//" y remover espacios al principio y final de cada linea
            line = line.split("//")[0].strip()
            #agregar newline al final de cada linea si es que no lo tiene
            if"\n" not in line:
                line += "\n"
            if line != "\n":
                data += line
    with open(nombre_limpio, "w+") as archivo:
        archivo.write(data)

def data(nombre):
    vars = []
    with open(nombre, "r") as archivo:
        for line in archivo.readlines():
            #terminar de leer variables
            if "CODE:" in line:
                break
            #que no sea la linea DATA:
            if "DATA:" not in line:
                #remover todos los espacios innecesarios y dejarlo como "nombre valor"
                line = " ".join(line.split())
                #agregarlos como nombre, valor
                line = line.split(" ")
                if len(line) == 2:
                    vars.append(line)
    return vars

def code(nombre, opcodes_keys):
    instrucciones = []
    leer = False
    with open(nombre, "r") as archivo:
        for line in archivo.readlines():
            #que no sea la linea DATA:
            if leer:
                #remover todos los espacios innecesarios
                line = " ".join(line.split())
                line = line.split(" ", 1)
                #agregar if line[0:3] in opcodes.keys()
                if line[0] in opcodes_keys:
                    if line[0] != "RET":
                        instrucciones.append(line)
                    else:
                        instrucciones.append([line[0], line[0]])
                else:
                    #si es un label
                    instrucciones.append([line[0], None])
            if "CODE:" in line:
                leer = True
    return instrucciones

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def escribir(contador, ins, instrucciones_strings):
    #transformar ins en bytearray
    #escribir en basys3 ins en contador
    instrucciones_strings.append(ins)
    return contador + 1

def decimalToBinary(decimal_value):
    binary_value = "{0:b}".format(int(decimal_value))
    return binary_value.zfill(16)

def hexadecimalToBinary(hexadecimal_value):
    binary_value =  "{0:08b}".format(int(hexadecimal_value, 16))
    return binary_value.zfill(16)

def direct_value(value):
    try:
        int(value)
        return 
    except: 
        pass

def procesar_valor(valor):
    if isinstance(valor, str):
        if valor[-1] not in "dbh":
            valor = valor + "d"
    if isinstance(valor, int):
        valor = str(valor)+"d"
    last_char = valor[-1]
    if(last_char == "d"):
        return decimalToBinary(valor[:-1])
    elif(last_char == "h"):
        return hexadecimalToBinary(valor[:-1])
    else:
        return valor[:-1].zfill(16)
    
def main(*args):
    nombre_programa = sys.argv[1]
    nombre_limpio = sys.argv[2]
    limpiar(nombre_programa, nombre_limpio)

    opcodes_keys = []
    for op in opcodes.keys():
        op = op.split(" ")
        opcodes_keys.append(op[0])

    instrucciones_strings = []
    #VARIABLES
    variables = data(nombre_limpio)
    print("------- LISTA DE VARIABLES -------")
    print(variables)
    variables_dict = {} #llave el nombre de la variable y el valor es la direcciones
    contador_variables = 0 #dir RAM en que empiezan a guardarse las variables

    labels_dict = {} # key: label_name, value: direccion 

    #DICCIONARIOS GUARDAN INT (no en binario) CON DIRECCION DE VARIABLE O LABEL

    contador_instrucciones = 0
    if len(variables) > 0:
        for nombre, valor in variables:
            if valor[-1] not in "dbh":
                valor = valor + "d"
            valor = procesar_valor(valor)
            dir = contador_variables
            contador_variables += 1
            lit = valor
            variables_dict[nombre] = dir #guardar en dict la direccion de la variable
            ins = opcodes["MOV A, Lit"]
            ins = lit + ins #MOV A, Lit CONCATENAR BITS
            contador_instrucciones = escribir(contador_instrucciones, ins, instrucciones_strings) #escribir en ROM MOV A, Lit
            ins = opcodes["MOV (Dir), A"]
            ins = procesar_valor(dir) + ins #MOV (Dir), A CONCATENAR BITS
            contador_instrucciones = escribir(contador_instrucciones, ins, instrucciones_strings) #escribir en ROM #MOV (Dir), A

    instrucciones = code(nombre_limpio, opcodes_keys)
    if len(instrucciones) > 0:
        for comando, operandos in instrucciones:
            if comando != "POP" and comando != "RET":
                #caso que no sea label
                if operandos is not None:
                    operandos = "".join(operandos.split())
                    #caso en que no tengamos un (Dir) y si un A y/o B en operandos
                    if ("A" in operandos or "B" in operandos) and "(" not in operandos:
                        if "B,A" == operandos or  "A,B" == operandos:
                            operandos_temp = operandos[0:2] + " " + operandos[2]
                            dir = "0000000000000000"
                        #caso en que sea COMANDO A / B
                        elif ("B" in operandos or "A" in operandos) and "," not in operandos:
                            if "A" in operandos:
                                operandos_temp = "A"
                                dir = "0000000000000000"
                            else:
                                operandos_temp = "B"
                                dir = "0000000000000000"
                        #caso en que sea A/B, Lit / Lit, A/B
                        elif ("B" in operandos or "A" in operandos) and "," in operandos:
                            operandos = operandos.split(",")
                            if "A" in operandos[0] or "B" in operandos[0]:
                                operandos_temp = operandos[0] + ", Lit"
                                dir = procesar_valor(operandos[1])
                            else:
                                operandos_temp = "Lit, " + operandos[1]
                                dir = procesar_valor(operandos[0])
                        ins = comando + " " + operandos_temp
                        ins = dir + opcodes[ins]
                        contador_instrucciones = escribir(contador_instrucciones, ins, instrucciones_strings)
                    #caso en que tengamos un (Dir)
                    elif "(" in operandos:
                        #caso en que sea COMANDO ·, () / (), ·
                        if "," in operandos:
                            #caso en que tengamos (Dir)
                            if "(B)" not in operandos:
                                operandos = operandos.split(",")
                                if "(" in operandos[0]:
                                    operandos_temp = "(Dir), " + operandos[1] #operandos[1] es A o B
                                    #try except
                                    try:
                                        dir = procesar_valor(variables_dict[operandos[0].strip("(").strip(")")])
                                    except:
                                        dir = procesar_valor(operandos[0].strip("(").strip(")"))
                                else:
                                    operandos_temp = operandos[0] + ", (Dir)" #operandos[0] es A o B
                                    try:
                                        dir = procesar_valor(variables_dict[operandos[1].strip("(").strip(")")])
                                    except:
                                        dir = procesar_valor(operandos[1].strip("(").strip(")"))
                            #caso en que tengamos (B)
                            else:
                                operandos = operandos.split(",")
                                #caso que sea un lit el otro operando
                                if "A" not in operandos and "varA" not in operandos and "varB" not in operandos:
                                    if "(" in operandos[0]:
                                        dir = procesar_valor(operandos[1]) #en este caso dir es el literal
                                        operandos_temp = "(B), Lit"
                                    else:
                                        dir = procesar_valor(operandos[0]) #en este caso dir es el literal
                                        operandos_temp = "Lit, (B)"
                                #caso en que A sea el otro operando
                                else:
                                    if "(" in operandos[0]:
                                        operandos_temp = "(B), A"
                                        dir = "0000000000000000"
                                    else:
                                        operandos_temp = "A, (B)"
                                        dir = "0000000000000000"
                        #caso en que sea COMANDO ()
                        else:
                            if "B" in operandos:
                                operandos_temp = "(B)"
                                dir = "0000000000000000"
                            else:
                                operandos_temp = "(Dir)"
                                try:
                                    dir = procesar_valor(variables_dict[operandos.strip("(").strip(")")])
                                except:
                                    dir = procesar_valor(operandos.strip("(").strip(")"))
                        ins = comando + " " + operandos_temp
                        ins = opcodes[ins]
                        ins = dir + ins
                        contador_instrucciones = escribir(contador_instrucciones, ins, instrucciones_strings)
                    #caso en que sea solo COMANDO Lit / Ins
                    elif "A" not in operandos and "B" not in operandos and "," not in operandos:
                        #caso que no sea salto o CALL
                        if ("J" not in comando) and comando != "CALL":
                            operandos_temp = "Lit"
                            dir = procesar_valor(operandos)
                        else:
                            operandos_temp = "Ins"
                            try:
                                dir = procesar_valor(labels_dict[operandos])
                            except:
                                #ESTA DIRECCION ES PLACEHOLDER. UNA VEZ TERMINADO, reemplazar con dir del
                                #labels_dict[label]
                                dir = "LABEL;" + operandos + ";"
                        ins = comando + " " + operandos_temp
                        ins = opcodes[ins]
                        ins = dir + ins
                        contador_instrucciones = escribir(contador_instrucciones, ins, instrucciones_strings)                    
                #caso que sea solo un label
                else:
                    dir = contador_instrucciones
                    contador_instrucciones += 1
                    #direccion es contador_instruccion
                    labels_dict[comando.strip(":").strip()] = dir        
            #caso en que COMANDO requiera de dos instrucciones
            else:
                if comando == "POP":
                    operandos_temp = operandos
                    ins_temp = comando + " " + operandos_temp
                    ins_temp = opcodes[ins_temp]
                    dir = "0000000000000000"
                    for i in range(0,2):
                        ins = dir + ins_temp[i]
                        contador_instrucciones = escribir(contador_instrucciones, ins, instrucciones_strings)
                #caso en que sea RET
                else:
                    ins_temp = comando
                    ins_temp = opcodes[ins_temp]
                    dir = "0000000000000000"
                    for i in range(0,2):
                        ins = dir + ins_temp[i]
                        contador_instrucciones = escribir(contador_instrucciones, ins, instrucciones_strings)

    instrucciones_finales = []

    for instruccion in instrucciones_strings:
        if "LABEL" in instruccion:
            ins_temp = instruccion.split(";") #entrega ["LABEL", label, instruccion en bits]
            label = ins_temp[1]
            dir = procesar_valor(labels_dict[label])
            ins_temp = dir + ins_temp[2]
            instrucciones_finales.append(ins_temp)
        else:
            instrucciones_finales.append(instruccion)

    byte_array = []
    
    largo = 0
    arr = []
    print(instrucciones_finales)
    for inst in instrucciones_finales:
        string = inst
        arr = []
        for i in range(0,4):
            bits = string[-(36 - i*8) : -(36 - (i*8 + 8))]
            num = int(bits, 2)
            arr.append(num)
        bits = string[ : 4]
        num = int(bits, 2)
        arr.append(num)
        arr = arr[::-1]
        data_2 = bytearray(arr)
        byte_array.append(data_2)
    return(byte_array)
    # tiene tres ceros a la derecha
    #for bytee in byte_array:
        #print(''.join('{:08b}'.format(x) for x in bytearray(bytee)))


if __name__== "__main__":
  byte_arrays = main()
  instance = Basys3()
  instance.begin()
  i = 0
  for byte_arr in byte_arrays:
    instance.write(i , byte_arr)
    print(byte_arr)
  instance.end()