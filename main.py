#main.py
import re
from text_cleaner import Parser
from interface import WordUpdaterGUI

TOKENS = {
    "EXP_MALA": ["mal", "desastre", "harto", "cansado", "cancelar", "malo", "mala", "malos", "malas", "malisimo", "malisima"],
    "EXP_BUENA": ["bien", "excelente", "satisfecho", "contento", "feliz", "bueno", "buena", "buenos", "buenas", "buenisimo", "buenisima"],
    "EXP_NEUTRA": [],
    "ATC_MALA": ["pesimo", "lento", "malo", "mala", "malos", "malas"],
    "ATC_BUENA": ["bueno", "rapido", "eficiente", "buena", "buenos", "buenas"],
    "ATC_NEUTRA": [],
    "SALUDO": ["buen dia", "buenas tardes", "buenas noches", "buenos dias"],
    "DESPEDIDA": ["hasta luego", "buen dia"],
    "IDENTIFICACION": ["documento", "cedula"],
    "CORTESIA": ["gracias", "por favor"]
}

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        return archivo.read()

def tokenizar(texto):
    patrones_compuestos = [frase for sublist in TOKENS.values() for frase in sublist if ' ' in frase]
    for frase in patrones_compuestos:
        texto = texto.lower().replace(frase, '_'.join(frase.split()))
    palabras = re.findall(r'\b\w+\b', texto)
    return palabras

def evaluar_atencion(palabras):
    puntuacion = 0
    malas = []
    buenas = []
    detalles = {
        "SALUDO": False,
        "DESPEDIDA": False,
        "IDENTIFICACION": False,
        "CORTESIA": 0
    }

    for palabra in palabras:
        palabra = palabra.replace('_', ' ')
        if palabra in TOKENS["ATC_MALA"]:
            malas.append(palabra)
        elif palabra in TOKENS["ATC_BUENA"]:
            buenas.append(palabra)
        for criterio, lista in TOKENS.items():
            if palabra in lista:
                if criterio in detalles:
                    if isinstance(detalles[criterio], bool):
                        detalles[criterio] = True
                    else:
                        detalles[criterio] += 1

    puntuacion += sum(1 for key, value in detalles.items() if isinstance(value, bool) and value)
    puntuacion += detalles["CORTESIA"]

    return puntuacion, malas, buenas, detalles

def evaluar_experiencia(palabras):
    puntuacion = 0
    malas = []
    buenas = []

    for palabra in palabras:
        palabra = palabra.replace('_', ' ')
        if palabra in TOKENS["EXP_MALA"]:
            puntuacion -= 1
            malas.append(palabra)
        elif palabra in TOKENS["EXP_BUENA"]:
            puntuacion += 1
            buenas.append(palabra)

    return puntuacion, malas, buenas

def actualizarToken(nombre_lista, valor):
    if nombre_lista in TOKENS:
        TOKENS[nombre_lista].append(valor)
    else:
        print(f"Error: La lista '{nombre_lista}' no existe en TOKENS.")

def obtener_palabras_neutras(palabras, palabras_malas, palabras_buenas):
    return [palabra.replace('_', ' ') for palabra in set(palabras) if palabra.replace('_', ' ') not in palabras_malas and palabra.replace('_', ' ') not in palabras_buenas]

