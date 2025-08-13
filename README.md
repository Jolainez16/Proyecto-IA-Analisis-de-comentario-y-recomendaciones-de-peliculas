Analisis de comentarios y recomendacion de peliculas
Este proyecto implementa un detector de emociones que nos permitira clasificar los comentarios de la peliculas como positivos o negativos. Nos recomendara películas similares o diferentes según sea el comentario ingresado o nuestras preferencias personales de acuerdo con nuestra elección.

Caracteristicas
Analizar comentarios de películas y determinar si son positivos o negativos utilizando un modelo de análisis de sentimientos entrenado con TensorFlow (modelo_sentimientos_imdb.keras).
Generar recomendaciones de películas basadas en el sentimiento del comentario o en preferencias personales del usuario.
Mostrar comentarios reales de IMDb para cada película.

Requisitos
•  Python 3.x como lenguaje principal.
•  TensorFlow / TensorFlow Datasets para el análisis de sentimientos.
•  IMDbPy para obtener información y comentarios de IMDb.
•  requests para acceder a la API de OMDb y obtener detalles de películas.
•  Tkinter para la interfaz gráfica de usuario.
•  Uso de módulos estándar (random, subprocess, sys, font) para funciones internas y ejecución de scripts adicionales.

Uso
1.	Asegurarse de tener requirements.txt con:
tensorflow
tensorflow-datasets
requests
imdbpy
2.	Instalar todas las bibliotecas:
pip install -r requirements.txt

3️⃣ Verificar archivos importantes
Debes tener en la carpeta del proyecto:
•	modelo_sentimientos_imdb.keras → tu modelo entrenado.
•	vocabulario.txt → vocabulario usado por TextVectorization.
•	principal.py → script principal que ejecuta la interfaz.
•	interfaz_busqueda.py 
•	Analizar_sentimientos.py

4️⃣ Ejecutar la aplicación
1.	Desde la terminal, estando en la carpeta del proyecto:
python principal.py
2.	Se abrirá la interfaz gráfica de Tkinter.

5️⃣ Uso de la interfaz
Tener que encuenta que debido a que usamos el conjunto de datos Imdb_reviews los comentarios y películas se deben escribir en ingles para que este funcione correctamente
1.	Buscar película:
o	Escribe el nombre o término de la película en el campo de búsqueda.
o	Presiona Buscar.
o	Selecciona la película de la lista desplegable
2.	Analizar comentario:
o	Escribe tu comentario sobre la película en el área de texto.
o	Presiona Analizar Sentimiento.
3.	Elegir tipo de recomendación:
o	Sí: Recomendaciones basadas en tu comentario (sentimiento).
o	No: Recomendaciones basadas en tus preferencias personales (abre otra interfaz). Si te decides por esta opción deberás escribir nombre o termino de la película, puede seleccionar el genero de tu gusto, director o actor, esto ultimo se tomaran encuenta para mostrar las películas que te recomendara.
o	Cancelar: No mostrar recomendaciones.
4.	Ver resultados:
o	En el área de texto se mostrarán:
	Recomendaciones de películas (hasta 5).
	Comentarios reales de IMDb de la película seleccionada.
5.	Salir:
o	Presiona el botón Salir para cerrar la aplicación.

6️⃣ Consejos y buenas prácticas
•	Asegúrate de que tu API key de OMDb sea válida (es necesario tener acceso a internet), tener en cuenta a que tiene un numero limitado de usos diarios, una vez excedido no funcionara hasta el día siguiente.
•	Mantén el modelo y vocabulario en la misma carpeta que el script.
•	La primera ejecución puede tardar un poco en cargar TensorFlow y el modelo.
•	Para nuevas películas o comentarios, simplemente repite los pasos 1 a 4.

