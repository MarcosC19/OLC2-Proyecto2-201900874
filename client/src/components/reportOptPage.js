import { Component } from 'react';
import '../css/reportOptPage.css';
import Navigation from './navbar';

export default class ReportOPT extends Component{
    constructor(){
        super();

        this.state = {
            reporte: [],
            archivo: ''
        }
    }

    componentDidMount(){
        this.getReport();
        alert('Generando reporte');
    }

    getReport(){
        fetch('http://localhost:5000/ReporteOpt')
        .then(res => res.json())
        .then(data => {
            this.setState({
                reporte: data.reporte
            });
        });
    }

    render() {
        return(
            <div>
                <div>
                    <Navigation/>
                </div>
                <h3 id = "opt">Reporte Optimizacion</h3>
                <div id = "mOPT">
                    <table border="1" cellPadding="2" cellSpacing="0" className="table table-success table-bordered border-dark">
                        <thead>
                            <tr>
                                <th>Tipo</th>
                                <th>Regla</th>
                                <th>Expresión Anterior</th>
                                <th>Expresión Nueva</th>
                                <th>Fila</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.state.reporte.map(simbolo => {
                                    return(
                                        <tr>
                                            <td>{simbolo.tipo}</td>
                                            <td>{simbolo.regla}</td>
                                            <td>{simbolo.expA}</td>
                                            <td>{simbolo.expN}</td>
                                            <td>{simbolo.fila}</td>
                                        </tr>
                                    )
                                })
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}