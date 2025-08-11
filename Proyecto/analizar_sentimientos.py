import tensorflow as tf

def cargar_vectorizador(ruta_vocab="vocabulario.txt", max_tokens=10000, seq_len=250):
    vectorize_layer = tf.keras.layers.TextVectorization(
        max_tokens=max_tokens,
        output_mode='int',
        output_sequence_length=seq_len
    )
    with open(ruta_vocab, "r", encoding="utf-8") as f:
        vocab = [line.strip() for line in f.readlines()]
    # Insertar tokens especiales al inicio en orden esperado
    vocab = ['', '[UNK]'] + vocab
    vectorize_layer.set_vocabulary(vocab)
    return vectorize_layer

# Cargar modelo y vectorizador
model = tf.keras.models.load_model("modelo_sentimientos_imdb.keras")
vectorize_layer = cargar_vectorizador()

# Función para predecir sentimiento
def predecir_sentimiento(texto):
    texto_tensor = tf.constant([texto])
    vectorizado = vectorize_layer(texto_tensor)
    prediccion = model(vectorizado)
    probabilidad = prediccion.numpy()[0][0]
    return probabilidad

# Ejemplo
if __name__ == "__main__":
    texto_prueba = "I really enjoyed this movie, it was fantastic!"
    prob = predecir_sentimiento(texto_prueba)
    print(f"Probabilidad de positivo: {prob:.4f}")