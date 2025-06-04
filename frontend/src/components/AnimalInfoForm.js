import { useState, useEffect } from "react"
import "../AnimalInfoForm.css"
import ReactMarkdown from "react-markdown";

const AnimalInfoForm = () => {
  const [animalInfo, setAnimalInfo] = useState("")
  const [speciesInfo, setSpeciesInfo] = useState("")
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [speciesData, setSpeciesData] = useState([]);
  const [selectedAnimal, setSelectedAnimal] = useState(null);

  // Estados para preguntas y respuestas
  const [pregunta, setPregunta] = useState(null);
  const [respuestaSeleccionada, setRespuestaSeleccionada] = useState(null);
  const [resultado, setResultado] = useState(null);
  const [ultimaPreguntaId, setUltimaPreguntaId] = useState(null);

  const handleSearch = async () => {
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          text: animalInfo
        })
      });

      if (!response.ok) {
        throw new Error("Error en la conexión con el servidor");
      }

      const data = await response.json();
      
      // DEBUGGING - Imprimir toda la respuesta
      console.log("=== RESPUESTA COMPLETA DEL SERVIDOR ===");
      console.log(data);
      
      // DEBUGGING - Imprimir solo las entities
      console.log("=== ENTITIES ===");
      console.log(data.entities);
      
      // DEBUGGING - Imprimir cada entity individualmente
      if (data.entities && data.entities.length > 0) {
        data.entities.forEach((entity, index) => {
          console.log(`=== ENTITY ${index} ===`);
          console.log("Entity completa:", entity);
          console.log("Entity.data:", entity.data);
          console.log("texto_enriquecido:", entity.texto_enriquecido);
        });
      }

      // Guardar los resultados en estado para mostrarlos después
      setSpeciesData(data.entities || []);
      // Limpiar el textarea de entrada
      setSpeciesInfo("");
      setSelectedAnimal(null);
      setPregunta(null);
      setRespuestaSeleccionada(null);
      setResultado(null);

    } catch (error) {
      console.error("Error al buscar:", error);
      alert("No se pudo obtener información del animal.");
    }
  };

  // Cuando cambias el animal seleccionado, traemos la pregunta
  useEffect(() => {
    if (selectedAnimal) {
      obtenerPregunta(selectedAnimal.data?.NombreComun || selectedAnimal.data?.NombreCientifico);
    }
  }, [selectedAnimal]);

  // Obtiene una pregunta del backend según el nombre común del animal
  const obtenerPregunta = async (nombreComun) => {
    try {
      const res = await fetch("http://localhost:5000/pregunta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre_comun: nombreComun }),
      });
      const data = await res.json();
      setPregunta(data);
      setRespuestaSeleccionada(null);
      setResultado(null);
      setUltimaPreguntaId(data.id);
    } catch (error) {
      console.error("Error al obtener pregunta:", error);
      setPregunta(null);
    }
  };

  // Envía la respuesta seleccionada para validar
  const enviarRespuesta = async () => {
    console.log("Enviando respuesta...");
 
    if (pregunta && respuestaSeleccionada !== null) {
      try {
        const res = await fetch("http://localhost:5000/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            pregunta_id: pregunta.id,
            respuesta_usuario: respuestaSeleccionada,
          }),
        });
        const data = await res.json();
        console.log("Respuesta del servidor:", data);
        
        setResultado({
          correcto: data.correcto,
          explicacion: data.explicacion,
          respuesta_correcta: data.respuesta_correcta,
        });
        
      } catch (error) {
        console.error("Error al enviar respuesta:", error);
        setResultado(null);
      }
    } else {
      console.warn("Pregunta o respuesta seleccionada está vacía");
    }
  };

  // FUNCIÓN CORREGIDA: Maneja la selección de animales con checkbox
  const handleSelectAnimal = (entity) => {
    console.log("=== ANIMAL SELECCIONADO ===");
    console.log("Entity clickeada:", entity);
    console.log("texto_enriquecido del entity:", entity.texto_enriquecido);
    console.log("Entity actualmente seleccionada:", selectedAnimal);
    
    // Si ya está seleccionado, deseleccionamos (toggle)
    if (selectedAnimal && selectedAnimal.data?.NombreCientifico === entity.data?.NombreCientifico) {
      console.log("Deseleccionando animal");
      setSelectedAnimal(null);
      setPregunta(null);
      setRespuestaSeleccionada(null);
      setResultado(null);
    } else {
      console.log("Seleccionando nueva entity");
      setSelectedAnimal(entity);  // Ahora guardamos la entity completa
      // Limpiar estados previos
      setPregunta(null);
      setRespuestaSeleccionada(null);
      setResultado(null);
      // Las preguntas se cargarán automáticamente por el useEffect
    }
  };

  const handleSubmitAnswer = () => {
    console.log("Pregunta:", question)
    console.log("Respuesta:", answer)
  }

  // DEBUGGING DEL ESTADO ACTUAL
  console.log("=== ESTADO ACTUAL ===");
  console.log("speciesData:", speciesData);
  console.log("selectedAnimal:", selectedAnimal);
  console.log("selectedAnimal.texto_enriquecido:", selectedAnimal?.texto_enriquecido);

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
            <p className="info-subtitle">Ingrese el nombre comun o nombre cientifico del animal a buscar</p>

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
            speciesData.every(entity => !entity.data) ? (
              <p style={{ color: 'red', fontWeight: 'bold' }}>
                No se encontraron especies con la información proporcionada. Prueba con otro animal en peligro de extinción en Boyacá
              </p>
            ) : (
              <div className="species-checkboxes">
                {speciesData.map((entity, index) => {
                  const animal = entity.data;

                  if (!animal) {
                    return (
                      <div key={`no-data-${index}`} className="form-check">
                        <label className="form-check-label" style={{ color: '#a00' }}>
                          No se encontró información para "{entity.text}"
                        </label>
                      </div>
                    );
                  }

                  // CLAVE ÚNICA CORREGIDA: Usamos el NombreCientifico del animal
                  const uniqueKey = animal.NombreCientifico || `animal-${index}`;
                  
                  return (
                    <div key={uniqueKey} className="form-check">
                      <input
                        className="form-check-input"
                        type="checkbox"
                        id={`animal-${uniqueKey}`}
                        checked={selectedAnimal !== null && selectedAnimal.data?.NombreCientifico === animal.NombreCientifico}
                        onChange={() => handleSelectAnimal(entity)}
                      />
                      <label
                        className="form-check-label"
                        htmlFor={`animal-${uniqueKey}`}
                        style={{ color: '#0c0c0c', fontWeight: 'bold' }}
                        onClick={() => handleSelectAnimal(entity)}
                      >
                        {animal.NombreComun || animal.NombreCientifico}
                      </label>
                    </div>
                  );
                })}
              </div>
            )
          ) : null}

