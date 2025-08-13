import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import random

api_key = "c5f3ad7f"  # Cambia aquí por tu clave OMDb

# -----------------------------
# Funciones de búsqueda y filtrado
# -----------------------------
def buscar_peliculas(api_key, termino, genero=None, director=None, actor=None, max_paginas=5):
    url = "http://www.omdbapi.com/"
    resultados_filtrados = []

    if not termino:
        return []

    peliculas_posibles = []

    for pagina in range(1, max_paginas + 1):
        params = {"apikey": api_key, "type": "movie", "s": termino, "page": pagina}
        try:
            respuesta = requests.get(url, params=params, timeout=5)
            datos = respuesta.json()
        except:
            break

        if datos.get("Response") != "True":
            break

        peliculas_posibles.extend(datos.get("Search", []))

    for p in peliculas_posibles:
        params_detalle = {"apikey": api_key, "i": p["imdbID"], "plot": "short"}
        detalle = requests.get(url, params=params_detalle).json()

        cumple = True
        if genero and genero.lower() not in detalle.get("Genre", "").lower():
            cumple = False
        if director and director.lower() not in detalle.get("Director", "").lower():
            cumple = False
        if actor and actor.lower() not in detalle.get("Actors", "").lower():
            cumple = False

        if cumple:
            resultados_filtrados.append(detalle)

    return resultados_filtrados

def buscar_y_mostrar():
    termino = entry_termino.get().strip()
    genero = entry_genero.get().strip()
    director = entry_director.get().strip()
    actor = entry_actor.get().strip()

    if not termino:
        messagebox.showwarning("Aviso", "Por favor ingresa al menos un término de búsqueda.")
        return

    global peliculas
    peliculas = buscar_peliculas(api_key, termino, genero, director, actor)
    listbox_resultados.delete(0, tk.END)
    text_detalles.config(state=tk.NORMAL)
    text_detalles.delete("1.0", tk.END)
    text_detalles.config(state=tk.DISABLED)

    if peliculas:
        for p in peliculas:
            texto = f"{p['Title']} ({p['Year']})"
            listbox_resultados.insert(tk.END, texto)
    else:
        messagebox.showinfo("Resultados", "No se encontraron películas con esas preferencias.")

# -----------------------------
# Función de recomendaciones aleatorias
# -----------------------------
def mostrar_recomendaciones(pelicula_actual):
    genero = pelicula_actual.get("Genre", "").lower() if pelicula_actual.get("Genre") else ""
    director = pelicula_actual.get("Director", "").lower() if pelicula_actual.get("Director") else ""
    actor = pelicula_actual.get("Actors", "").lower() if pelicula_actual.get("Actors") else ""

    terminos_busqueda = []

    if genero:
        terminos_busqueda.append(genero.split(",")[0].strip())
    if director:
        terminos_busqueda.append(director.split(",")[0].strip())
    if actor:
        terminos_busqueda.append(actor.split(",")[0].strip())

    if not terminos_busqueda:
        terminos_busqueda = ["movie"]

    posibles_recomendadas = []
    vistos = set()
    vistos.add(pelicula_actual["imdbID"])

    for termino in terminos_busqueda:
        resultados = buscar_peliculas(api_key, termino=termino, max_paginas=2)
        for p in resultados:
            if p["imdbID"] not in vistos:
                cumple = False
                if any(g.strip() in p.get("Genre", "").lower() for g in genero.split(",")):
                    cumple = True
                if any(d.strip() in p.get("Director", "").lower() for d in director.split(",")):
                    cumple = True
                if any(a.strip() in p.get("Actors", "").lower() for a in actor.split(",")):
                    cumple = True
                if cumple:
                    posibles_recomendadas.append(p)

    if posibles_recomendadas:
        return random.sample(posibles_recomendadas, min(5, len(posibles_recomendadas)))
    else:
        return []

