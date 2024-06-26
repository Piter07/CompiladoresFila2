# interface.py

import tkinter as tk
from tkinter import ttk

class WordUpdaterGUI:
    def __init__(self, palabras_neutras, puntuacion_atencion, detalles_atencion, puntuacion_experiencia, palabras_malas, palabras_buenas):
        self.palabras_neutras = palabras_neutras
        self.index = 0

        self.root = tk.Tk()
        self.root.title("Actualización de Palabras Neutras")

        # Frame para mostrar las puntuaciones y detalles
        self.info_frame = tk.Frame(self.root, padx=10, pady=10)
        self.info_frame.pack()

        self.mostrar_puntuaciones(puntuacion_atencion, detalles_atencion, puntuacion_experiencia, palabras_malas, palabras_buenas)

        # Frame para la clasificación de palabras neutras
        self.word_frame = tk.Frame(self.root, padx=10, pady=10)
        self.word_frame.pack()

        self.label = tk.Label(self.word_frame, text="Seleccione una palabra para clasificar:")
        self.label.pack(pady=5)

        self.word_var = tk.StringVar()
        self.word_dropdown = ttk.Combobox(self.word_frame, textvariable=self.word_var, values=self.palabras_neutras)
        self.word_dropdown.pack(pady=5)

        self.option_var = tk.StringVar()
        self.option_var.set("Seleccionar opción")
        self.option_menu = ttk.OptionMenu(self.word_frame, self.option_var, "Seleccionar opción", "Buena", "Mala")
        self.option_menu.pack(pady=5)

        self.update_button = tk.Button(self.word_frame, text="Actualizar", command=self.actualizar_palabra)
        self.update_button.pack(pady=10)

        self.root.mainloop()

    def mostrar_puntuaciones(self, puntuacion_atencion, detalles_atencion, puntuacion_experiencia, palabras_malas, palabras_buenas):
        atencion_label = tk.Label(self.info_frame, text=f"Puntuación de Atención: {puntuacion_atencion}")
        atencion_label.pack(anchor='w')

        detalles_label = tk.Label(self.info_frame, text=f"Detalles de Atención: {detalles_atencion}")
        detalles_label.pack(anchor='w')

        experiencia_label = tk.Label(self.info_frame, text=f"Puntuación de Experiencia: {puntuacion_experiencia}")
        experiencia_label.pack(anchor='w')

        malas_label = tk.Label(self.info_frame, text=f"Palabras Malas: {palabras_malas}")
        malas_label.pack(anchor='w')

        buenas_label = tk.Label(self.info_frame, text=f"Palabras Buenas: {palabras_buenas}")
        buenas_label.pack(anchor='w')

    def actualizar_palabra(self):
        palabra = self.word_var.get()
        opcion = self.option_var.get()

        if opcion == "Buena":
            TOKENS["EXP_BUENA"].append(palabra)
        elif opcion == "Mala":
            TOKENS["EXP_MALA"].append(palabra)

        self.index += 1
        if self.index < len(self.palabras_neutras):
            self.word_dropdown.set(self.palabras_neutras[self.index])
            self.option_var.set("Seleccionar opción")
        else:
            self.label.config(text="No hay más palabras neutras para clasificar.")
            self.word_dropdown.config(state=tk.DISABLED)
            self.option_menu.config(state=tk.DISABLED)
            self.update_button.config(state=tk.DISABLED)

# Ejemplo de uso (solo se ejecuta si se llama directamente desde este archivo)
if __name__ == "__main__":
    palabras_neutras = ["palabra1", "palabra2", "palabra3"]
    puntuacion_atencion = 3
    detalles_atencion = {"SALUDO": True, "DESPEDIDA": False, "IDENTIFICACION": True, "CORTESIA": 2}
    puntuacion_experiencia = 2
    palabras_malas = ["mala1", "mala2"]
    palabras_buenas = ["buena1", "buena2"]

    gui = WordUpdaterGUI(palabras_neutras, puntuacion_atencion, detalles_atencion, puntuacion_experiencia, palabras_malas, palabras_buenas)
