from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  
from Entrenamiento import find_animals
import random
from g_integration import enriquecer_texto, generar_retroalimentacion_motivadora


app = Flask(__name__)
CORS(app)

# Preguntas
preguntas = [
    {
        "id": 1,
        "pregunta": "¿Dónde crees que el {ANIMAL} debería vivir para estar seguro?",
        "opciones": [
            "En zonas protegidas", 
            "En zonas urbanas", 
            "En zonas contaminadas"],
        "respuesta_correcta": 0,
        "explicacion": "Este animal necesita un hábitat seguro para sobrevivir.",
    },
    {
        "id": 2,
        "pregunta": "¿Qué harías para reducir la contaminación en el hábitat del {ANIMAL}?",
        "opciones": [
            "Ignorar el problema", 
            "Realizar campañas de limpieza", 
            "Construir fábricas cercanas"],
        "respuesta_correcta": 1,
        "explicacion": "Reducir la contaminación ayuda a preservar la vida de este animal.",
    },
    {
        "id": 3,
        "pregunta": "¿Por qué es importante conservar al {ANIMAL}?",
        "opciones": [
            "Porque es parte del ecosistema y es un ser vivo que contribuye al ciclo de vida", 
            "Porque no tiene importancia en el ecosistema",
            "No se, no respondo"],
        "respuesta_correcta": 0,
        "explicacion": "Cada especie cumple un rol fundamental en el ecosistema.",
    },
    {
        "id": 4,
        "pregunta": "¿Cuál es una acción para proteger al {ANIMAL} de la extinción?",
        "opciones": [
            "Cazar indiscriminadamente", 
            "Ignorar su situación",
            "Crear reservas naturales"],
        "respuesta_correcta": 2,
        "explicacion": "Las reservas naturales ofrecen un refugio seguro para la conservación de este animal.",
    },
    {
        "id": 5,
        "pregunta": "¿Cómo afecta la contaminación al {ANIMAL}?",
        "opciones": [
            "Provoca enfermedades y reduce su población", 
            "No afecta en nada", 
            "Mejora su entorno"],
        "respuesta_correcta": 0,
        "explicacion": "La contaminación provoca daños en la salud de este animal y amenaza su supervivencia.",
    },
    {
        "id": 6,
        "pregunta": "¿Por qué es importante respetar el hábitat natural del {ANIMAL}?",
        "opciones": [
            "No es importante respetar el hábitat del animal ", 
            "Porque puede adaptarse a cualquier lugar",
            "Es vital para su supervivencia",],
        "respuesta_correcta": 2,
        "explicacion": "El hábitat natural provee alimento, refugio y condiciones ideales para este animal.",
    },
    {
        "id": 7,
        "pregunta": "¿Qué deberías hacer si encuentras un {ANIMAL} herido?",
        "opciones": [
            "Buscar ayuda profesional y no molestar al animal", 
            "Ignorar y alejarse",
            "Intentar cazarlo"],
        "respuesta_correcta": 0,
        "explicacion": "Ayudar con profesionales garantiza el cuidado adecuado para la recuperación de este animal.",
    },
    {
        "id": 8,
        "pregunta": "¿Qué impacto tiene la deforestación en el {ANIMAL}?",
        "opciones": [
            "No tiene ningún impacto", 
            "Destruye su hogar y reduce su población",
            "Mejora su calidad de vida"],
        "respuesta_correcta": 1,
        "explicacion": "La deforestación elimina el hábitat natural de este animal, poniendo en riesgo su supervivencia.",
    },
    {
        "id": 9,
        "pregunta": "¿Cómo pueden las personas ayudar a proteger al {ANIMAL}?",
        "opciones": [
            "Apoyando programas de conservación", 
            "Dañando su hábitat", 
            "Cazándolo por deporte"],
        "respuesta_correcta": 0,
        "explicacion": "Participar en programas de conservación ayuda a proteger y preservar a este animal.",
    },
    {
        "id": 10,
        "pregunta": "¿Qué rol cumple el {ANIMAL} en el ecosistema?",
        "opciones": [
            "Mantiene el equilibrio natural", 
            "No tiene ningún rol", 
            "Es perjudicial para otros animales"],
        "respuesta_correcta": 0,
        "explicacion": "Este animal ayuda a mantener el equilibrio y la salud del ecosistema donde vive.",
    },
    {
        "id": 11,
        "pregunta": "Si encuentras un área donde un {ANIMAL} vive pero está siendo afectada por basura, ¿qué harías?",
        "opciones": [
            "Ignorar el problema porque no es tu responsabilidad",
            "Usar esa área para construir un parque temático",
            "Organizar una limpieza comunitaria",
        ],
        "respuesta_correcta": 2,
        "explicacion": "Mantener limpio el hábitat ayuda a preservar las condiciones necesarias para la vida del animal.",
    },
    {
        "id": 12,
        "pregunta": "¿Cómo puedes ayudar a que un ecosistema se recupere después de un incendio forestal?",
        "opciones": [
            "Plantando árboles de especies exóticas sin control",
            "Apoyando la reforestación con especies nativas",
            "Dejando que la naturaleza haga todo sin intervención"
        ],
        "respuesta_correcta": 1,
        "explicacion": "La reforestación con especies nativas favorece la recuperación natural y el hábitat de los animales.",
    },
    {
        "id": 13,
        "pregunta": "¿Qué harías si ves a personas cazando ilegalmente a un {ANIMAL} en peligro de extinción?",
        "opciones": [
            "Reportar a las autoridades ambientales",
            "Unirse a la caza para no quedarse atrás",
            "Ignorar para evitar problemas"
        ],
        "respuesta_correcta": 0,
        "explicacion": "Reportar la caza ilegal ayuda a proteger a las especies en riesgo y preservar el ecosistema.",
    },
    {
        "id": 14,
        "pregunta": "¿Cuál es una medida efectiva para evitar que especies en peligro se extingan?",
        "opciones": [
            "Construir más carreteras en zonas de hábitat natural",
            "Crear corredores biológicos entre áreas protegidas",
            "Permitir la caza regulada sin supervisión"
        ],
        "respuesta_correcta": 1,
        "explicacion": "Los corredores biológicos permiten el movimiento y reproducción segura de las especies.",
    },
    {
        "id": 15,
        "pregunta": "Si un río en el hábitat del {ANIMAL} está contaminado, ¿qué acciones serían las mejores para proteger a la fauna?",
        "opciones": [
            "Impulsar programas para reducir vertidos contaminantes",
            "Aumentar el uso de pesticidas para eliminar plagas",
            "No hacer nada porque el río se limpia solo"
        ],
        "respuesta_correcta": 0,
        "explicacion": "Reducir la contaminación del agua es vital para la salud del ecosistema y de las especies que dependen de él.",
    },
    {
        "id": 16,
        "pregunta": "¿Por qué es importante que las comunidades locales participen en la conservación del {ANIMAL}?",
        "opciones": [
            "Porque solo los científicos pueden tomar decisiones",
            "Porque su participación garantiza el éxito de las acciones conservacionistas",
            "Porque no afecta a las comunidades"
        ],
        "respuesta_correcta": 1,
        "explicacion": "Las comunidades locales conocen el territorio y pueden apoyar activamente la conservación.",
    },
    {
        "id": 17,
        "pregunta": "Si una planta invasora amenaza el hábitat del {ANIMAL}, ¿qué deberías hacer?",
        "opciones": [
            "Plantar más de esa planta invasora para aprovecharla",
            "No hacer nada porque no afecta a largo plazo",
            "Participar en programas para eliminar la planta invasora",
        ],
        "respuesta_correcta": 2,
        "explicacion": "Eliminar especies invasoras ayuda a restaurar el equilibrio natural del ecosistema.",
    },
    {
        "id": 18,
        "pregunta": "¿Qué impacto tiene el cambio climático en el {ANIMAL} y su ecosistema?",
        "opciones": [
            "Provoca cambios en su hábitat que pueden reducir su supervivencia",
            "No tiene ningún impacto significativo",
            "Mejora las condiciones del hábitat"
        ],
        "respuesta_correcta": 0,
        "explicacion": "El cambio climático altera temperaturas y disponibilidad de recursos, afectando la vida de muchas especies.",
    },
    {
        "id": 19,
        "pregunta": "¿Qué harías para fomentar la educación ambiental sobre la conservación del {ANIMAL}?",
        "opciones": [
            "Ignorar el tema porque es aburrido",
            "Organizar talleres y charlas en escuelas y comunidades",
            "Promover información falsa para evitar preocupaciones"
        ],
        "respuesta_correcta": 1,
        "explicacion": "La educación ambiental sensibiliza y motiva a las personas a cuidar el medio ambiente y sus especies.",
    },
    {
        "id": 20,
        "pregunta": "Si un proyecto de desarrollo amenaza un ecosistema donde vive el {ANIMAL}, ¿qué deberías hacer?",
        "opciones": [
            "Promover evaluaciones de impacto ambiental y buscar alternativas",
            "Apoyar el proyecto sin importar las consecuencias",
            "Ignorar el problema porque no te afecta"
        ],
        "respuesta_correcta": 0,
        "explicacion": "Las evaluaciones ambientales buscan minimizar daños y proteger la biodiversidad.",
    }
]

