from flask import Flask, request, jsonify
import spacy
from pymongo import MongoClient

# Inicializar Flask
app = Flask(__name__)

# Cargar el modelo entrenado
nlp = spacy.load("./animal_ner_model")

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
    data = request.json
    texto = data.get("texto", "")

    if not texto:
        return jsonify({"error": "No se proporcionó texto"}), 400

    doc = nlp(texto)
    nombres_identificados = [ent.text for ent in doc.ents if ent.label_ == "ANIMAL"]

    if not nombres_identificados:
        return jsonify({"mensaje": "No se encontraron entidades ANIMAL en el texto."}), 200

    resultados = []
    for nombre in nombres_identificados:
        animal_info = buscar_animal(nombre)
        if animal_info:
            resultados.append(animal_info)

    if not resultados:
        return jsonify({
            "mensaje": "Se encontraron entidades ANIMAL, pero no hay información en la base de datos.",
            "entidades_detectadas": nombres_identificados
        }), 200

    return jsonify(resultados), 200

# Ejecutar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