# -----------------------------
# Mostrar detalles y recomendaciones
# -----------------------------
def mostrar_detalles(event):
    seleccion = listbox_resultados.curselection()
    if not seleccion:
        return
    idx = seleccion[0]
    pelicula = peliculas[idx]

    detalles = (
        f"Título: {pelicula['Title']}\n"
        f"Año: {pelicula['Year']}\n"
        f"Género: {pelicula['Genre']}\n"
        f"Director: {pelicula['Director']}\n"
        f"Actores: {pelicula['Actors']}\n"
        f"Duración: {pelicula.get('Runtime', 'N/A')}\n"
        f"Clasificación: {pelicula.get('Rated', 'N/A')}\n"
        f"Sinopsis: {pelicula.get('Plot', 'N/A')}\n"
        f"IMDB Rating: {pelicula.get('imdbRating', 'N/A')}\n"
    )

    text_detalles.config(state=tk.NORMAL)
    text_detalles.delete("1.0", tk.END)
    text_detalles.insert(tk.END, detalles)

    recomendadas = mostrar_recomendaciones(pelicula)
    if recomendadas:
        texto_recom = "\nRecomendaciones similares:\n"
        for r in recomendadas:
            texto_recom += f"- {r['Title']} ({r['Year']})\n"
        text_detalles.insert(tk.END, texto_recom)

    text_detalles.config(state=tk.DISABLED)

def limpiar_campos():
    entry_termino.delete(0, tk.END)
    entry_genero.delete(0, tk.END)
    entry_director.delete(0, tk.END)
    entry_actor.delete(0, tk.END)
    listbox_resultados.delete(0, tk.END)
    text_detalles.config(state=tk.NORMAL)
    text_detalles.delete("1.0", tk.END)
    text_detalles.config(state=tk.DISABLED)

# -----------------------------
# Interfaz gráfica
# -----------------------------
root = tk.Tk()
root.title("Buscador de Películas con Recomendaciones Aleatorias")
root.geometry("900x650")
root.minsize(800, 600)

style = ttk.Style(root)
style.theme_use('clam')

fuente_normal = ("Helvetica", 11)

frame_entrada = ttk.Frame(root, padding=15)
frame_entrada.pack(pady=10, padx=15, fill='x')

ttk.Label(frame_entrada, text="Término búsqueda:", font=fuente_normal).grid(row=0, column=0, sticky="e", padx=5, pady=6)
entry_termino = ttk.Entry(frame_entrada, width=40, font=fuente_normal)
entry_termino.grid(row=0, column=1, padx=5, pady=6)

ttk.Label(frame_entrada, text="Género:", font=fuente_normal).grid(row=1, column=0, sticky="e", padx=5, pady=6)
entry_genero = ttk.Entry(frame_entrada, width=40, font=fuente_normal)
entry_genero.grid(row=1, column=1, padx=5, pady=6)

ttk.Label(frame_entrada, text="Director:", font=fuente_normal).grid(row=2, column=0, sticky="e", padx=5, pady=6)
entry_director = ttk.Entry(frame_entrada, width=40, font=fuente_normal)
entry_director.grid(row=2, column=1, padx=5, pady=6)

ttk.Label(frame_entrada, text="Actor:", font=fuente_normal).grid(row=3, column=0, sticky="e", padx=5, pady=6)
entry_actor = ttk.Entry(frame_entrada, width=40, font=fuente_normal)
entry_actor.grid(row=3, column=1, padx=5, pady=6)

btn_buscar = ttk.Button(frame_entrada, text="Buscar", command=buscar_y_mostrar)
btn_buscar.grid(row=4, column=0, columnspan=2, pady=12, sticky="we")

btn_limpiar = ttk.Button(frame_entrada, text="Limpiar", command=limpiar_campos)
btn_limpiar.grid(row=5, column=0, columnspan=2, pady=6, sticky="we")

# Botón Salir
btn_salir = ttk.Button(frame_entrada, text="Salir", command=root.destroy)
btn_salir.grid(row=6, column=0, columnspan=2, pady=6, sticky="we")

frame_resultados = ttk.Frame(root, padding=10)
frame_resultados.pack(fill='both', expand=True, padx=15, pady=10)

listbox_resultados = tk.Listbox(frame_resultados, font=fuente_normal, width=50, height=20)
listbox_resultados.pack(side='left', fill='both', expand=True)
listbox_resultados.bind('<<ListboxSelect>>', mostrar_detalles)

scrollbar = ttk.Scrollbar(frame_resultados, orient='vertical', command=listbox_resultados.yview)
scrollbar.pack(side='left', fill='y')
listbox_resultados.config(yscrollcommand=scrollbar.set)

text_detalles = tk.Text(frame_resultados, width=50, height=20, wrap='word', font=fuente_normal, state=tk.DISABLED)
text_detalles.pack(side='left', fill='both', expand=True, padx=(10,0))

root.mainloop()