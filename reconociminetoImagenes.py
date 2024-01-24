import os
import csv
import traceback
import re
from PIL import Image
import pytesseract
from tkinter import Tk, filedialog

#IMPORTANTE dirigir donde se encuentra el ejecutable de tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# Array de palabras que no se toman en cuenta
palabrasIgnorar = ['BNB', 'Comprobante Electrónico', 'Transferencia interbancaria', 'Referencia:', 'Fecha de la transacción:',
                   'Hora de la transacción:', 'Nombre del originante:', 'Se debitó de su caja de ahorro:',
                   'Nombre del destinatario:', 'Banco destino:', '5e acreditó a la cuenta:', 'Se acreditó a la cuenta:',
                   'La suma de Bs.:', 'Bancarización:', 'Fecha de latransacción:', 'Se debitó de su caja de ahorro:',
                   'Nombre del destinatario:', 'Fecha de la', 'transacción:', 'Se debitó de su caja de', 'ahorro:',
                   'Nombre del', 'destinatario:']

# Esta función extrae texto de una imagen
def extraccionTextoImagen(rutaImagen):
    imagen = Image.open(rutaImagen)
    textoExtraido = pytesseract.image_to_string(imagen, lang='spa')

    # Ignorar palabras específicas usando expresiones regulares
    for palabra in palabrasIgnorar:
        textoExtraido = re.sub(r'\b' + re.escape(palabra) + r'\b', '', textoExtraido)

    return textoExtraido

# Crear una ventana de Tkinter para el cuadro de diálogo
root = Tk()
root.withdraw()  # Ocultar la ventana principal de Tkinter

# Mostrar el cuadro de diálogo para seleccionar un directorio
selected_directory = filedialog.askdirectory(title="Selecciona el directorio con las imágenes")

if not selected_directory:
    print("No se seleccionó ningún directorio. Saliendo.")
    exit()

# Palabras detectadas totales
palabras_detectadas_totales = []

try:
    # Carpeta de salida para el archivo CSV
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    directorio_salida = escritorio
    archivo_csv_salida = os.path.join(directorio_salida, 'palabras_detectadas.csv')

    print("-----------INICIO DE ESCANEO--------------")
    # Procesar cada imagen en la carpeta
    for imagen in os.listdir(selected_directory):
        if imagen.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            rutaImagen = os.path.join(selected_directory, imagen)

            # Llama a la función para extraer texto
            texto_extraido = extraccionTextoImagen(rutaImagen)

            # Agrupa las letras en palabras
            palabras_detectadas = ["".join(grupo) for grupo in texto_extraido.split()]

            # Extiende la lista de palabras detectadas
            palabras_detectadas_totales.extend(palabras_detectadas)

            # Imprime el nombre del archivo y el texto extraído
            print(f'Archivo: {imagen}\nTexto Extraído: {", ".join(palabras_detectadas)}\n{"-"*50}')

    print("-----------FINALIZACION DE ESCANEO---------")

    # Verificar si el archivo CSV ya existe y borrarlo
    if os.path.exists(archivo_csv_salida):
        os.remove(archivo_csv_salida)
        print(f'Archivo existente borrado: {archivo_csv_salida}')

    # Escribir en el archivo CSV con cada palabra en una celda separada
    with open(archivo_csv_salida, 'w', newline='', encoding='utf-8') as csvfile:
        escritor_csv = csv.writer(csvfile)

        # Escribir cada palabra en una celda separada
        for palabra in palabras_detectadas_totales:
            escritor_csv.writerow([palabra])

    print(f'Se ha creado el archivo CSV en: {archivo_csv_salida}')

except Exception as e:
    traceback.print_exc()
    print(f'Error: {str(e)}')

# Cerrar la ventana de Tkinter
root.destroy()
