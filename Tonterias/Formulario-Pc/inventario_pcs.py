import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import csv

# Clase que maneja los formularios para cada PC
class PCFormulario:
    def __init__(self, root, numero_pcs):
        self.root = root  # Ventana principal de la app
        self.numero_pcs = numero_pcs  # Número de PCs a registrar
        self.entries = []  # Lista para almacenar los campos de cada formulario

        self.frame = tk.Frame(root)  # Crear un frame para organizar los elementos en la ventana
        self.frame.pack(padx=10, pady=10)

        self.crear_formularios()  # Llamar al método que crea los formularios

        # Botón para guardar los datos en un archivo CSV
        boton_guardar = tk.Button(self.frame, text="Guardar en CSV", command=self.guardar_csv)
        boton_guardar.grid(row=self.numero_pcs*8+1, column=0, columnspan=2, pady=10)

    # Crear los formularios para cada PC
    def crear_formularios(self):
        for i in range(self.numero_pcs):
            # Título del formulario para cada PC
            tk.Label(self.frame, text=f"PC #{i+1}", font=('Arial', 12, 'bold')).grid(row=i*8, column=0, columnspan=2, pady=(10, 0))

            # Crear los campos de entrada para cada PC
            nombre = self.crear_input("Nombre del PC:", i*8+1)
            modelo_pc = self.crear_combobox("Modelo PC:", i*8+2)
            modelo = self.crear_input("Fabricante/Modelo:", i*8+3)
            chipset = self.crear_input("Chipset:", i*8+4)
            doble_pantalla = self.crear_checkbox("¿Tiene doble pantalla?", i*8+5)
            ssd = self.crear_checkbox("¿Tiene SSD?", i*8+6)
            portatil = self.crear_checkbox("¿Es portátil?", i*8+7)
            observaciones = self.crear_input("Observaciones:", i*8+8)

            # Almacenar los campos creados en la lista entries
            self.entries.append((nombre, modelo_pc, modelo, chipset, doble_pantalla, ssd, portatil, observaciones))

    # Crear un campo de entrada de texto
    def crear_input(self, label_text, row):
        tk.Label(self.frame, text=label_text).grid(row=row, column=0, sticky='w')  # Etiqueta del campo
        entry = tk.Entry(self.frame, width=50)  # Campo de texto para introducir datos
        entry.grid(row=row, column=1, pady=2)
        return entry  # Devolver el campo para almacenarlo en la lista entries

    # Crear un checkbox para opciones booleanas
    def crear_checkbox(self, label_text, row):
        var = tk.IntVar()  # Variable que almacena el valor del checkbox (0 o 1)
        cb = tk.Checkbutton(self.frame, text=label_text, variable=var)  # Crear el checkbox
        cb.grid(row=row, column=0, columnspan=2, sticky='w')  # Colocar el checkbox en el formulario
        return var  # Devolver la variable para poder acceder a su valor

    # Crear un combobox para seleccionar entre opciones predefinidas
    def crear_combobox(self, label_text, row):
        tk.Label(self.frame, text=label_text).grid(row=row, column=0, sticky='w')  # Etiqueta para el combobox
        opciones = ["Fenix", "Fenix V2", "Estación"]  # Opciones para el combobox
        combo = ttk.Combobox(self.frame, values=opciones, state="readonly")  # Crear el combobox
        combo.grid(row=row, column=1, pady=2)  # Colocar el combobox en el formulario
        return combo  # Devolver el combobox

    # Guardar los datos en un archivo CSV
    def guardar_csv(self):
        # Cabecera de las columnas para el archivo CSV
        datos = [
            ["Nombre del PC", "Modelo PC", "Fabricante/Modelo", "Chipset", "Doble Pantalla", "SSD", "Portátil", "Observaciones"]
        ]

        # Recorrer todos los formularios y almacenar los datos
        for entry in self.entries:
            fila = [
                entry[0].get(),  # Nombre del PC
                entry[1].get(),  # Modelo PC
                entry[2].get(),  # Fabricante/Modelo
                entry[3].get(),  # Chipset
                "Sí" if entry[4].get() else "No",  # Doble Pantalla
                "Sí" if entry[5].get() else "No",  # SSD
                "Sí" if entry[6].get() else "No",  # Portátil
                entry[7].get()  # Observaciones
            ]
            datos.append(fila)  # Agregar la fila de datos al archivo

        # Guardar los datos en un archivo CSV
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            with open(archivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)  # Crear el escritor CSV
                writer.writerows(datos)  # Escribir todas las filas de datos
            messagebox.showinfo("Éxito", f"Datos guardados en {archivo}")  # Mostrar mensaje de éxito


# Clase principal que maneja la interfaz de inicio
class App:
    def __init__(self, root):
        self.root = root  # Ventana principal
        self.root.title("Inventario de PCs para Jira")  # Título de la ventana

        # Etiqueta para preguntar cuántos PCs registrar
        self.label = tk.Label(root, text="¿Cuántos PCs deseas registrar?")
        self.label.pack(pady=10)

        # Campo de entrada para el número de PCs
        self.entry_num = tk.Entry(root)
        self.entry_num.pack()

        # Botón para continuar con la creación de formularios
        self.boton = tk.Button(root, text="Continuar", command=self.continuar)
        self.boton.pack(pady=10)

    # Función para continuar después de ingresar el número de PCs
    def continuar(self):
        try:
            num = int(self.entry_num.get())  # Obtener el número de PCs ingresado
            if num <= 0:
                raise ValueError  # Validación para evitar valores negativos o cero
            self.label.destroy()  # Eliminar la etiqueta
            self.entry_num.destroy()  # Eliminar el campo de entrada
            self.boton.destroy()  # Eliminar el botón
            PCFormulario(self.root, num)  # Crear los formularios para los PCs
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un número válido.")  # Mostrar mensaje de error


# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