def reevaluar_archivos():
    archivo_funcionario = 'funcionario.txt'
    archivo_cliente = 'cliente.txt'

    texto_funcionario = leer_archivo(archivo_funcionario)
    texto_cliente = leer_archivo(archivo_cliente)

    parser_funcionario = Parser(texto_funcionario)
    texto_funcionario_limpio = ' '.join(parser_funcionario.parse())

    parser_cliente = Parser(texto_cliente)
    texto_cliente_limpio = ' '.join(parser_cliente.parse())

    palabras_funcionario = tokenizar(texto_funcionario_limpio)
    palabras_cliente = tokenizar(texto_cliente_limpio)

    # Evaluación de experiencia de atención
    puntuacion_atencion, malas_funcionario, buenas_funcionario, detalles_atencion = evaluar_atencion(palabras_funcionario)

    # Evaluación de experiencia del cliente
    puntuacion_experiencia, malas_cliente, buenas_cliente = evaluar_experiencia(palabras_cliente)

    # Obtener palabras neutras de funcionario y cliente
    palabras_neutras_funcionario = obtener_palabras_neutras(palabras_funcionario, malas_funcionario, buenas_funcionario)
    palabras_neutras_cliente = obtener_palabras_neutras(palabras_cliente, malas_cliente, buenas_cliente)
    palabras_neutras = list(set(palabras_neutras_funcionario + palabras_neutras_cliente))

    # Mostrar resultados en la consola después de la reevaluación
    print("\nResultados después de la actualización:")
    print(f"Puntuación de Atención: {puntuacion_atencion}")
    print(f"Detalles de Atención: {detalles_atencion}")
    print(f"Palabras malas (Funcionario): {', '.join(malas_funcionario)}")
    print(f"Palabras buenas (Funcionario): {', '.join(buenas_funcionario)}")
    print(f"Puntuación de Experiencia del Cliente: {puntuacion_experiencia}")
    print(f"Palabras malas (Cliente): {', '.join(malas_cliente)}")
    print(f"Palabras buenas (Cliente): {', '.join(buenas_cliente)}")

def main():
    global TOKENS

    archivo_funcionario = 'funcionario.txt'
    archivo_cliente = 'cliente.txt'

    texto_funcionario = leer_archivo(archivo_funcionario)
    texto_cliente = leer_archivo(archivo_cliente)

    parser_funcionario = Parser(texto_funcionario)
    texto_funcionario_limpio = ' '.join(parser_funcionario.parse())
    print(texto_funcionario_limpio)
    parser_cliente = Parser(texto_cliente)
    texto_cliente_limpio = ' '.join(parser_cliente.parse())
    print(texto_cliente_limpio)

    palabras_funcionario = tokenizar(texto_funcionario_limpio)
    palabras_cliente = tokenizar(texto_cliente_limpio)

    # Evaluación inicial de experiencia de atención
    puntuacion_atencion, malas_funcionario, buenas_funcionario, detalles_atencion = evaluar_atencion(palabras_funcionario)

    # Evaluación inicial de experiencia del cliente
    puntuacion_experiencia, malas_cliente, buenas_cliente = evaluar_experiencia(palabras_cliente)

    # Obtener palabras neutras de funcionario y cliente
    palabras_neutras_funcionario = obtener_palabras_neutras(palabras_funcionario, malas_funcionario, buenas_funcionario)
    palabras_neutras_cliente = obtener_palabras_neutras(palabras_cliente, malas_cliente, buenas_cliente)
    palabras_neutras = list(set(palabras_neutras_funcionario + palabras_neutras_cliente))

    # Mostrar resultados iniciales en la consola
    print("Resultados Iniciales:")
    print(f"Puntuación de Atención: {puntuacion_atencion}")
    print(f"Detalles de Atención: {detalles_atencion}")
    print(f"Palabras malas (Funcionario): {', '.join(malas_funcionario)}")
    print(f"Palabras buenas (Funcionario): {', '.join(buenas_funcionario)}")
    print(f"Puntuación de Experiencia del Cliente: {puntuacion_experiencia}")
    print(f"Palabras malas (Cliente): {', '.join(malas_cliente)}")
    print(f"Palabras buenas (Cliente): {', '.join(buenas_cliente)}")

    # Crear la interfaz gráfica para actualizar palabras neutras
    gui = WordUpdaterGUI(palabras_neutras, actualizarToken, reevaluar_archivos)
    gui.mostrar()

if __name__ == "__main__":
    main()
