from flask import Flask, request, jsonify
from flask_cors import CORS  
from Entrenamiento import find_animals
import random

app = Flask(__name__)
CORS(app)

# Preguntas
preguntas = [
    {
        "id": 1,
        "pregunta": "¿Dónde crees que el {ANIMAL} debería vivir para estar seguro?",
        "opciones": ["En zonas protegidas", "En zonas urbanas", "En zonas contaminadas"],
        "respuesta_correcta": 0,
        "explicacion": "El {ANIMAL} necesita un hábitat seguro para sobrevivir.",
    },
    {
        "id": 2,
        "pregunta": "¿Qué harías para reducir la contaminación en el hábitat del {ANIMAL}?",
        "opciones": ["Realizar campañas de limpieza", "Ignorar el problema", "Construir fábricas cercanas"],
        "respuesta_correcta": 0,
        "explicacion": "Reducir la contaminación ayuda a preservar la vida del {ANIMAL}.",
    },
    {
        "id": 3,
        "pregunta": "¿Por qué es importante conservar al {ANIMAL}?",
        "opciones": ["Porque es parte del ecosistema", "Porque no tiene importancia", "Porque molesta"],
        "respuesta_correcta": 0,
        "explicacion": "Cada especie cumple un rol fundamental en el ecosistema.",
    },
    {
        "id": 4,
        "pregunta": "¿Cuál es una acción para proteger al {ANIMAL} de la extinción?",
        "opciones": ["Crear reservas naturales", "Cazar indiscriminadamente", "Ignorar su situación"],
        "respuesta_correcta": 0,
        "explicacion": "Las reservas naturales ofrecen un refugio seguro para la conservación del {ANIMAL}.",
    },
    {
        "id": 5,
        "pregunta": "¿Cómo afecta la contaminación al {ANIMAL}?",
        "opciones": ["Provoca enfermedades y reduce su población", "No afecta en nada", "Mejora su entorno"],
        "respuesta_correcta": 0,
        "explicacion": "La contaminación provoca daños en la salud del {ANIMAL} y amenaza su supervivencia.",
    },
    {
        "id": 6,
        "pregunta": "¿Por qué es importante respetar el hábitat natural del {ANIMAL}?",
        "opciones": ["Porque es vital para su supervivencia", "Porque no tiene importancia", "Porque puede adaptarse a cualquier lugar"],
        "respuesta_correcta": 0,
        "explicacion": "El hábitat natural provee alimento, refugio y condiciones ideales para el {ANIMAL}.",
    },
    {
        "id": 7,
        "pregunta": "¿Qué deberías hacer si encuentras un {ANIMAL} herido?",
        "opciones": ["Buscar ayuda profesional y no molestar", "Ignorar y alejarse", "Intentar cazarlo"],
        "respuesta_correcta": 0,
        "explicacion": "Ayudar con profesionales garantiza el cuidado adecuado para la recuperación del {ANIMAL}.",
    },
    {
        "id": 8,
        "pregunta": "¿Qué impacto tiene la deforestación en el {ANIMAL}?",
        "opciones": ["Destruye su hogar y reduce su población", "No tiene ningún impacto", "Mejora su calidad de vida"],
        "respuesta_correcta": 0,
        "explicacion": "La deforestación elimina el hábitat natural del {ANIMAL}, poniendo en riesgo su supervivencia.",
    },
    {
        "id": 9,
        "pregunta": "¿Cómo pueden las personas ayudar a proteger al {ANIMAL}?",
        "opciones": ["Apoyando programas de conservación", "Dañando su hábitat", "Cazándolo por deporte"],
        "respuesta_correcta": 0,
        "explicacion": "Participar en programas de conservación ayuda a proteger y preservar al {ANIMAL}.",
    },
    {
        "id": 10,
        "pregunta": "¿Qué rol cumple el {ANIMAL} en el ecosistema?",
        "opciones": ["Mantiene el equilibrio natural", "No tiene ningún rol", "Es perjudicial para otros animales"],
        "respuesta_correcta": 0,
        "explicacion": "El {ANIMAL} ayuda a mantener el equilibrio y la salud del ecosistema donde vive.",
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

@app.route('/predict', methods=['POST'])
def predict():
    global animal_detectado
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    entities = find_animals(text)
    if entities:
        animal_detectado = entities[0]

    return jsonify({"entities": entities})


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
