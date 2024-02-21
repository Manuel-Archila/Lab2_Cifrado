from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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
        if letter == '=':
            break
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

def prepare_key(binary_word, key):
    if len(binary_word) > len(key):
        diff = len(binary_word) - len(key)
        for i in range(diff):
            key = key + key[i % len(key)]
    return key
    
# Funcion que realiza la operacion xor entre dos listas de binarios
def _xor(binary1, binary2):
    result = ''
    for i in range(len(binary1)):
        # print(i)
        if binary1[i] == binary2[i]:
            result += '0'
        else:
            result += '1'
    result_list = [result[i:i+8] for i in range(0, len(result), 8)]
    
    return result_list
# Funcion para completar la palabra con un comodin
def completar_palabra(palabra, longitud_objetivo, comodin):
    caracteres_faltantes = longitud_objetivo - len(palabra)
    palabra_completada = palabra + (comodin * caracteres_faltantes)
    
    return palabra_completada

# Función para leer la imagen como bytes
def read_image_as_bytes(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

# Función para guardar los bytes resultantes como imagen
def save_bytes_as_image(bytes_data, output_path):
    with open(output_path, 'wb') as image_file:
        image_file.write(bytes_data)

def xor_bytes(data_bytes, key):
    key_bytes = key.encode() 
    xor_result = bytearray()

    for i in range(len(data_bytes)):
        xor_result.append(data_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return bytes(xor_result)

def apply_xor_to_images(image_path1, image_path2):
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)
    img1.show()
    img2.show()

    if img1.size != img2.size:
        print('Las imágenes no tienen el mismo tamaño')
        return
    
    array1 = np.array(img1)
    array2 = np.array(img2)
    
    result_array = np.bitwise_xor(array1, array2)

    result_img = Image.fromarray(result_array)
    result_img.save('resultado_xor.png')
    result_img.show()

def calcular_distribuciones(string, n):
    counts = {}
    for i in range(0, len(string) - n + 1):
        gram = string[i:i+n]
        if gram in counts:
            counts[gram] += 1
        else:
            counts[gram] = 1
    total = sum(counts.values())
    probabilities = {k: v / total for k, v in counts.items()}
    return probabilities

def show_histogram(data, title):
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values(), color='skyblue')
    plt.title(title)
    plt.ylabel('Probabilidad')
    plt.xlabel('Secuencia')
    plt.show()

print("--- Parte 5 ---")

binary1, binary2 =prepare_xor('hi', 'not')
resultado = _xor(binary1, binary2)
print(resultado)
binaries = []
for binary in resultado:
    binaries.append(binary2decimal(binary))

print(ascii2word(binaries))


print("--- Parte 6 ---")

from PIL import Image
import base64

with open('./imagen_xor.png', 'rb') as image_file:
    image_bytes = image_file.read()

image_base64_bytes = base64.b64encode(image_bytes)
image_base64_str = image_base64_bytes.decode('utf-8')

six_block_word = base642sixblockbinary(image_base64_str)
binary_word = sixblockbinary2binary(six_block_word)
binary_word = "".join(binary_word)

blocks = len(binary_word)/8

blocks = int(blocks)

#tomar una palabra y completarla a un largo consigo misma
key = completar_palabra("cifrados", blocks, "cifrados")
key = key[:blocks]


letters_ascii = word2ascii(key)
letters_binary_word1 = []
for letter in letters_ascii:
    letters_binary_word1.append(decimal2binary(letter))
llave = "".join(letters_binary_word1)

image_path = './imagen_xor.png'
key = 'cifrados'
output_path = 'imagen_xor_decoded.png'

image_bytes = read_image_as_bytes(image_path)

xor_result_bytes = xor_bytes(image_bytes, key)

save_bytes_as_image(xor_result_bytes, output_path)
print("Una de las complicaciones que se tuvieron al realizar el XOR fue que las imagenes tenia que tener el mismo tamaño para que la cantidad de bits a operar fuera la misma en ambas imagenes. Otra cosa que habia que tener el cuenta es que si las imagenes era a color o en blanco y negro. Esta ultima era bastante importante debido a que los colores le añaden otra dimension a los bits, hace que las imagenes no puedan ser operadas.")

print("--- Parte 7 ---")

print("Esto ocurre debido a que el XOR es una operación que se realiza bit a bit, al operar imagenes con texto no tienen las mismas dimensiones. Esto hace que el cambio en los bits de la imagen no sea el esperado. Causando la corrupción de la imagen.")

print("--- Parte 8 ---")

apply_xor_to_images('./imagen1.jpg','./imagen2.jpg')

print("--- Parte 9 ---")

string = "111011001011111100011110111010111101100001111001000000000101100010000000001010010110110010100110101000000100101011100011101100111101000001011101111111"

probabilities_bits = calcular_distribuciones(string, 1)

probabilities_bigrams = calcular_distribuciones(string, 2)

probabilities_trigrams = calcular_distribuciones(string, 3)

show_histogram(probabilities_bits, 'Distribución de Probabilidad de Bits')
show_histogram(probabilities_bigrams, 'Distribución de Probabilidad de Bigramas')
show_histogram(probabilities_trigrams, 'Distribución de Probabilidad de Trigramas')

print("Como se puede observar en las diferntes gráficas, para los bits tienen una frecuencia simila, esto indica una distribución equitativa de bits.")
print("En el caso de los bigramas, se puede observar que los bigramas 11 y 00 tienen una frecuencia mayor que los otros bigramas.")
print("En el caso de los trigramas, se puede observar que los trigramas 111 y 000 tienen una frecuencia mayor que los otros trigramas.")

print("Estos son útiles para visualizar y comprender la distribución de patrones en secuencias de bits, bigramas o trigramas, lo que puede ser valioso para el análisis de datos y la detección de patrones.")










