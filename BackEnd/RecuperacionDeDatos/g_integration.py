import os
import google.generativeai as genai

# Configurar API key desde variable de entorno
genai.configure(api_key=os.getenv("G_API_KEY"))

# Crear modelo (usa el default si no especificas)
model = genai.GenerativeModel()

def enriquecer_texto(texto_base, contexto):
    prompt = f"""
Eres un experto en biodiversidad

Contexto: {contexto}
Texto base: {texto_base}

A partir del siguiente texto, genera un único párrafo explicativo con toda la información posible, sin introducciones ni preguntas iniciales, y que finalice con la frase: '¿Quieres conocer otro animal en peligro de extinción de Boyacá?'

"""
    response = model.generate_content(prompt)
    return response.text




def generar_retroalimentacion_motivadora(resultado, contexto):
    tipo = "positivo" if resultado else "constructivo"
    prompt = f"""
Eres un mentor motivador. Basándote en este contexto: {contexto}
Da un mensaje {tipo} para un estudiante que acaba de {'acertar' if resultado else 'equivocarse'} en la respuesta.
"""
    response = model.generate_content(prompt)
    return response.text