{/* Modal para mostrar información del animal seleccionado */}
          {selectedAnimal && (
            <div className="modal-overlay" onClick={() => setSelectedAnimal(null)}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                  <h3 className="modal-title">
                    🐾 {selectedAnimal.data?.NombreComun || selectedAnimal.data?.NombreCientifico || "Animal"}
                  </h3>
                  <button 
                    className="modal-close-btn"
                    onClick={() => setSelectedAnimal(null)}
                    aria-label="Cerrar modal"
                  >
                    ×
                  </button>
                </div>
                
                <div className="modal-body">
                  {selectedAnimal.texto_enriquecido ? (
                    <div className="texto-enriquecido">
                      <ReactMarkdown>{selectedAnimal.texto_enriquecido}</ReactMarkdown>
                    </div>
                  ) : (
                    <p className="no-info-text">⚠️ No hay información enriquecida disponible.</p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Preservación del ecosistema */}
        <div className="ecosystem-preservation">
          <h2>Preservación del ecosistema</h2>

          {!pregunta && <p>Selecciona un animal para cargar una pregunta...</p>}

          {pregunta && (
            <>
              <p className="pregunta-text">{pregunta.pregunta}</p>

              {/* LISTA DINÁMICA DE OPCIONES CORREGIDA */}
              {pregunta.opciones.map((opcion, i) => (
                <div key={`opcion-${pregunta.id}-${i}`} className="input-group">
                  <label>
                    <input
                      type="radio"
                      name={`respuesta-${pregunta.id}`} // Nombre único por pregunta
                      value={i}
                      checked={respuestaSeleccionada === i}
                      onChange={() => setRespuestaSeleccionada(i)}
                    />
                    {opcion}
                  </label>
                </div>
              ))}

              <button
                className="submit-button"
                onClick={enviarRespuesta}
                disabled={respuestaSeleccionada === null}
              >
                Enviar respuesta <span className="arrow-icon">→</span>
              </button>

              {resultado && (
                <div
                  className={`resultado ${resultado.correcto ? "correcto" : "incorrecto"}`}
                  style={{
                    backgroundColor: "white",
                    color: "black",
                    padding: "1rem",
                    borderRadius: "8px",
                  }}
                >
                  <p>
                    {resultado.correcto ? (
                      "¡Correcto!"
                    ) : (
                      <span style={{ fontWeight: "bold", color: "red" }}>Incorrecto</span>
                    )}
                  </p>

                  {!resultado.correcto && (
                    <>
                      <p>
                        <strong>La respuesta correcta es:</strong>{" "}
                        {resultado.respuesta_correcta
                          ? resultado.respuesta_correcta
                          : "No hay respuesta correcta disponible."}
                      </p>

                      <p>
                        <strong>Explicación:</strong>{" "}
                        {resultado.explicacion
                          ? resultado.explicacion
                          : "No hay explicación disponible."}
                      </p>
                    </>
                  )}

                  <button
                    onClick={() => obtenerPregunta(selectedAnimal.data?.NombreComun || selectedAnimal.data?.NombreCientifico)}
                    disabled={!selectedAnimal}
                  >
                    Otra pregunta
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnimalInfoForm