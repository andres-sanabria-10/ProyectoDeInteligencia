from flask import Flask, request, jsonify
from flask_cors import CORS  
from Entrenamiento import find_animals  # <-- importar aquí

app = Flask(__name__)
CORS(app)

# --- ENDPOINT ---
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    entities = find_animals(text)
    return jsonify({"entities": entities})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