# Q-learning parameters
Q = {}
alpha = 0.1
gamma = 0.9
epsilon = 0.2  # 20% de exploración

animal_detectado = None
estado_anterior = -1  # -1: primera pregunta; 0: última respuesta incorrecta; 1: última respuesta correcta
ultima_pregunta_id = None
intentos_usuario = {}

# Inicializar Q con claves de la forma (id_pregunta, estado_anterior, id_opcion)
for pregunta in preguntas:
    for estado in [-1, 0, 1]:
        for i in range(len(pregunta["opciones"])):
            Q[(pregunta["id"], estado, i)] = 1.0  # valor inicial

def seleccionar_pregunta():
    # Selecciona la pregunta con la mayor Q value para estado_anterior actual
    max_valor = float('-inf')
    preguntas_candidatas = []
    for p in preguntas:
        for i in range(len(p["opciones"])):
            val = Q.get((p["id"], estado_anterior, i), 0)
            if val > max_valor:
                max_valor = val
                preguntas_candidatas = [p]
            elif val == max_valor:
                if p not in preguntas_candidatas:
                    preguntas_candidatas.append(p)
    return random.choice(preguntas_candidatas)

def actualizar_Q(id_pregunta, estado_ant, id_opcion, recompensa):
    old_value = Q.get((id_pregunta, estado_ant, id_opcion), 0)
    Q[(id_pregunta, estado_ant, id_opcion)] = old_value + alpha * (recompensa - old_value)

