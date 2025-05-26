import os  # Para manejar rutas y archivos del sistema operativo
import re  # Expresiones regulares, lo usamos para detectar los números
from PIL import Image  # De Pillow, para abrir imágenes y trabajarlas
import pytesseract  # La joyita que hace magia OCR con las imágenes

# 📁 Carpeta donde están guardadas las capturas de pantalla del grupo de WhatsApp
CARPETA_IMAGENES = 'capturas_numeros_grupos'

# 🔍 Expresión regular que pesca los números de teléfono en formato internacional
# Ejemplos que detecta: +54 9 376 411 0177, +51 958-123-456, +56 9 8765 4321
REGEX_NUMERO = r'\+\d{1,3}\s?\d{1,4}[\s-]?\d{3,4}[\s-]?\d{3,4}'

# 📝 Archivo donde vamos a guardar los números que extraigamos, sin duplicados
ARCHIVO_SALIDA = 'numeros_extraidos.txt'


def extraer_numeros_imagen(ruta_imagen: str) -> list[str]:
    """
    🧠 Esta función se encarga de abrir una imagen, aplicarle OCR con pytesseract,
    y luego extraer los números de teléfono usando la expresión regular.
    """
    imagen = Image.open(ruta_imagen)  # Abrimos la imagen
    texto_extraido = pytesseract.image_to_string(imagen)  # OCR: de imagen a texto
    return re.findall(REGEX_NUMERO, texto_extraido)  # Buscamos todos los números que matcheen


def procesar_carpeta(carpeta: str):
    """
    📂 Esta función recorre todas las imágenes de una carpeta, una por una,
    aplica el OCR y extrae los números. Al final los guarda ordenaditos en un archivo.
    """
    numeros_extraidos = set()  # Usamos un set para evitar duplicados automáticamente
    
    # 🔄 Recorremos todos los archivos de la carpeta
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(('png', 'jpg', 'jpeg')):  # Nos aseguramos de que sean imágenes
            ruta = os.path.join(carpeta, archivo)  # Construimos la ruta completa
            print(f'📸 Procesando archivo: {archivo}')
            numeros = extraer_numeros_imagen(ruta)  # OCR + extracción con regex
            numeros_extraidos.update(numeros)  # Agregamos sin duplicados

    # 🧾 Guardamos los números en un archivo de texto, ordenados
    with open(ARCHIVO_SALIDA, 'w') as f:
        for numero in sorted(numeros_extraidos):
            f.write(numero.strip() + '\n')  # .strip() por si hay espacios extras

    print(f'✅ Extracción de números completa. Archivo guardado en: {ARCHIVO_SALIDA}')


# 🚀 Punto de entrada principal del script
if __name__ == '__main__':
    procesar_carpeta(CARPETA_IMAGENES)
