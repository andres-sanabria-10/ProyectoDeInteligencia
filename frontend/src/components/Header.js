import { Link } from "react-router-dom"

const Header = () => {
  return (
    <header className="header-main">
      <div className="container-fluid">
        <div className="row align-items-center">
          <div className="col-md-3">
            <Link to="/" className="logo-link">
              <h2 className="m-0">🦎 AniBoy</h2>
            </Link>
          </div>
          <div className="col-md-9">
            <nav className="main-nav">
              <ul className="nav-list">
                <li>
                  <Link to="/" className="nav-link">
                    🏠 Inicio
                  </Link>
                </li>
                <li>
                  <Link to="/animal-info" className="nav-link">
                    🚀 Empezar
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
