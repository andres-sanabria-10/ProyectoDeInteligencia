import spacy
from spacy.util import minibatch
from spacy.training.example import Example
import random
import os
from pymongo import MongoClient

# Cargar el modelo base de spaCy
nlp = spacy.load("es_core_news_lg")

# Añadir o recuperar el componente NER
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Etiqueta personalizada
LABEL = "ANIMAL"
ner.add_label(LABEL)

# Conexión a MongoDB
client = MongoClient("mongodb+srv://andressanabria02:uL3Bgc9CCAHiOrgD@cluster0.p02ar.mongodb.net/projectInteligenceArtificial?retryWrites=true&w=majority&appName=Cluster0")
db = client["projectIntligenceArtificial"]
collection = db["information"]

# Obtener datos
data = list(collection.find({}, {"_id": 0, "NombreCientifico": 1, "NombreComun": 1}))
print("Datos obtenidos de la base de datos:")
for item in data:
    print(item)

# Preparar los datos de entrenamiento
# Preparar los datos de entrenamiento originales
training_data = []
for item in data:
    nombre_cientifico = item.get("NombreCientifico")
    nombre_comun = item.get("NombreComun")

    if nombre_cientifico:
        nombre_cientifico = nombre_cientifico.strip()  # Eliminar espacios innecesarios
        training_data.append((nombre_cientifico, {"entities": [(0, len(nombre_cientifico), LABEL)]}))

    if nombre_comun:
        nombre_comun = nombre_comun.strip()  # Eliminar espacios innecesarios
        training_data.append((nombre_comun, {"entities": [(0, len(nombre_comun), LABEL)]}))

print("Datos de entrenamiento originales:")
for text, annotations in training_data:
    print(f"Texto: '{text}', Anotacion: {annotations}")

# Función para agregar variaciones
def add_variations(training_data):
    variations = []
    for text, annotations in training_data:
        # Variación en minúsculas
        variations.append((text.lower(), {"entities": [(0, len(text), "ANIMAL")]}))
        # Variación en mayúsculas
        variations.append((text.upper(), {"entities": [(0, len(text), "ANIMAL")]}))

    return variations

# Agregar variaciones al conjunto de entrenamiento
training_data.extend(add_variations(training_data))

print("\nDatos de entrenamiento con variaciones:")
for text, annotations in training_data:
    print(f"Texto: '{text}', Anotacion: {annotations}")
    
# Verificar longitudes de texto
print("\nVerificando longitudes de las entidades:")
for text, annotations in training_data:
    print(f"Texto: '{text}' (Longitud: {len(text)})")
    for start, end, label in annotations["entities"]:
        entity_text = text[start:end]
        print(f" - Entidad: '{entity_text}' (Etiqueta: {label})")
        if len(entity_text) != end - start:
            print(f"   ERROR: La longitud de la entidad no coincide con el texto.")

# Configurar entrenamiento
optimizer = nlp.begin_training()
n_iter = 30  # Número de iteraciones
batch_size = 16

# Entrenar
with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != "ner"]):
    for i in range(n_iter):
        random.shuffle(training_data)
        losses = {}
        batches = minibatch(training_data, size=batch_size)
        for batch in batches:
            texts, annotations = zip(*batch)
            examples = [Example.from_dict(nlp.make_doc(text), ann) for text, ann in zip(texts, annotations)]
            nlp.update(examples, drop=0.2, sgd=optimizer, losses=losses)
        print(f"Iteración {i+1} - Pérdida: {losses}")

# Verifica si ya existe el modelo (para saber si se sobrescribe)
model_path = "./animal_ner_model"
if os.path.exists(model_path):
    print(" Aviso: El modelo anterior será sobrescrito.")

# Guardar el modelo
nlp.to_disk(model_path)
print(f" Modelo guardado exitosamente en '{model_path}'")

# Cargar y probar el modelo entrenado
print("\nCargando el modelo entrenado desde disco...")
nlp_trained = spacy.load(model_path)

# Frases de prueba
test_texts = [
    "Allobates juanii",
    "Panthera leo Allobates juanii de la selva.",
    "La jirafa es un animal muy alto.",
    "Giraffa camelopardalis es conocida por su cuello largo."
]

# Usar el modelo entrenado para reconocer entidades
for test_text in test_texts:
    print(f"\nProbando el texto: '{test_text}'")
    doc = nlp_trained(test_text)

    # Extraer las entidades reconocidas
    if not doc.ents:
        print(" - No se encontraron entidades.")
    else:
        for ent in doc.ents:
            print(f" - Entidad encontrada: '{ent.text}' (Etiqueta: {ent.label_})")

            # Consultar la base de datos para obtener más información
            if ent.label_ == "ANIMAL":
                animal_name = ent.text
                animal_data = collection.find_one({"NombreCientifico": animal_name})  # Buscar en MongoDB por nombre científico
                if animal_data:
                    print(f"   Datos del animal encontrados: {animal_data}")
                else:
                    print(f"   No se encontraron datos adicionales para: {animal_name}")