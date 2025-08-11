import tkinter as tk
from tkinter import ttk, messagebox
#import analisis  # Módulo para análisis de sentimientos (comentar hasta tenerlo listo)
import subprocess
import sys

def analizar_comentario():
    pelicula = entry_pelicula.get().strip()
    comentario = entry_comentario.get("1.0", tk.END).strip()

    if not pelicula or not comentario:
        messagebox.showwarning("Campos vacíos", "Por favor ingrese el nombre de la película y un comentario.")
        return

    # Llamada a función de análisis - comentada hasta tener módulo analisis.py
    # resultado = analisis.analizar_sentimiento(comentario)
    # Por ahora simulamos resultado
    resultado = "Positivo" if "buena" in comentario.lower() else "Negativo"

    messagebox.showinfo("Resultado del análisis", f"Sentimiento detectado: {resultado}")

    opcion = messagebox.askyesno("Recomendaciones", 
        "¿Quieres recomendaciones de películas basadas en tus preferencias personales?")
    
    if opcion:
        abrir_interfaz_busqueda()

def abrir_interfaz_busqueda():
    """Abre la otra interfaz en un proceso independiente."""
    try:
        subprocess.Popen([sys.executable, "interfaz_busqueda.py"])
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'interfaz_busqueda.py'.")

root = tk.Tk()
root.title("Analizador de Comentarios de Películas")
root.geometry("500x400")

frame = ttk.Frame(root, padding="10")
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Nombre de la película:").pack(anchor="w")
entry_pelicula = ttk.Entry(frame, width=50)
entry_pelicula.pack(pady=5)

ttk.Label(frame, text="Comentario:").pack(anchor="w")
entry_comentario = tk.Text(frame, width=50, height=6)
entry_comentario.pack(pady=5)

btn_analizar = ttk.Button(frame, text="Analizar Sentimiento", command=analizar_comentario)
btn_analizar.pack(pady=10)

root.mainloop()