import { useState } from "react"
import "../AnimalInfoForm.css"

const AnimalInfoForm = () => {
  const [animalInfo, setAnimalInfo] = useState("")
  const [speciesInfo, setSpeciesInfo] = useState("")
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [speciesData, setSpeciesData] = useState([]);
  const [selectedAnimal, setSelectedAnimal] = useState(null);

  const handleSearch = async () => {
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          text: animalInfo // lo que escribió el usuario
        })
      });

      if (!response.ok) {
        throw new Error("Error en la conexión con el servidor");
      }

      const data = await response.json();

      // Guardar los resultados en estado para mostrarlos después
      setSpeciesData(data.entities || []);      // Limpiar el textarea de entrada
      setSpeciesInfo("");
    } catch (error) {
      console.error("Error al buscar:", error);
      alert("No se pudo obtener información del animal.");
    }
  };
  const handleSubmitAnswer = () => {
    // Aquí puedes implementar la lógica para enviar la respuesta
    console.log("Pregunta:", question)
    console.log("Respuesta:", answer)
  }

  return (
    <div className="animal-info-container">
      <div className="welcome-section">
        <p>Ingresa información relacionada con animales en peligro de extinción en Boyacá</p>
      </div>

      <div className="info-grid">
        {/* Columna izquierda */}
        <div className="info-column">
          <div className="info-box">
            <h2>Información</h2>
            <p className="info-subtitle">Ingrese el nombre o características del animal a buscar</p>

            <div className="text-area-container">
              <textarea
                value={animalInfo}
                onChange={(e) => setAnimalInfo(e.target.value)}
                placeholder="Ejemplo:
Gallito de Roca
Es de color rojo y negro
Tiene cresta
Es un ave"
                className="info-textarea"
              />
              <div className="scrollbar">
                <div className="scrollbar-thumb"></div>
              </div>
            </div>

            <button className="search-button" onClick={handleSearch}>
              BUSCAR
            </button>
          </div>
        </div>

        {/* Columna derecha */}
        <div className="image-column">
          <div className="image-placeholder">
            <div className="mountain-shape"></div>
            <div className="circle-shape"></div>
          </div>
        </div>
      </div>

      <hr className="divider" />

      <div className="bottom-grid">
        {/* Información de la especie */}
        <div className="species-info">
          <h2>Información de la especie</h2>
          {speciesData.length > 0 ? (
            <div className="species-checkboxes">
              {speciesData.map((item, index) => {
                const animal = item.data;

                if (!animal) {
                  return (
                    <div key={index} className="form-check">
                      <label className="form-check-label" style={{ color: '#a00' }}>
                        No se encontró información para "{item.text}"
                      </label>
                    </div>
                  );
                }

                return (
                  <div key={animal._id} className="form-check">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id={`animal-${animal._id}`}
                      onChange={() => setSelectedAnimal(animal)}
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`animal-${animal._id}`}
                      style={{ color: '#0c0c0c', fontWeight: 'bold' }}
                    >
                      {animal.NombreCientifico} ({animal._id})
                    </label>
                  </div>
                );
              })}

            </div>
          ) : (
            <div className="text-area-container large">
              <textarea
                value={selectedAnimal ? JSON.stringify(selectedAnimal, null, 2) : speciesInfo}
                onChange={(e) => setSpeciesInfo(e.target.value)}
                className="species-textarea"
                placeholder="Aquí puedes ingresar información adicional..."
              />
              <div className="scrollbar">
                <div className="scrollbar-thumb"></div>
              </div>
            </div>
          )}
        </div>

        {/* Preservación del ecosistema */}
        <div className="ecosystem-preservation">
          <h2>Preservación del ecosistema</h2>

          <div className="input-group">
            <label>Preguntas</label>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="question-input"
            />
          </div>

          <div className="input-group">
            <label>Respuesta</label>
            <input type="text" value={answer} onChange={(e) => setAnswer(e.target.value)} className="answer-input" />
          </div>

          <button className="submit-button" onClick={handleSubmitAnswer}>
            <span className="arrow-icon">→</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default AnimalInfoForm
