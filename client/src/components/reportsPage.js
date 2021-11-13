import { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/reportsPage.css';
import Navigation from './navbar';

export default class Reports extends Component{
    constructor(){
        super();

        this.state = {
            errores: [],
            table: [],
            archivo: ''
        }
    }

    componentDidMount(){
        this.getErrors();
        this.getTable();
        alert('Generando reportes');
    }

    getErrors(){
        fetch('https://jolc2-back-201900874.herokuapp.com/getErrores')
        .then(res => res.json())
        .then(data => {
            this.setState({
                errores: data.error
            });
        });
    }

    getTable(){
        fetch('https://jolc2-back-201900874.herokuapp.com/getTabla')
        .then(res => res.json())
        .then(data => {
            this.setState({
                table: data.tabla
            });
        });
    }

    render() {
        return(
            <div>
                <div>
                    <Navigation/>
                </div>
                <h3 id = "ts">Tabla de Simbolos</h3>
                <div id = "mTS">
                    <table border="1" cellPadding="2" cellSpacing="0" className="table table-success table-bordered border-dark">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Tipo</th>
                                <th>Ámbito</th>
                                <th>Fila</th>
                                <th>Columna</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.state.table.map(simbolo => {
                                    return(
                                        <tr>
                                            <td>{simbolo.nombre}</td>
                                            <td>{simbolo.tipo}</td>
                                            <td>{simbolo.ambito}</td>
                                            <td>{simbolo.fila}</td>
                                            <td>{simbolo.columna}</td>
                                        </tr>
                                    )
                                })
                            }
                        </tbody>
                    </table>
                </div>
                <h3 id = "errores">Tabla de Errores</h3>
                <div id = "mErrores">
                    <table border="1" cellPadding="2" cellSpacing="0" className="table table-primary table-bordered border-dark">
                        <thead>
                            <tr>
                                <th><center>Tipo</center></th>
                                <th><center>Descripción</center></th>
                                <th><center>Linea</center></th>
                                <th><center>Columna</center></th>
                                <th><center>Fecha y Hora</center></th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.state.errores.map(error => {
                                    return(
                                        <tr>
                                            <td>{error.tipo}</td>
                                            <td>{error.descripcion}</td>
                                            <td>{error.linea}</td>
                                            <td>{error.columna}</td>
                                            <td>{error.tiempo}</td>
                                        </tr>
                                    )
                                })
                            }
                        </tbody>
                    </table>
                </div>
                <button type="button" id = "arbol" className="btn btn-outline-dark" onClick={() => {window.open("https://jolc2-back-201900874.herokuapp.com/getAST", "_blank")}}>Visualizar<br/>Arbol</button>
                <Link to = "/ReportOpt"><button type="button" id = "optimizacion" className="btn btn-outline-dark">Reporte<br/>Optimizacion</button></Link>
            </div>
        );
    }
}