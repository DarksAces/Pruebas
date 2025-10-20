import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

# -------------------- Función para copiar al portapapeles --------------------
def copiar_a_portapapeles(label):
    texto = label.cget("text")
    if texto:
        ventana.clipboard_clear()
        ventana.clipboard_append(texto)
        ventana.update()
        messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles.")
    else:
        messagebox.showwarning("Vacío", "No hay contraseña para copiar.")

# -------------------- Modo 1: Rápido --------------------
def generar_password_rapido():
    try:
        longitud = int(entry_rapido_longitud.get())
        if longitud <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Introduce una longitud válida.")
        return

    caracteres = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    label_rapido_resultado.config(text=password)

# -------------------- Modo 2: Personalizado --------------------
def generar_password_personalizado():
    try:
        longitud = int(entry_longitud.get())
        if longitud <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Introduce una longitud válida.")
        return

    caracteres = ""
    if var_mayus.get(): caracteres += string.ascii_uppercase
    if var_minus.get(): caracteres += string.ascii_lowercase
    if var_num.get(): caracteres += string.digits
    if var_sym.get(): caracteres += string.punctuation

    if not caracteres:
        messagebox.showerror("Error", "Selecciona al menos un tipo de carácter.")
        return

    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    label_personalizado_resultado.config(text=password)

# -------------------- Modo 3: Similares --------------------
sustituciones = {'a': '@', 's': '$', 'o': '0', 'e': '3', 'i': '1', 'l': '!', 'b': '8', 't': '7'}

def generar_similar():
    try:
        longitud = int(entry_similar_longitud.get())
        if longitud <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Introduce una longitud válida.")
        return

    base_passwords = entry_base_password.get("1.0", tk.END).strip().splitlines()
    if not base_passwords:
        messagebox.showerror("Error", "Introduce al menos una contraseña base.")
        return

    resultado_final = []
    for base in base_passwords:
        modificada = ""
        for char in base:
            if char.lower() in sustituciones and var_sim_sust.get():
                modificada += sustituciones[char.lower()]
            else:
                modificada += char

        extra = ""
        chars = ""
        if var_sim_mayus.get(): chars += string.ascii_uppercase
        if var_sim_minus.get(): chars += string.ascii_lowercase
        if var_sim_num.get(): chars += string.digits
        if var_sim_sym.get(): chars += string.punctuation

        while len(modificada + extra) < longitud:
            extra += random.choice(chars) if chars else ''

        resultado = (modificada + extra)[:longitud]
        resultado_final.append(resultado)

    text_similar_resultado.delete("1.0", tk.END)
    text_similar_resultado.insert(tk.END, "\n".join(resultado_final))

def copiar_similares():
    texto = text_similar_resultado.get("1.0", tk.END).strip()
    if texto:
        ventana.clipboard_clear()
        ventana.clipboard_append(texto)
        ventana.update()
        messagebox.showinfo("Copiado", "Contraseñas copiadas al portapapeles.")
    else:
        messagebox.showwarning("Vacío", "No hay contraseñas para copiar.")

# -------------------- Interfaz gráfica --------------------
ventana = tk.Tk()
ventana.title("Generador de Contraseñas Seguras")
ventana.geometry("500x650")

notebook = ttk.Notebook(ventana)
notebook.pack(pady=10, expand=True)

# ---------- Pestaña 1: Rápido ----------
frame_rapido = ttk.Frame(notebook)
notebook.add(frame_rapido, text='Rápido')

tk.Label(frame_rapido, text="Longitud de la contraseña (por defecto 16):").pack()
entry_rapido_longitud = tk.Entry(frame_rapido)
entry_rapido_longitud.insert(0, "16")
entry_rapido_longitud.pack(pady=5)

tk.Label(frame_rapido, text="Contraseña generada:").pack(pady=5)
label_rapido_resultado = tk.Label(frame_rapido, font=("Consolas", 14))
label_rapido_resultado.pack(pady=5)

tk.Button(frame_rapido, text="Generar", command=generar_password_rapido).pack(pady=5)
tk.Button(frame_rapido, text="Copiar", command=lambda: copiar_a_portapapeles(label_rapido_resultado)).pack()

# ---------- Pestaña 2: Personalizado ----------
frame_personalizado = ttk.Frame(notebook)
notebook.add(frame_personalizado, text='Personalizado')

tk.Label(frame_personalizado, text="Longitud de la contraseña:").pack()
entry_longitud = tk.Entry(frame_personalizado)
entry_longitud.insert(0, "12")
entry_longitud.pack(pady=5)

var_mayus = tk.BooleanVar(value=True)
var_minus = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True)
var_sym = tk.BooleanVar(value=True)

tk.Checkbutton(frame_personalizado, text="Mayúsculas", variable=var_mayus).pack()
tk.Checkbutton(frame_personalizado, text="Minúsculas", variable=var_minus).pack()
tk.Checkbutton(frame_personalizado, text="Números", variable=var_num).pack()
tk.Checkbutton(frame_personalizado, text="Símbolos", variable=var_sym).pack()

tk.Button(frame_personalizado, text="Generar", command=generar_password_personalizado).pack(pady=5)
label_personalizado_resultado = tk.Label(frame_personalizado, font=("Consolas", 14))
label_personalizado_resultado.pack(pady=5)
tk.Button(frame_personalizado, text="Copiar", command=lambda: copiar_a_portapapeles(label_personalizado_resultado)).pack()

# ---------- Pestaña 3: Similares ----------
frame_similar = ttk.Frame(notebook)
notebook.add(frame_similar, text='Similares')

tk.Label(frame_similar, text="Introduce una o más contraseñas base (una por línea):").pack()
entry_base_password = tk.Text(frame_similar, width=30, height=5)
entry_base_password.pack(pady=5)

tk.Label(frame_similar, text="Longitud final deseada:").pack()
entry_similar_longitud = tk.Entry(frame_similar)
entry_similar_longitud.insert(0, "12")
entry_similar_longitud.pack(pady=5)

var_sim_sust = tk.BooleanVar(value=True)
var_sim_mayus = tk.BooleanVar(value=True)
var_sim_minus = tk.BooleanVar(value=True)
var_sim_num = tk.BooleanVar(value=True)
var_sim_sym = tk.BooleanVar(value=True)

tk.Checkbutton(frame_similar, text="Sustituir letras (a→@, s→$...)", variable=var_sim_sust).pack()
tk.Checkbutton(frame_similar, text="Añadir Mayúsculas", variable=var_sim_mayus).pack()
tk.Checkbutton(frame_similar, text="Añadir Minúsculas", variable=var_sim_minus).pack()
tk.Checkbutton(frame_similar, text="Añadir Números", variable=var_sim_num).pack()
tk.Checkbutton(frame_similar, text="Añadir Símbolos", variable=var_sim_sym).pack()

tk.Button(frame_similar, text="Generar Similares", command=generar_similar).pack(pady=5)

text_similar_resultado = tk.Text(frame_similar, height=5, font=("Consolas", 12))
text_similar_resultado.pack(pady=5)
tk.Button(frame_similar, text="Copiar", command=copiar_similares).pack()

ventana.mainloop()
