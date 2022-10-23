from sys import last_traceback


def limpiar(nombre, nombre_limpio):
    data = ""
    with open(nombre, "r") as archivo:
        for line in archivo.readlines():
            #sacar comentarios despues de "//" y remover espacios al principio y final de cada linea
            line = line.split("//")[0].strip()
            #agregar newline al final de cada linea si es que no lo tiene
            if line[-2:] != "\n" and "\n" not in line:
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
                #remover todos los espacios innecesarios y dejarlo como "nobre valor"
                vars.append(" ".join(line.split()))
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
                line.split(" ", 1)
                #agregar if line[0:3] in opcodes.keys()
                if line[0] in opcodes_keys:
                    instrucciones.append(line)
                else:
                    #si es un label
                    instrucciones.append([line[0], None])
            if "CODE:" in line:
                leer = True
    return instrucciones

nombre_programa = "programa_1.txt"
nombre_limpio = "limpio.txt"
limpiar(nombre_programa, nombre_limpio)

print(code(nombre_limpio))

def escribir(contador, ins):
    #transformar ins en bytearray
    #escribir en basys3 ins en contador
    return contador + 1

def decimalToBinary(decimal_value):
    binary_value = "{0:b}".format(int(decimal_value))
    return binary_value.zfill(16)

def hexadecimalToBinary(hexadecimal_value):
    binary_value =  "{0:08b}".format(int(hexadecimal_value, 16))
    return binary_value.zfill(16)

def procesar_valor(valor):
    last_char = valor[-1]
    if(last_char == "d"):
        return decimalToBinary(int(valor[:-1]))
    elif(last_char == "h"):
        return hexadecimalToBinary(int(valor[:-1]))
    else:
        return valor[:-1].zfill(16)
    
#VARIABLES
variables = data()
variables_dict = {} #llave el nombre de la variable y el valor es la direcciones
contador_variables = 0 #dir RAM en que empiezan a guardarse las variables

labels_dict = {} # key: label_name, value: direccion 

opcodes = {}

contador_instrucciones = 0

for nombre, valor in variables:
    valor = procesar_valor(valor)
    dir = contador_variables #convertir a binario de 16 bits
    contador_variables += 1
    lit = valor #convertir a binario de 16 bits
    #LIT Y DIR DEBEN SER DE 16 BITS!
    variables_dict[nombre] = dir #guardar en dict la direccion de la variable
    ins = opcodes["MOV A, Lit"]
    ins = lit + ins #MOV A, Lit CONCATENAR BITS
    contador_instrucciones = escribir(contador_instrucciones, ins) #escribir en ROM MOV A, Lit
    ins = opcodes["MOV (Dir), A"]
    ins = dir + ins #MOV (Dir), A CONCATENAR BITS
    contador_instrucciones = escribir(contador_instrucciones, ins) #escribir en ROM #MOV (Dir), A

instrucciones = code()

for comando, operandos in instrucciones:
    if comando != "POP" and comando != "PUSH" and comando != "RET":
        #caso que no sea label
        if operandos is not None:
            operandos = "".join(operandos.split())
            if "B,A" == operandos or  "A,B" == operandos:
                ins = comando + " " + operandos[0:2] + " " + operandos[3]
                ins = opcodes[ins]
                contador_instrucciones = escribir(contador_instrucciones, ins)
            elif "(" in operandos:
                #caso en que tengamos un (Dir)
                if "(B)" not in operandos:
                    operandos = operandos.split(",")
                    if "(" in operandos[0]:
                        operandos_temp = "(Dir), " + operandos[1] #operandos[1] es A o B
                        dir = variables_dict[operandos[0].strip("(").strip(")")]
                    else:
                        operandos_temp = operandos[0] + ", (Dir)" #operandos[0] es A o B
                        dir = variables_dict[operandos[1].strip("(").strip(")")]
                #caso en que tengamos (B)
                else:
                    operandos = operandos.split(",")
                    #caso que sea un lit el otro operando
                    if "A" not in operandos:
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
                ins = comando + operandos_temp
                ins = opcodes[ins]
                ins = dir + ins
                contador_instrucciones = escribir(contador_instrucciones, ins)
            else:
                #caso en que tengamos un lit
                operandos = operandos.split(",")
                #caso que sea A/B , Lir
                if "A" not in operandos[0] or "B" not in operandos[0]:
                    operandos_temp = "Lit, " + operandos[1]
                    lit = procesar_valor(operandos[0])
                #caso que sea Lit, A/B
                else:
                    operandos_temp = operandos[0] + ", Lit"
                    lit = procesar_valor(operandos[1])
                ins = comando + operandos_temp
                ins = opcodes[ins]
                contador_instrucciones = escribir(contador_instrucciones, ins)                     
        else:
            #caso que sea solo un label
            #direccion es contador_instruccion
            pass
    


