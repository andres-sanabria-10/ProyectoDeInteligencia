# Entrenamiento.py

import spacy
from spacy.matcher import PhraseMatcher
from pymongo import MongoClient
from bson import ObjectId

# Preparación igual que antes
nlp = spacy.blank("es")

client = MongoClient("mongodb+srv://andressanabria02:uL3Bgc9CCAHiOrgD@cluster0.p02ar.mongodb.net/projectIntligenceArtificial?retryWrites=true&w=majority&appName=Cluster0")
db = client["projectIntligenceArtificial"]
collection = db["information"]

data = list(collection.find({}, {"_id": 0, "NombreCientifico": 1, "NombreComun": 1}))

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
nombres_animales = set()

patterns = []
for item in data:
    if "NombreCientifico" in item and item["NombreCientifico"]:
        nombre_cientifico = item["NombreCientifico"].strip()
        patterns.append(nlp.make_doc(nombre_cientifico))
        nombres_animales.add(nombre_cientifico.lower())
        
    if "NombreComun" in item and item["NombreComun"]:
        for nombre in item["NombreComun"].split(","):
            nombre = nombre.strip()
            if nombre:
                patterns.append(nlp.make_doc(nombre))
                nombres_animales.add(nombre.lower())

matcher.add("ANIMAL", patterns)

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: objectid_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [objectid_to_str(i) for i in obj]
    return obj

def find_animals(text):
    doc = nlp(text)
    matches = matcher(doc)
    entities = []

    for match_id, start, end in matches:
        span = doc[start:end]
        span_text = span.text.lower()

        if span_text in nombres_animales:
            animal_info = collection.find_one({
                "$or": [
                    {"NombreCientifico": {"$regex": f"^{span.text}$", "$options": "i"}},
                    {"NombreComun": {"$regex": f"(\\b{span.text}\\b)", "$options": "i"}}
                ]
            }, {"_id": 0})
            
            if animal_info:
                animal_info = objectid_to_str(animal_info)
                entities.append({
                    "text": span.text,
                    "label": "ANIMAL",
                    "data": animal_info
                })
            else:
                entities.append({
                    "text": span.text,
                    "label": "ANIMAL",
                    "data": None
                })

    return entities
