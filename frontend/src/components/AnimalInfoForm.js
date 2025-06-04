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
      obtenerPregunta(selectedAnimal.NombreComun || selectedAnimal.NombreCientifico);
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
     console.log("Enviando respuesta...");  // <- para confirmar que entra
 
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
        console.log("Respuesta del servidor:", data);  // <- para ver qué devuelve el backend
        
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
    console.warn("Pregunta o respuesta seleccionada está vacía"); // <--- AÑADE ESTO
  }
  };
   // Limpiar selección al cambiar animal para evitar selección múltiple
  const handleSelectAnimal = (animal) => {
    // Si ya está seleccionado, deseleccionamos (toggle)
     console.log("handleSearch llamado con animalInfo:", animalInfo);
    if (selectedAnimal?._id === animal._id) {
      setSelectedAnimal(null);
      setPregunta(null);
      setRespuestaSeleccionada(null);
      setResultado(null);
    } else {
      setSelectedAnimal(animal);
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
) : null}




{/* Mostrar detalles del animal seleccionado */}
{selectedAnimal && (
  <div className="border rounded-lg p-5 mt-5 bg-gray-50 shadow-md">
    <h3 className="text-xl font-bold mb-2">{selectedAnimal.NombreComun || "Animal"}</h3>
    <p><strong>Nombre Científico:</strong> {selectedAnimal.NombreCientifico}</p>
    <p><strong>Familia:</strong> {selectedAnimal.Familia}</p>
    <p><strong>Género:</strong> {selectedAnimal.Genero}</p>
    <p><strong>Estado de Conservación:</strong> {selectedAnimal.EstadoDeConservacion}</p>
    <p><strong>Localidad:</strong> {selectedAnimal.Localidad}</p>
    <p><strong>Hábitat:</strong> {selectedAnimal.Habitat}</p>
    <p><strong>Amenazas:</strong> {selectedAnimal.Amenazas}</p>
    <p><strong>Esfuerzos de Protección:</strong> {selectedAnimal.EsfuerzosDeProteccion}</p>
    <p><strong>Características:</strong> {selectedAnimal.Caracteristicas}</p>
    <p><strong>Registros:</strong> {selectedAnimal.Registros}</p>
   
    <p><strong>Texto enriquecido:</strong></p>
    <ReactMarkdown>{selectedAnimal.texto_enriquecido}</ReactMarkdown>

  </div>
)}



        </div>
         {/* Preservación del ecosistema - NUEVA ESTRUCTURA */}
        <div className="ecosystem-preservation">
          <h2>Preservación del ecosistema</h2>

          {!pregunta && <p>Selecciona un animal para cargar una pregunta...</p>}

          {pregunta && (
            <>
              <p className="pregunta-text">{pregunta.pregunta}</p>

              {pregunta.opciones.map((opcion, i) => (
                <div key={i} className="input-group">
                  <label>
                    <input
                      type="radio"
                      name="respuesta"
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
      onClick={() => obtenerPregunta(selectedAnimal.NombreComun)}
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
