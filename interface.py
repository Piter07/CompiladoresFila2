import tkinter as tk
from tkinter import ttk

class WordUpdaterGUI:
    def __init__(self, palabras_neutras, actualizarToken, reevaluacion_func):
        self.palabras_neutras = palabras_neutras
        self.actualizarToken = actualizarToken
        self.reevaluacion_func = reevaluacion_func

        self.root = tk.Tk()
        self.root.title("Actualización de Palabras Neutras")

        self.word_frame = tk.Frame(self.root, padx=10, pady=10)
        self.word_frame.pack()

        self.label = tk.Label(self.word_frame, text="Seleccione una palabra para clasificar:")
        self.label.pack(pady=5)

        self.word_var = tk.StringVar()
        self.word_dropdown = ttk.Combobox(self.word_frame, textvariable=self.word_var, values=self.palabras_neutras)
        self.word_dropdown.pack(pady=5)

        self.option_var = tk.StringVar()
        self.option_var.set("Seleccionar categoría")
        self.option_menu = ttk.OptionMenu(self.word_frame, self.option_var, "Seleccionar categoría", "EXP_BUENA",
                                          "EXP_MALA", "ATC_BUENA", "ATC_MALA", "SALUDO", "DESPEDIDA", "IDENTIFICACION", "CORTESIA")
        self.option_menu.pack(pady=5)

        self.update_button = tk.Button(self.word_frame, text="Actualizar", command=self.actualizar_palabra)
        self.update_button.pack(pady=10)

        self.confirm_button = tk.Button(self.word_frame, text="Confirmar y cerrar", command=self.confirmar_y_cerrar)
        self.confirm_button.pack(pady=10)

    def actualizar_palabra(self):
        palabra = self.word_var.get()
        categoria = self.option_var.get()

        if palabra and categoria != "Seleccionar categoría":
            self.actualizarToken(categoria, palabra)
            print(f"Palabra '{palabra}' actualizada a la categoría '{categoria}'.")

    def confirmar_y_cerrar(self):
        # Llamar a la función de reevaluación configurada en main.py
        if self.reevaluacion_func:
            self.reevaluacion_func()

        # Cerrar la ventana después de confirmar
        self.root.destroy()

    def mostrar(self):
        self.root.mainloop()
