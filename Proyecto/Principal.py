import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import random
import requests
import tensorflow as tf
from imdb import IMDb

# -----------------------------
# Configuración OMDb y modelo
# -----------------------------
api_key = "c5f3ad7f"
cache_generos = {}
cache_detalles = {}
ia = IMDb()

# -----------------------------
# Cargar modelo y vectorizador
# -----------------------------
def cargar_vectorizador(ruta_vocab="vocabulario.txt", seq_len=250):
    with open(ruta_vocab, "r", encoding="utf-8") as f:
        vocab = [line.strip() for line in f.readlines()]
    vocab_limpio = [w for w in vocab if w not in ['', '[UNK]']]
    vectorize_layer = tf.keras.layers.TextVectorization(
        max_tokens=len(vocab_limpio)+2,
        output_mode='int',
        output_sequence_length=seq_len
    )
    vectorize_layer.set_vocabulary(vocab_limpio)
    return vectorize_layer

model = tf.keras.models.load_model("modelo_sentimientos_imdb.keras")
vectorize_layer = cargar_vectorizador()

def analizar_sentimiento_real(comentario):
    texto_tensor = tf.constant([comentario])
    vectorizado = vectorize_layer(texto_tensor)
    prediccion = model(vectorizado)
    return "Positivo" if prediccion.numpy()[0][0] > 0.5 else "Negativo"

# -----------------------------
# Funciones OMDb
# -----------------------------
def obtener_detalle_pelicula(titulo):
    if titulo in cache_detalles:
        return cache_detalles[titulo]
    url = "http://www.omdbapi.com/"
    params = {"apikey": api_key, "t": titulo}
    resp = requests.get(url, params=params)
    data = resp.json()
    cache_detalles[titulo] = data
    return data

def buscar_peliculas_por_genero(gen):
    gen_clave = gen.lower()
    if gen_clave in cache_generos:
        return cache_generos[gen_clave]

    url = "http://www.omdbapi.com/"
    resultados = []
    keywords = ["love","war","night","day","man","woman","life","death","story"]
    for kw in keywords:
        params = {"apikey": api_key, "s": kw, "type":"movie"}
        resp = requests.get(url, params=params)
        data = resp.json()
        if data.get("Response") == "True":
            for movie in data.get("Search", []):
                title = movie.get("Title","")
                det = obtener_detalle_pelicula(title)
                genero = det.get("Genre","")
                year = det.get("Year","")
                if gen.lower() in genero.lower():
                    resultados.append(f"{title} ({year}) - Género: {genero}")
                if len(resultados) >= 50:
                    break
        if len(resultados) >= 50:
            break

    cache_generos[gen_clave] = resultados
    return resultados or ["Forrest Gump", "Inception", "The Matrix"]

def buscar_peliculas_diferentes(generos_excluir):
    resultados = []
    keywords = ["love","war","night","day","man","woman","life","death","story"]
    url = "http://www.omdbapi.com/"
    for kw in keywords:
        params = {"apikey": api_key, "s": kw, "type":"movie"}
        resp = requests.get(url, params=params)
        data = resp.json()
        if data.get("Response") == "True":
            for movie in data.get("Search", []):
                title = movie.get("Title","")
                det = obtener_detalle_pelicula(title)
                genero = det.get("Genre","")
                year = det.get("Year","")
                if not any(g.lower() in genero.lower() for g in generos_excluir):
                    resultados.append(f"{title} ({year}) - Género: {genero}")
                if len(resultados) >= 50:
                    break
        if len(resultados) >= 50:
            break
    return resultados or ["Gladiator", "La La Land", "Her"]

# -----------------------------
# Función para obtener comentarios IMDb
# -----------------------------
def obtener_comentarios_imdb(titulo, max_reviews=5):
    try:
        results = ia.search_movie(titulo)
        if not results:
            return ["No se encontraron comentarios en IMDb."]
        
        movie = results[0]
        ia.update(movie, 'reviews')
        reviews = movie.get('reviews', [])
        comentarios = [rev.get('content','') for rev in reviews[:max_reviews]]
        if not comentarios:
            return ["No hay comentarios disponibles."]
        return comentarios
    except Exception as e:
        return [f"Error al obtener comentarios: {e}"]

