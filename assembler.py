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

def code(nombre):
    instrucciones = []
    leer = False
    with open(nombre, "r") as archivo:
        for line in archivo.readlines():
            #que no sea la linea DATA:
            if leer:
                #remover todos los espacios innecesarios
                line = " ".join(line.split())
                #cambiar OR a ORR
                if line[0:2] == "OR":
                    line = line[0:2] + "R" + line[2:]
                #agregar if line[0:3] in opcodes.keys()
                instrucciones.append([line[0:3], line[3:]])
            if "CODE:" in line:
                leer = True
    return instrucciones

nombre_programa = "programa_1.txt"
nombre_limpio = "limpio.txt"
limpiar(nombre_programa, nombre_limpio)

print(code(nombre_limpio))

def escribir(contador, ins):
    #escribir en basys3 ins en contador
    return contador + 1

variables = data()
variables_dict = {}
contador_variables = 0 #dir RAM en que empiezan a guardarse las variables
opcodes = {}

contador_instrucciones = 0

for nombre, valor in variables:
    dir = contador_variables #convertir a binario de 16 bits
    contador_variables += 1
    lit = valor #convertir a binario de 16 bits
    #LIT Y DIR DEBEN SER DE 16 BITS!
    variables_dict[nombre] = dir #guardar en dict la direccion de la variable
    ins = opcodes["MOV A, Lit"]
    ins = lit + ins #MOV A, Lit
    contador_instrucciones = escribir(contador_instrucciones, ins) #escribir en ROM MOV A, Lit
    ins = opcodes["MOV (Dir), A"]
    ins = dir + ins #MOV (Dir), A
    contador_instrucciones = escribir(contador_instrucciones, ins) #escribir en ROM #MOV (Dir), A
    

