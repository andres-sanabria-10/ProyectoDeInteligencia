from flask import Flask, request, jsonify
import spacy
from pymongo import MongoClient
from bson import ObjectId
import os

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
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Procesar el texto con el modelo entrenado
    doc = nlp(text)

    # Extraer entidades y buscar en MongoDB
    entities = []
    for ent in doc.ents:
        if ent.label_ == "ANIMAL":
            # Buscar primero por NombreCientifico
            animal_data = collection.find_one({"NombreCientifico": {"$regex": f"^{ent.text}$", "$options": "i"}})
            if not animal_data:
                # Buscar flexible por NombreComun
                animal_data = collection.find_one({"NombreComun": {"$regex": f".*{ent.text}.*", "$options": "i"}})

            if animal_data:
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
