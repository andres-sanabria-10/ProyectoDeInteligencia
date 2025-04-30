import spacy 
from spacy.util import minibatch
from spacy.training.example import Example
import random
import os
from pymongo import MongoClient

# CREAR UN MODELO VACÍO PARA ESPAÑOL
nlp = spacy.blank("es")

# Añadir el componente NER manualmente
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

# Función para limpiar datos
def clean_text(text):
    if not text:
        return ""
    return text.strip()

# Preparar los datos de entrenamiento
training_data = []

for item in data:
    nombre_cientifico = clean_text(item.get("NombreCientifico", ""))
    nombre_comun = clean_text(item.get("NombreComun", ""))
    
    if nombre_cientifico:
        contexts = [
            f"Observamos un {nombre_cientifico} en su hábitat natural.",
            f"Durante la expedición, vimos al {nombre_cientifico}.",
            f"El {nombre_cientifico} es un animal fascinante.",
            f"Encontramos un ejemplar de {nombre_cientifico} en el bosque.",
            f"En el zoológico, vimos al {nombre_cientifico} descansando."
        ]
        for context in contexts:
            start_idx = context.find(nombre_cientifico)
            end_idx = start_idx + len(nombre_cientifico)
            training_data.append((context, {"entities": [(start_idx, end_idx, LABEL)]}))
            
            context_lower = context.lower()
            nombre_cientifico_lower = nombre_cientifico.lower()
            start_idx_lower = context_lower.find(nombre_cientifico_lower)
            end_idx_lower = start_idx_lower + len(nombre_cientifico_lower)
            training_data.append((context_lower, {"entities": [(start_idx_lower, end_idx_lower, LABEL)]}))

    
    if nombre_comun:
        # Separar múltiples nombres comunes por comas
        nombres_comunes = [nombre.strip() for nombre in nombre_comun.split(',')]

        for nombre in nombres_comunes:
            contexts = [
                f"Observamos un {nombre} en su hábitat natural.",
                f"Durante la expedición, vimos al {nombre}.",
                f"El {nombre} es un animal fascinante.",
                f"Encontramos un ejemplar de {nombre} en el bosque.",
                f"En el zoológico, vimos al {nombre} descansando."
            ]
            for context in contexts:
                start_idx = context.find(nombre)
                end_idx = start_idx + len(nombre)
                training_data.append((context, {"entities": [(start_idx, end_idx, LABEL)]}))
                
                context_lower = context.lower()
                nombre_lower = nombre.lower()  # <- Aquí está el cambio
                start_idx_lower = context_lower.find(nombre_lower)
                end_idx_lower = start_idx_lower + len(nombre_lower)
                training_data.append((context_lower, {"entities": [(start_idx_lower, end_idx_lower, LABEL)]}))


# Agregar ejemplos negativos
negative_examples = [
    ("Hoy fue un día soleado en la ciudad.", {"entities": []}),
    ("Los árboles y las flores embellecen el paisaje.", {"entities": []}),
    ("El automóvil rojo pasó rápidamente por la avenida.", {"entities": []}),
    ("En la biblioteca encontramos muchos libros interesantes.", {"entities": []}),
    ("La lluvia caía suavemente sobre el techo.", {"entities": []})
]

training_data.extend(negative_examples)

print(f"Total de ejemplos de entrenamiento: {len(training_data)}")

# Entrenar el modelo
optimizer = nlp.begin_training()
n_iter = 30
batch_size = 8

losses = {}
with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != "ner"]):
    for i in range(n_iter):
        random.shuffle(training_data)
        batches = minibatch(training_data, size=batch_size)
        batch_losses = {}
        
        for batch in batches:
            texts, annotations = zip(*batch)
            examples = [Example.from_dict(nlp.make_doc(text), ann) for text, ann in zip(texts, annotations)]
            nlp.update(examples, drop=0.2, sgd=optimizer, losses=batch_losses)
        
        for k, v in batch_losses.items():
            losses.setdefault(k, []).append(v)
        
        print(f"Iteración {i+1}/{n_iter} - Pérdida: {batch_losses}")

# Guardar el modelo
model_path = "./animal_ner_model"
if os.path.exists(model_path):
    print("Aviso: El modelo anterior será sobrescrito.")
nlp.to_disk(model_path)
print(f"Modelo guardado exitosamente en '{model_path}'")