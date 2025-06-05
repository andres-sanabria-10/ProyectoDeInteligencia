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
  const [estadoAnterior, setEstadoAnterior] = useState(-1); // Para Q-learning

  // NUEVO: Estado para detectar si el usuario pidió imagen
  const [solicitudConImagen, setSolicitudConImagen] = useState(false);

  // NUEVO: Función para detectar si el usuario solicita imagen
  const detectarSolicitudImagen = (texto) => {
    const patrones = [
      "genera imagen", "generar imagen", "crea imagen", "crear imagen",
      "muestra imagen", "mostrar imagen", "crea foto", "crear foto", 
      "genera foto", "generar foto", "imagen", "foto", "visual",
      "como se ve", "cómo se ve", "visualizar", "ver imagen"
    ];
    
    return patrones.some(patron => texto.toLowerCase().includes(patron));
  };

  const handleSearch = async () => {
    try {
      // CORREGIDO: Detectar si el usuario pidió imagen antes de hacer la búsqueda
      const pidioImagen = detectarSolicitudImagen(animalInfo);
      setSolicitudConImagen(pidioImagen);

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

      console.log("=== RESPUESTA COMPLETA DEL SERVIDOR ===");
      console.log(data);
      console.log("=== USUARIO PIDIÓ IMAGEN? ===", pidioImagen);

      // Guardar los resultados en estado para mostrarlos después
      setSpeciesData(data.entities || []);
      // Limpiar el textarea de entrada
      setSpeciesInfo("");
      setSelectedAnimal(null);
      setPregunta(null);
      setRespuestaSeleccionada(null);
      setResultado(null);
      setUltimaPreguntaId(null);
      setEstadoAnterior(-1);

    } catch (error) {
      console.error("Error al buscar:", error);
      alert("No se pudo obtener información del animal.");
    }
  };

  // Cuando cambias el animal seleccionado, traemos la primera pregunta
  useEffect(() => {
    if (selectedAnimal) {
      obtenerPrimeraPregunta(selectedAnimal.data?.NombreComun || selectedAnimal.data?.NombreCientifico);
    }
  }, [selectedAnimal]);

  // Obtiene la PRIMERA pregunta del backend
  const obtenerPrimeraPregunta = async (nombreComun) => {
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
      setEstadoAnterior(-1); // Primera pregunta
    } catch (error) {
      console.error("Error al obtener pregunta:", error);
      setPregunta(null);
    }
  };

  // Obtiene la SIGUIENTE pregunta usando Q-learning
  const obtenerSiguientePregunta = async () => {
    try {
      const res = await fetch("http://localhost:5000/pregunta_siguiente", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ultima_pregunta_id: ultimaPreguntaId,
          estado_anterior: estadoAnterior
        }),
      });
      const data = await res.json();
      setPregunta(data);
      setRespuestaSeleccionada(null);
      setResultado(null);
      setUltimaPreguntaId(data.id);
    } catch (error) {
      console.error("Error al obtener siguiente pregunta:", error);
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

        // Actualizar estado para Q-learning
        setEstadoAnterior(data.correcto ? 1 : 0);

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

    // Si ya está seleccionado, deseleccionamos (toggle)
    if (selectedAnimal && selectedAnimal.data?.NombreCientifico === entity.data?.NombreCientifico) {
      console.log("Deseleccionando animal");
      setSelectedAnimal(null);
      setPregunta(null);
      setRespuestaSeleccionada(null);
      setResultado(null);
      setUltimaPreguntaId(null);
      setEstadoAnterior(-1);
    } else {
      console.log("Seleccionando nueva entity");
      setSelectedAnimal(entity);
      // Limpiar estados previos
      setPregunta(null);
      setRespuestaSeleccionada(null);
      setResultado(null);
      setUltimaPreguntaId(null);
      setEstadoAnterior(-1);
      // Las preguntas se cargarán automáticamente por el useEffect
    }
  };

  return (
    <div className="animal-info-container">
      <div className="welcome-section">
        <p>Ingresa información relacionada con animales en peligro de extinción en Boyacá</p>
      </div>

      <div className="info-grid">
        {/* Columna izquierda - Información */}
        <div className="info-column">
          <div className="info-box">
            <h2>Información</h2>
            <p className="info-subtitle">Ingrese el nombre común o nombre científico del animal a buscar</p>

            <div className="text-area-container">
              <textarea
                value={animalInfo}
                onChange={(e) => setAnimalInfo(e.target.value)}
                placeholder="Ejemplo:
                Gallito de Roca
                Es de color rojo y negro
                Tiene cresta
                Es un ave

                Para generar imagen incluye: 'genera imagen' o 'crear foto'"
                className="info-textarea"
              />
              <div className="scrollbar">
                <div className="scrollbar-thumb"></div>
              </div>
            </div>

            <button className="search-button" onClick={handleSearch}>
              BUSCAR
            </button>

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
                        {/* CORREGIDO: BOTÓN DE DESCARGA SOLO SI SE SOLICITÓ IMAGEN */}
                        {solicitudConImagen && selectedAnimal.imagen && selectedAnimal.imagen.success && (
                          <div className="imagen-download-section">
                            <p>🖼️ Imagen generada exitosamente</p>
                            <button
                              className="download-imagen-btn"
                              onClick={async () => {
                                try {
                                  const response = await fetch(`http://localhost:5000/imagen/${selectedAnimal.imagen.filename}`);
                                  const blob = await response.blob();

                                  const url = window.URL.createObjectURL(blob);
                                  const link = document.createElement('a');
                                  link.href = url;
                                  link.download = selectedAnimal.imagen.filename;
                                  link.click();
                                  window.URL.revokeObjectURL(url);
                                } catch (error) {
                                  console.error('Error al descargar:', error);
                                  alert('Error al descargar la imagen');
                                }
                              }}
                              style={{
                                backgroundColor: '#4CAF50',
                                color: 'white',
                                padding: '10px 20px',
                                border: 'none',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                marginBottom: '20px'
                              }}
                            >
                              📥 Descargar imagen del {selectedAnimal.data?.NombreComun}
                            </button>
                          </div>
                        )}

                        {/* NUEVO: Mensaje informativo si no se pidió imagen pero se generó */}
                        {!solicitudConImagen && selectedAnimal.imagen && selectedAnimal.imagen.success && (
                          <div className="imagen-info-section" style={{ 
                            backgroundColor: '#e3f2fd', 
                            padding: '10px', 
                            borderRadius: '5px', 
                            marginBottom: '15px',
                            border: '1px solid #2196F3'
                          }}>
                            <p style={{ margin: 0, color: '#1976D2' }}>
                              💡 <strong>Consejo:</strong> Para ver y descargar imágenes del animal, incluye "genera imagen" o "crear foto" en tu búsqueda.
                            </p>
                          </div>
                        )}

                        {/* TEXTO ENRIQUECIDO */}
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
            </div>
          </div>
        </div>

        {/* Columna derecha - Preguntas de Preservación */}
        <div className="questions-column">
          <div className="ecosystem-preservation">
            <h2>🌿 Preservación del ecosistema</h2>

            {!pregunta && (
              <div className="question-card waiting-card">
                <div className="card-body">
                  <p className="waiting-text">🌿 Selecciona un animal para cargar una pregunta...</p>
                </div>
              </div>
            )}

            {pregunta && (
              <div className="question-card">
                <div className="question-card-header">
                  <h3 className="question-title">🧠 Pregunta sobre conservación</h3>
                </div>

                <div className="question-card-body">
                  <p className="pregunta-text">{pregunta.pregunta}</p>

                  <div className="opciones-container">
                    {pregunta.opciones.map((opcion, i) => (
                      <div key={`opcion-${pregunta.id}-${i}`} className="opcion-item">
                        <label className="opcion-label">
                          <input
                            type="radio"
                            name={`respuesta-${pregunta.id}`}
                            value={i}
                            checked={respuestaSeleccionada === i}
                            onChange={() => setRespuestaSeleccionada(i)}
                            className="radio-input"
                          />
                          <span className="radio-custom"></span>
                          <span className="opcion-text">{opcion}</span>
                        </label>
                      </div>
                    ))}
                  </div>

                  <button
                    className="submit-answer-btn"
                    onClick={enviarRespuesta}
                    disabled={respuestaSeleccionada === null}
                  >
                    <span className="btn-text">Enviar respuesta</span>
                    <span className="btn-icon">🚀</span>
                  </button>

                  {resultado && (
                    <div className={`resultado-card ${resultado.correcto ? "correcto" : "incorrecto"}`}>
                      <div className="resultado-header">
                        <span className="resultado-icon">
                          {resultado.correcto ? "✅" : "❌"}
                        </span>
                        <span className="resultado-title">
                          {resultado.correcto ? "¡Correcto!" : "Incorrecto"}
                        </span>
                      </div>

                      {!resultado.correcto && (
                        <div className="resultado-details">
                          <div className="respuesta-correcta">
                            <strong>Respuesta correcta:</strong>
                            <p>{resultado.respuesta_correcta || "No disponible"}</p>
                          </div>

                          <div className="explicacion">
                            <strong>Explicación:</strong>
                            <p>{resultado.explicacion || "No disponible"}</p>
                          </div>
                        </div>
                      )}

                      <button
                        className="otra-pregunta-btn"
                        onClick={obtenerSiguientePregunta}
                      >
                        🔄 Otra pregunta
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnimalInfoForm