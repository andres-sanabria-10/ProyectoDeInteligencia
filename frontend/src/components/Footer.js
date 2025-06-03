const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="footer-main">
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-6">
            <p className="mb-0">© {currentYear} AniBoy - Proyecto de Inteligencia Computacional 🌿</p>
          </div>
          <div className="col-md-6 text-end">
            <p className="mb-0">Desarrollado para Inteligencia Computacional 🦋</p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
