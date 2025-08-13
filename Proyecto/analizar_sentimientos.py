import tensorflow as tf

def cargar_vectorizador(ruta_vocab="vocabulario.txt", seq_len=250):
    # Cargar vocabulario
    with open(ruta_vocab, "r", encoding="utf-8") as f:
        vocab = [line.strip() for line in f.readlines()]

    # Filtrar tokens reservados que puedan quedar
    vocab_limpio = [w for w in vocab if w not in ['', '[UNK]']]

    # Crear TextVectorization con max_tokens >= tamaño del vocabulario limpio
    vectorize_layer = tf.keras.layers.TextVectorization(
        max_tokens=len(vocab_limpio) + 2,  # +2 para tokens reservados internos
        output_mode='int',
        output_sequence_length=seq_len
    )

    # Asignar vocabulario limpio
    vectorize_layer.set_vocabulary(vocab_limpio)

    return vectorize_layer

# Cargar modelo y vectorizador
model = tf.keras.models.load_model("modelo_sentimientos_imdb.keras")
vectorize_layer = cargar_vectorizador()

# Función para predecir sentimiento
def predecir_sentimiento(texto):
    texto_tensor = tf.constant([texto])
    vectorizado = vectorize_layer(texto_tensor)
    prediccion = model(vectorizado)
    # Solo devolver Positivo o Negativo
    return "Positivo" if prediccion.numpy()[0][0] > 0.5 else "Negativo"

# Ejemplo
if __name__ == "__main__":
    texto_prueba = "I really enjoyed this movie, it was fantastic!"
    resultado = predecir_sentimiento(texto_prueba)
    print(f"Resultado: {resultado}")