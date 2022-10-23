def decimalToBinary(decimal_value):
    binary_value = "{0:b}".format(int(decimal_value))
    return binary_value.zfill(16)

def hexadecimalToBinary(hexadecimal_value):
    binary_value =  "{0:08b}".format(int(hexadecimal_value, 16))
    return binary_value.zfill(16)

print(decimalToBinary("24"))
print(hexadecimalToBinary("1a"))
print("".join("a   sd".split()))