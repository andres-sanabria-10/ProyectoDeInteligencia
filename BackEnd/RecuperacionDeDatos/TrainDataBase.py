
from flask import Flask, request, jsonify
import spacy
from pymongo import MongoClient

# Inicializar Flask
app = Flask(__name__)

# Cargar el modelo es_core_news_lg
nlp = spacy.load("es_core_news_lg")

# Conexión a MongoDB Atlas
client = MongoClient('mongodb+srv://andressanabria02:uL3Bgc9CCAHiOrgD@cluster0.p02ar.mongodb.net/projectInteligenceArtificial?retryWrites=true&w=majority&appName=Cluster0')
db = client['projectInteligenceArtificial']
collection = db['information']

# Función para buscar animales en la base de datos
def buscar_animal(nombre):
    resultado = collection.find_one({"$or": [{"NombreCientifico": nombre}, {"NombreComun": nombre}]})
    return resultado

# Endpoint para procesar el texto y buscar información del animal
@app.route('/buscar-animal', methods=['POST'])
def buscar_animal_endpoint():
    # Obtener el texto enviado por el usuario
    data = request.json
    texto = data.get("texto", "")

    if not texto:
        return jsonify({"error": "No se proporcionó texto"}), 400

    # Procesar el texto con spaCy
    doc = nlp(texto)
    nombres_identificados = []

    for ent in doc.ents:
        # Asumimos que las entidades relevantes son nombres científicos o comunes
        nombres_identificados.append(ent.text)

    # Buscar información en la base de datos para cada nombre identificado
    resultados = []
    for nombre in nombres_identificados:
        animal_info = buscar_animal(nombre)
        if animal_info:
            resultados.append(animal_info)

    # Devolver los resultados al usuario
    return jsonify(resultados)

# Ejecutar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)