# -----------------------------
# Funciones de la interfaz
# -----------------------------
def buscar_peliculas_interfaz():
    termino = entry_busqueda.get().strip()
    if not termino:
        messagebox.showwarning("Advertencia", "Escribe un término de búsqueda.")
        return
    url = "http://www.omdbapi.com/"
    params = {"apikey": api_key, "s": termino, "type":"movie"}
    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo consultar la API: {e}")
        return

    peliculas = []
    if data.get("Response") == "True":
        for movie in data.get("Search", []):
            peliculas.append(f"{movie.get('Title','')} ({movie.get('Year','')})")

    combobox_peliculas['values'] = peliculas
    if peliculas:
        combobox_peliculas.current(0)

def analizar_comentario():
    pelicula = combobox_peliculas.get().strip()
    comentario = entry_comentario.get("1.0", tk.END).strip()

    if not pelicula or not comentario:
        messagebox.showwarning("Campos vacíos", "Por favor selecciona una película y escribe un comentario.")
        return

    sentimiento = analizar_sentimiento_real(comentario)
    messagebox.showinfo("Resultado del análisis", f"Sentimiento detectado: {sentimiento}")

    respuesta = messagebox.askyesnocancel(
        "Elegir tipo de recomendación",
        "¿Qué tipo de recomendación deseas?\n\n"
        "Sí: Basadas en tu comentario\n"
        "No: Basadas en tus preferencias personales\n"
        "Cancelar: Ninguna"
    )

    if respuesta is True:
        mostrar_recomendaciones(pelicula, comentario)
    elif respuesta is False:
        abrir_interfaz_busqueda()

def abrir_interfaz_busqueda():
    try:
        subprocess.Popen([sys.executable, "interfaz_busqueda.py"])
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'interfaz_busqueda.py'.")

# -----------------------------
# Mostrar recomendaciones y comentarios en la misma ventana
# -----------------------------
def mostrar_recomendaciones(pelicula_seleccionada, comentario):
    text_reco.config(state="normal")
    text_reco.delete("1.0", tk.END)

    sentimiento = analizar_sentimiento_real(comentario)
    titulo = pelicula_seleccionada.split(" (")[0]
    det = obtener_detalle_pelicula(titulo)
    generos = det.get("Genre","").split(",")

    if sentimiento == "Positivo":
        recomendaciones = buscar_peliculas_por_genero(generos[0])
    else:
        recomendaciones = buscar_peliculas_diferentes(generos)

    aleatorias = random.sample(recomendaciones, min(5, len(recomendaciones)))

    text_reco.insert(tk.END, "Recomendaciones:\n")
    for rec in aleatorias:
        text_reco.insert(tk.END, f"- {rec}\n")
    
    text_reco.insert(tk.END, "\nComentarios de IMDb:\n")
    comentarios_imdb = obtener_comentarios_imdb(titulo)
    for c in comentarios_imdb:
        text_reco.insert(tk.END, f"- {c}\n")
    
    text_reco.config(state="disabled")

# -----------------------------
# Interfaz gráfica
# -----------------------------
root = tk.Tk()
root.title("Analizador de Comentarios de Películas")
root.geometry("600x900")

frame = ttk.Frame(root, padding="10")
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Buscar película:").pack(anchor="w")
entry_busqueda = ttk.Entry(frame, width=50)
entry_busqueda.pack(pady=5)
btn_buscar = ttk.Button(frame, text="Buscar", command=buscar_peliculas_interfaz)
btn_buscar.pack(pady=5)

ttk.Label(frame, text="Selecciona la película:").pack(anchor="w")
combobox_peliculas = ttk.Combobox(frame, width=50, state="readonly")
combobox_peliculas.pack(pady=5)

ttk.Label(frame, text="Comentario:").pack(anchor="w")
entry_comentario = tk.Text(frame, width=50, height=6)
entry_comentario.pack(pady=5)

btn_analizar = ttk.Button(frame, text="Analizar Sentimiento", command=analizar_comentario)
btn_analizar.pack(pady=10)

# Botón Salir
btn_salir = ttk.Button(frame, text="Salir", command=root.destroy)
btn_salir.pack(pady=5)

ttk.Label(frame, text="Recomendaciones y comentarios IMDb:").pack(anchor="w")
text_reco = tk.Text(frame, width=70, height=20, state="disabled")
text_reco.pack(pady=5)

root.mainloop()
