import { useState } from "react"
import "../AnimalInfoForm.css"

const AnimalInfoForm = () => {
  const [animalInfo, setAnimalInfo] = useState("")
  const [speciesInfo, setSpeciesInfo] = useState("")
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")

  const handleSearch = () => {
    // Aquí puedes implementar la lógica de búsqueda
    console.log("Buscando información del animal:", animalInfo)
  }

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
          <div className="text-area-container large">
            <textarea
              value={speciesInfo}
              onChange={(e) => setSpeciesInfo(e.target.value)}
              className="species-textarea"
            />
            <div className="scrollbar">
              <div className="scrollbar-thumb"></div>
            </div>
          </div>
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
