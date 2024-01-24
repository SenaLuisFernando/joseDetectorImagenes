import os
import csv
import traceback
from PIL import Image
import pytesseract


#Array de palabras que no se toman en cuenta
palabrasIgnorar = ['BNB','Comprobante Electrónico','Transferencia interbancaria','Referencia:','Fecha de la transacción:','Hora de la transacción:','Nombre del originante:','Se debitó de su caja de ahorro:',
                   'Nombre del destinatario:','Banco destino:','5e acreditó a la cuenta:','Se acreditó a la cuenta:','La suma de Bs.:','Bancarización:','Fecha de latransacción:',
                   'Se debitó de su caja de ahorro:','Nombre del destinatario:','Fecha de la','transacción:','Se debitó de su caja de','ahorro:','Nombre del','destinatario:']
# Esta función extrae texto de una imagen
def extraccionTextoImagen(rutaImagen):
    imagen = Image.open(rutaImagen)
    textoExtraido = pytesseract.image_to_string(imagen, lang='spa')
    # Ignorar palabras específicas
    for palabra in palabrasIgnorar:
        textoExtraido = textoExtraido.replace(palabra, '')
    return textoExtraido

# Ubicación de la carpeta
rutaCarpetaJose = '~/Downloads/ImagenesJose/'
rutaExpandida = os.path.expanduser(rutaCarpetaJose)
archivosDeCarpeta = os.listdir(rutaExpandida)
palabras_detectadas_totales = []
try:
    # Filtrar archivos solo por la extensión de imágenes para evitar errores
    imagenesFiltradas = [archivo for archivo in archivosDeCarpeta if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    print("-----------INICIO DE ESCANEO--------------")
    # Procesar cada imagen en la carpeta
    for imagen in imagenesFiltradas:
        rutaImagen = os.path.join(rutaExpandida, imagen)
        # Llama a la función para extraer texto
        texto_extraido = extraccionTextoImagen(rutaImagen)
        # Agrupa las letras en palabras
        palabras_detectadas = ["".join(grupo) for grupo in texto_extraido.split()]
        # Extiende la lista de palabras detectadas
        palabras_detectadas_totales.extend(palabras_detectadas)
        # Imprime el nombre del archivo y el texto extraído
    print(f'Archivo: {imagen}\nTexto Extraído: {", ".join(palabras_detectadas)}\n{"-"*50}')

    print("-----------FINALIZACION DE ESCANEO---------")

    # GUARDADO de las palabras detectadas en un archivo CSV
    directorio_salida = '/home/luis/Documents' 
    archivo_csv_salida = os.path.join(directorio_salida, 'palabras_detectadas.csv')

    # Verificar si el archivo ya existe y borrarlo
    if os.path.exists(archivo_csv_salida):
        os.remove(archivo_csv_salida)
        print(f'Archivo existente borrado: {archivo_csv_salida}')

    # Separar la cadena en palabras y eliminar cadenas vacías
    palabras_detectadas_totales = [palabra.strip() for texto_extraido in palabras_detectadas_totales for palabra in texto_extraido.split()]

    # Escribir en el archivo CSV con cada palabra en una celda separada
    with open(archivo_csv_salida, 'w', newline='', encoding='utf-8') as csvfile:
        escritor_csv = csv.writer(csvfile)
        # Escribir cada palabra en una celda separada
        escritor_csv.writerow(palabras_detectadas_totales)

    print(f'Se ha creado el archivo CSV en: {archivo_csv_salida}')


except Exception as e:
    traceback.print_exc()