# ENDPOINTS



@app.route("/pregunta", methods=["POST"])
def get_pregunta():
    global animal_detectado
    data = request.get_json()
    nombre_comun = data.get("nombre_comun") or (animal_detectado if isinstance(animal_detectado, str) else "el animal")

    pregunta = seleccionar_pregunta()

    pregunta_texto = pregunta["pregunta"].replace("{ANIMAL}", nombre_comun)
    opciones_texto = [op.replace("{ANIMAL}", nombre_comun) for op in pregunta["opciones"]]
    explicacion_texto = pregunta["explicacion"].replace("{ANIMAL}", nombre_comun)

    return jsonify({
        "id": pregunta["id"],
        "pregunta": pregunta_texto,
        "opciones": opciones_texto,
        "explicacion": explicacion_texto
    })


@app.route("/pregunta_siguiente", methods=["POST"])
def pregunta_siguiente():
    global ultima_pregunta_id, estado_anterior
    data = request.get_json()
    ultima_id = data.get("ultima_pregunta_id")
    estado_ant = data.get("estado_anterior", -1)  # default -1

    preguntas_filtradas = [p for p in preguntas if p["id"] != ultima_id]
    if not preguntas_filtradas:
        preguntas_filtradas = preguntas

    if random.random() < epsilon:
        # Exploración: pregunta aleatoria
        pregunta = random.choice(preguntas_filtradas)
    else:
        # Explotación: pregunta con max Q usando estado_ant
        pregunta = max(
            preguntas_filtradas,
            key=lambda p: max(Q.get((p["id"], estado_ant, i), 0) for i in range(len(p["opciones"])))
        )

    ultima_pregunta_id = pregunta["id"]
    nombre_comun = animal_detectado if isinstance(animal_detectado, str) else "el animal"

    pregunta_texto = pregunta["pregunta"].replace("{ANIMAL}", nombre_comun)
    opciones_texto = [op.replace("{ANIMAL}", nombre_comun) for op in pregunta["opciones"]]

    # Guardamos el estado anterior para la próxima pregunta
    estado_anterior = estado_ant

    return jsonify({
        "id": pregunta["id"],
        "pregunta": pregunta_texto,
        "opciones": opciones_texto
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    global animal_detectado, intentos_usuario, estado_anterior

    data = request.get_json()
    id_pregunta = data.get("pregunta_id")
    respuesta_usuario = data.get("respuesta_usuario")

    pregunta = next((p for p in preguntas if p["id"] == id_pregunta), None)
    if not pregunta:
        return jsonify({"error": "Pregunta no encontrada"}), 404

    intentos = intentos_usuario.get(id_pregunta, 0)
    es_correcta = respuesta_usuario == pregunta["respuesta_correcta"]

    nombre_comun = animal_detectado if isinstance(animal_detectado, str) else "el animal"
    explicacion = pregunta["explicacion"].replace("{ANIMAL}", nombre_comun)

    recompensa = 1 if es_correcta else -1
    actualizar_Q(id_pregunta, estado_anterior, respuesta_usuario, recompensa)

    # Actualizamos el estado_anterior para la próxima pregunta
    estado_anterior = 1 if es_correcta else 0

    if es_correcta:
        intentos_usuario.pop(id_pregunta, None)
        return jsonify({
            "correcto": True,
            "explicacion": explicacion
        })
    else:
        if intentos == 0:
            intentos_usuario[id_pregunta] = 1
            return jsonify({
                "correcto": False,
                "segunda_oportunidad": False,
                "respuesta_correcta": pregunta["opciones"][pregunta["respuesta_correcta"]],
                "explicacion": explicacion
            })
        else:
            intentos_usuario.pop(id_pregunta, None)
            return jsonify({
                "correcto": False,
                "segunda_oportunidad": False,
                "explicacion": explicacion,
                "respuesta_correcta": pregunta["opciones"][pregunta["respuesta_correcta"]] + ". "
            })


@app.route("/tabla_q", methods=["GET"])
def get_tabla_q():
    tabla_serializada = {}
    for clave, valor in Q.items():
        if len(clave) == 3:
            id_pregunta, estado_ant, indice_opcion = clave
            key_str = f"{id_pregunta}_{estado_ant}_{indice_opcion}"
        else:
            key_str = str(clave)
        tabla_serializada[key_str] = valor
    return jsonify(tabla_serializada)



import requests
import os
from datetime import datetime

# Patrones para detectar intenciones
PATRONES_IMAGEN = [
    "genera imagen", "generar imagen", "crea imagen", "crear imagen",
    "muestra imagen", "mostrar imagen", "crea foto", "crear foto",
    "genera foto", "generar foto", "imagen", "foto", "visual",
    "como se ve", "cómo se ve", "visualizar", "ver imagen"
]

PATRONES_TEXTO = [
    "información", "informacion", "info", "datos", "características",
    "caracteristicas", "detalles", "descripción", "descripcion",
    "quiero información", "quiero informacion", "dame información",
    "dame informacion", "explica", "cuéntame", "cuentame"
]

def detectar_intencion(texto):
    """
    Detecta si el usuario quiere texto, imagen o ambos
    Returns: 'texto', 'imagen', 'ambos'
    """
    texto_lower = texto.lower()
    
    quiere_imagen = any(patron in texto_lower for patron in PATRONES_IMAGEN)
    quiere_texto = any(patron in texto_lower for patron in PATRONES_TEXTO)
    
    if quiere_imagen and quiere_texto:
        return 'ambos'
    elif quiere_imagen:
        return 'imagen'
    elif quiere_texto:
        return 'texto'
    else:
        # Por defecto, si no se especifica, dar información
        return 'texto'

def generar_imagen_animal(animal_data, nombre_comun):
    """
    Genera imagen del animal usando Stability AI
    """
    try:
        # Construir prompt basado en los datos del animal
        caracteristicas = animal_data.get('Caracteristicas', '')
        habitat = animal_data.get('Habitat', '')
        
        prompt = f"""
        A detailed, photorealistic image of {nombre_comun}, a species from Colombia. 
        {caracteristicas if caracteristicas else ''}
        Natural habitat: {habitat if habitat else 'Colombian biodiversity'}
        High quality, National Geographic style, natural lighting, 
        wildlife photography, detailed textures, vibrant colors
        """
        
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/ultra",
            headers={
                "authorization": "Bearer sk-DFLxApGPeGMlMm4FSDiyloIEFxMUuXuLcbHaZdkKtizllwka",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": prompt.strip(),
                "output_format": "webp",
            },
        )
        
        if response.status_code == 200:
            # Generar nombre único para la imagen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{nombre_comun.replace(' ', '_')}_{timestamp}.webp"
            
            # Guardar imagen
            with open(filename, 'wb') as file:
                file.write(response.content)
            
            return {
                "success": True,
                "filename": filename,
                "message": "Imagen generada exitosamente"
            }
        else:
            return {
                "success": False,
                "error": "Error al generar imagen",
                "details": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": "Error en la generación de imagen",
            "details": str(e)
        }

@app.route('/predict', methods=['POST'])
def predict():
    global animal_detectado
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Detectar intención del usuario
    intencion = detectar_intencion(text)
    
    # Detectar animales en el texto
    entities = find_animals(text)
    
    response_data = {
        "intencion": intencion,
        "entities": []
    }
    
    if entities:
        for i, entity in enumerate(entities):
            entity_response = {
                "nombre": entity.get("text", ""),
                "label": entity.get("label", ""),
                "data": entity.get("data", {}),
                "texto_enriquecido": "",
                "imagen": None
            }
            
            if entity.get("data"):
                animal_data = entity["data"]
                nombre_cientifico = animal_data.get("NombreCientifico", "")
                nombre_comun = animal_data.get("NombreComun", "")
                
                # GENERAR TEXTO si se requiere
                if intencion in ['texto', 'ambos']:
                    texto_base = f"Información sobre {nombre_comun} ({nombre_cientifico})"
                    contexto_animal = f"""
                    Nombre científico: {nombre_cientifico}
                    Nombre común: {nombre_comun}
                    Características: {animal_data.get('Caracteristicas', '')}
                    Hábitat: {animal_data.get('Habitat', '')}
                    Estado de conservación: {animal_data.get('EstadoDeConservacion', '')}
                    Amenazas: {animal_data.get('Amenazas', '')}
                    Localidad: {animal_data.get('Localidad', '')}
                    """
                    entity_response["texto_enriquecido"] = enriquecer_texto(texto_base, contexto_animal)
                
                # GENERAR IMAGEN si se requiere
                if intencion in ['imagen', 'ambos']:
                    imagen_result = generar_imagen_animal(animal_data, nombre_comun)
                    entity_response["imagen"] = imagen_result
            
            response_data["entities"].append(entity_response)
        
        # Guardar el primer animal detectado para compatibilidad
        animal_detectado = entities[0]
    else:
        response_data["entities"].append({
            "nombre": None,
            "mensaje": "Lo siento, ese animal no se encuentra en nuestra base de datos.",
            "texto_enriquecido": "",
            "imagen": None
        })
    
    return jsonify(response_data)


@app.route('/imagen/<filename>')
def get_imagen(filename):
    """
    Endpoint para servir las imágenes generadas
    """
    try:
        # Verificar que el archivo existe
        if os.path.exists(filename):
            return send_file(filename, mimetype='image/webp')
        else:
            return jsonify({"error": "Imagen no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)







