import '../css/navbar.css';
import { Link } from 'react-router-dom';
import { Component } from 'react';

export default class Navbar extends Component{
    render() {
        return(
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <div className="container-fluid">
                    <Link className="navbar-brand mb-0 h1" to="/">
                        <img src="./images/iconJulia.png"  alt="" width="30" height="24" className="d-inline-block align-text-top"/>
                        &nbsp; JOLC
                    </Link>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            {/* ETIQUETA PARA ACCEDER AL COMPILADOR */}
                            <li className="nav-item">
                            <Link className="navbar-brand mb-0 h1"  to="/Interpreter">Editor</Link>
                            </li>
                            {/* ETIQUETA PARA ACCEDER AL COMPILADOR */}
                            <li className="nav-item">
                            <Link className="navbar-brand mb-0 h1"  to="/Compiler">Compilador</Link>
                            </li>
                            {/* ETIQUETA PARA ACCEDER AL OPTIMIZADOR MIRILLA */}
                            <li className="nav-item">
                            <Link className="navbar-brand mb-0 h1"  to="/OptMirr">Opt. Mirilla</Link>
                            </li>
                            {/* ETIQUETA PARA ACCEDER AL OPTIMIZADOR BLOQUES */}
                            <li className="nav-item">
                            <Link className="navbar-brand mb-0 h1"  to="/OptBlock">Opt. Bloques</Link>
                            </li>
                            {/* ETIQUETA PARA ACCEDER A LOS REPORTES*/}
                            <li className="nav-item">
                            <Link className="navbar-brand mb-0 h1" aria-current="page" to="/Reports">Reportes</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        );
    }
    
}