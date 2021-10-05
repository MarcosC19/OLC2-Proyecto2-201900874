import { Component } from 'react';
import '../css/principal.css';
import Navigation from './navbar';

export default class Principal extends Component {
    render() {
        return(
            <div>
                <div>
                    <Navigation/>
                </div>
                <div id="fondo">
                    <img src="./images/fondo.jpg" id="card" alt="Fondo JOLC"/>
                    <h2 id="initialMessage">Bienvenido a JOLC</h2>
                    <h2 id="titleCard">Datos del Desarrollador</h2>
                    <div id="datos">
                        <div id="nameCard">
                            <img src="./images/nombre.png" id="nameI" alt="Nombre Desarrollador"></img>
                            <h3 id="nameT">Marcos Enrique Curtidor Sagui</h3>
                        </div>
                        <div id="carneCard">
                            <img src="./images/carneNumber.png" id="carneI" alt="Carne Desarrollador"></img>
                            <h3 id="carneT">201900874</h3>
                        </div>
                        <div id="classCard">
                            <img src="./images/classImage.png" id="classI" alt="Curso"></img>
                            <h3 id="classT">Organización de Lenguajes y Compiladores 2</h3>
                        </div>
                        <div id="dateCard">
                            <img src="./images/dateImage.png" id="dateI" alt="Fecha"></img>
                            <h3 id="dateT">Segundo Semestre 2021</h3>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}