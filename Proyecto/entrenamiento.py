import tensorflow as tf
import tensorflow_datasets as tfds

# Parámetros
max_features = 10000
sequence_length = 250
epochs = 5

# 1. Cargar y preparar el dataset
(train_data, test_data), info = tfds.load(
    "imdb_reviews",
    split=(tfds.Split.TRAIN, tfds.Split.TEST),
    as_supervised=True,
    with_info=True)

# Crear la capa de vectorización y adaptarla
vectorize_layer = tf.keras.layers.TextVectorization(
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

train_text = train_data.map(lambda text, label: text)
vectorize_layer.adapt(train_text)

# Función para vectorizar texto y etiquetas
def vectorize_text(text, label):
    return vectorize_layer(text), label

# Aplicar vectorización y batching
train_data = train_data.map(vectorize_text).shuffle(10000).batch(32).prefetch(tf.data.AUTOTUNE)
test_data = test_data.map(vectorize_text).batch(32).prefetch(tf.data.AUTOTUNE)

# 2. Construir y compilar el modelo
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(max_features + 1, 16),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 3. Entrenar el modelo
model.fit(train_data, epochs=epochs, validation_data=test_data)

# 4. Guardar el modelo
model.save("modelo_sentimientos_imdb.keras")

# 5. Guardar vocabulario limpio (sin tokens especiales)
vocab = vectorize_layer.get_vocabulary()
vocab_limpio = [w for w in vocab if w not in ['', '[UNK]']]  # eliminar tokens especiales
with open("vocabulario.txt", "w", encoding="utf-8") as f:
    for word in vocab_limpio:
        f.write(word + "\n")