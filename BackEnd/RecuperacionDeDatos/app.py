from flask import Flask, request, jsonify
import spacy
from spacy.training.example import Example
from pymongo import MongoClient
import os
from bson import ObjectId

# Inicializar Flask
app = Flask(__name__)

# Cargar el modelo entrenado de Spacy
model_path = "./animal_ner_model"
nlp = spacy.load(model_path)

# Conexión a MongoDB
client = MongoClient("mongodb+srv://andressanabria02:uL3Bgc9CCAHiOrgD@cluster0.p02ar.mongodb.net/projectInteligenceArtificial?retryWrites=true&w=majority&appName=Cluster0")
db = client["projectIntligenceArtificial"]
collection = db["information"]

# Función para convertir ObjectId a string
def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: objectid_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [objectid_to_str(i) for i in obj]
    return obj

@app.route('/predict', methods=['POST'])
def predict():
    # Obtener el texto enviado en el cuerpo de la solicitud
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Procesar el texto con el modelo entrenado
    doc = nlp(text)

    # Extraer las entidades y buscar información adicional en MongoDB
    entities = []
    for ent in doc.ents:
        if ent.label_ == "ANIMAL":
            animal_data = collection.find_one({"NombreCientifico": ent.text})
            if not animal_data:
                animal_data = collection.find_one({"NombreComun": ent.text})

            if animal_data:
                # Convertir ObjectId a string
                animal_data = objectid_to_str(animal_data)
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "data": animal_data
                })
            else:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "data": None
                })
    
    return jsonify({"entities": entities})

if __name__ == '__main__':
    app.run(debug=True)