import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  // Asegurar que el body tenga fondo oscuro cuando se muestra esta página
  React.useEffect(() => {
    document.body.style.backgroundColor = '#121212';
    
    return () => {
      // Restaurar cuando se desmonte
      document.body.style.backgroundColor = '';
    };
  }, []);

  return (
    <div className="home-container">
      <div className="row justify-content-center">
        <div className="col-md-8 text-center">
          <h2 className="welcome-title">Bienvenido al generador de imágenes </h2>
          <p className="welcome-text">
            Top 10 de los animales en peligro de extinción:
          </p>
        </div>
      </div>
      
      <div className="row justify-content-center">
  <div className="col-md-7">
    <div id="analogCarousel" className="carousel slide" data-bs-ride="carousel">
      <div className="carousel-inner">
        {[
          { src: "/animals/1.jpg", title: "Lagartija anadia ", desc: "Nombre científico: Anadia bogotensis" },
          { src: "/animals/2.jpg", title: "Cerquero alidorado ", desc: "Nombre científico: Arremon schlegeli" },
          { src: "/animals/3.jpg", title: "Rana venenosa de Santander", desc: "Nombre científico: Andinobates virolinensis" },
          { src: "/animals/4.jpg", title: "Marteja Mico de noche Sorbe humo Maca cagao Mico chala", desc: "Nombre científico: Aotus lemurinus" },
          { src: "/animals/5.jpg", title: "Mono Araña Blanco", desc: "Nombre científico: Ateles belzebuth" },
          { src: "/animals/6.png", title: "Camaleón del Ruiz", desc: "Nombre científico: Anolis ruizii" },
          { src: "/animals/7.jpg", title: "Mono araña negro o Choibo", desc: "Nombre científico: Ateles hybridus" },
          { src: "/animals/8.jpeg", title: "Pato maicero Pato piquidorado", desc: "Nombre científico: Anas georgica" },
          { src: "/animals/9.jpg", title: "Rana Venesosa", desc: "Nombre científico: Allobates juanii" },
          { src: "/animals/10.jpeg", title: "Mico de noche caribeño", desc: "Nombre científico: Aotus griseimembra" },
        ].map((slide, idx) => (
          <div className={`carousel-item ${idx === 0 ? 'active' : ''}`} key={idx}>
            <img src={slide.src} className="d-block w-100 rounded" alt={slide.title} />
            <div className="carousel-caption d-none d-md-block bg-dark bg-opacity-50 p-3 rounded">
              <h5>{slide.title}</h5>
              <p>{slide.desc}</p>
            </div>
          </div>
        ))}
      </div>
      <button className="carousel-control-prev" type="button" data-bs-target="#analogCarousel" data-bs-slide="prev">
        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Anterior</span>
      </button>
      <button className="carousel-control-next" type="button" data-bs-target="#analogCarousel" data-bs-slide="next">
        <span className="carousel-control-next-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Siguiente</span>
      </button>
    </div>


  </div>
</div>


    </div>
  );
};

export default HomePage;