# Funcion que conviert de palabra a ascii
def word2ascii(word):
    ascii_letters = []
    for letter in word:
        ascii_letters.append(ord(letter))
    return ascii_letters

# Funcion que convierte de decimal a binario
def decimal2binary(decimal, length=8):
    binary = ''

    if decimal == 0:
        return '0'
    
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = decimal // 2
    
    if len(binary) < length:
        binary = '0' * (length - len(binary)) + binary
    return binary



# Funcion que convierte de binario a decimal
def binary2decimal(binary):
    decimal = 0
    for i in range(len(binary)):
        decimal += int(binary[i]) * 2 ** ((len(binary) - 1 - i))
    return decimal

# Funcion que convierte de ascii a palabra
def ascii2word(ascii_letters):
    word = ''
    for ascii_letter in ascii_letters:
        word += chr(ascii_letter)
    return word

# Funcion que convierte de binario de bloques de 8 a bloques de 6
def sixblockbinary(binaries):
    long_block = "".join(binaries)
    six_block = []
    for i in range(0, len(long_block), 6):
        six_block.append(long_block[i:i+6])
    
    for i in range(len(six_block)):
        if len(six_block[i]) < 6:
            six_block[i] = six_block[i] + '0' * (6 - len(six_block[i]))  
    return six_block

# Funcion que convierte de bloques de 6 a base64
def sixblockbinary2base64(six_block):
    base64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    base64_string = ''
    for block in six_block:
        base64_string += base64[binary2decimal(block)]
    return base64_string

# Funcion que convierte de base64 a bloques de 6
def base642sixblockbinary(base64_string):
    base64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    six_block = []
    for letter in base64_string:
        binary = decimal2binary(base64.index(letter), 6)
        six_block.append(binary)
    return six_block

# Funcion que convierte de bloques de 6 a binario de bloques de 8
def sixblockbinary2binary(six_block):
    long_block = "".join(six_block)
    binaries = []
    for i in range(0, len(long_block), 8):
        binaries.append(long_block[i:i+8])
    
    for i in range(len(binaries)):
        if len(binaries[i]) < 8:
            binaries[i] = binaries[i] + '0' * (8 - len(binaries[i]))
    return binaries

# Funcion que balancea las longitudes de la palabra y la clave y devuelve dos listas de binarios
def prepare_xor(word, key):
    if len(word) < len(key):
        diff = len(key) - len(word)
        word = word + '0' * diff
    elif len(word) > len(key):
        diff = len(word) - len(key)
        for i in range(diff):
            key = key + key[i % len(key)]
    
    ascii1 = word2ascii(word)
    ascii2 = word2ascii(key)
    binary1 = ''
    binary2 = ''
    for i in range(len(ascii1)):
        binary1 += decimal2binary(ascii1[i])
        binary2 += decimal2binary(ascii2[i])
    return binary1, binary2
    
# Funcion que realiza la operacion xor entre dos listas de binarios
def _xor(word, key):
    binary1, binary2 = prepare_xor(word, key)
    result = ''
    for i in range(len(binary1)):
        if binary1[i] == binary2[i]:
            result += '0'
        else:
            result += '1'
    result_list = [result[i:i+8] for i in range(0, len(result), 8)]
    
    return result_list

print("1. Caracteres a bytes")
word1 = 'ho'
print("Palabra:", word1)
letters_ascii = word2ascii(word1)
letters_binary_word1 = []
for letter in letters_ascii:
    letters_binary_word1.append(decimal2binary(letter))
palabra1 = "".join(letters_binary_word1)
print(palabra1)

word2 = 'caminar'
print("Palabra:", word2)
letters_ascii = word2ascii(word2)

letters_binary_word2 = []
for letter in letters_ascii:
    letters_binary_word2.append(decimal2binary(letter))
palabra2 = "".join(letters_binary_word2)
print(palabra2)

print()

print("2. Bytes a caracteres")
print("Palabra:", word1)
letters_from_binary = []
for binary in letters_binary_word1:
    letters_from_binary.append(binary2decimal(binary))
palabra1_ascii = ascii2word(letters_from_binary)
print(palabra1_ascii)

print("Palabra:", word2)
letters_from_binary = []
for binary in letters_binary_word2:
    letters_from_binary.append(binary2decimal(binary))
palabra2_ascii = ascii2word(letters_from_binary)
print(palabra2_ascii)

print()

print("3. Bytes a base64")
print("Palabra:", word1)
print("Cadena en bytes:", palabra1)
six_block_word1 = sixblockbinary(letters_binary_word1)
base64_word1 = sixblockbinary2base64(six_block_word1)
print(base64_word1)

print("Palabra:", word2)
print("Cadena en bytes:", palabra2)
six_block_word2 = sixblockbinary(letters_binary_word2)
base64_word2 = sixblockbinary2base64(six_block_word2)
print(base64_word2)

print()

print("4. Base64 a caracteres")
print("Palabra:", word1)
print("Cadena en base64:", base64_word1)
six_block_word1 = base642sixblockbinary(base64_word1)
binary_word1 = sixblockbinary2binary(six_block_word1)
letters_from_binary = []
for binary in binary_word1:
    letters_from_binary.append(binary2decimal(binary))
palabra1_ascii = ascii2word(letters_from_binary)
print(palabra1_ascii)

print("Palabra:", word2)
print("Cadena en base64:", base64_word2)
six_block_word2 = base642sixblockbinary(base64_word2)
binary_word2 = sixblockbinary2binary(six_block_word2)
letters_from_binary = []
for binary in binary_word2:
    letters_from_binary.append(binary2decimal(binary))
palabra2_ascii = ascii2word(letters_from_binary)
print(palabra2_ascii)





# binary1, binary2 =prepare_xor('hi', 'not')
# resultado = _xor('hi', 'not')
# print(resultado)
# binaries = []
# for binary in resultado:
#     binaries.append(binary2decimal(binary))

# print(ascii2word(binaries))


