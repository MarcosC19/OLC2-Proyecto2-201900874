import flask
import graphviz
from flask import Flask
from flask_cors import CORS
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.nodoAST import nodeAST
from gramaticaP import parse
from gramaticaP import parseC3D
from Optimizacion.gramaticaOPT import parseMirilla
from Optimizacion.contC3D import TipoOPT
from Optimizacion.contC3D import ReglasMir
from Optimizacion.contC3D import ReglasBlock

app = Flask(__name__)
CORS(app)
result = None
errores = []
reporteOpt = []

@app.route('/')
def helloServer():
    return 'Server work'

@app.route('/Interpreter', methods=['POST'])
def interpreterEntry():
    entrada = flask.request.json['entrada']
    global result
    global errores
    result = parse(entrada)
    errores = result[1]
    retorno = {"salida": result[0].getConsole()}
    return retorno

@app.route('/getAST', methods=['GET'])
def getAST():
    init = nodeAST("INICIO")
    instructions = nodeAST("INSTRUCCIONES")
    for instruccion in result[0].getInstructions():
        instructions.addChildrenNode(instruccion.getNode())
    init.addChildrenNode(instructions)
    dot = result[0].getDot(init)
    
    myGraph = graphviz.Digraph(format='svg')
    myGraph.body.append(dot)

    return myGraph.pipe().decode('utf-8')

@app.route('/getErrores', methods=['GET'])
def getErrors():
    global errores
    regreso = []
    for error in errores:
        jsonR = {
            'descripcion': error.getDesc(),
            'linea': error.getFile(),
            'columna': error.getColumn(),
            'tipo': error.getType(),
            'tiempo': error.getTime()
        }
        regreso.append(jsonR)
    prueba = {
        'error': regreso
    }
    return prueba

@app.route('/getTabla', methods=['GET'])
def getTable():
    regreso = []
    if len(result) > 2:
        tablaActual = result[2]
        tipo = ""
        for simbolo in tablaActual:
            nuevoSimbolo = tablaActual[simbolo]
            if nuevoSimbolo.typeVal == TIPO_DATO.ENTERO: tipo = "Entero"
            elif nuevoSimbolo.typeVal == TIPO_DATO.DECIMAL: tipo = "Decimal"
            elif nuevoSimbolo.typeVal == TIPO_DATO.CADENA: tipo = "Cadena"
            elif nuevoSimbolo.typeVal == TIPO_DATO.CARACTER: tipo = "Caracter"
            elif nuevoSimbolo.typeVal == TIPO_DATO.BOOLEANO: tipo = "Boolean"
            elif nuevoSimbolo.typeVal == TIPO_DATO.NULL: tipo = "Nulo"
            elif nuevoSimbolo.typeVal == TIPO_DATO.LISTA: tipo = "Lista"
            elif nuevoSimbolo.typeVal == TIPO_DATO.STRUCTN: tipo = "Struct No Mutable"
            elif nuevoSimbolo.typeVal == TIPO_DATO.STRUCTM: tipo = "Struct Mutable"
            elif nuevoSimbolo.typeVal == TIPO_DATO.FUNCION: tipo = "Funcion"
            jsonR = {
                'nombre': simbolo,
                'tipo': tipo,
                'ambito': 'global',
                'fila': nuevoSimbolo.fila,
                'columna': nuevoSimbolo.columna
            }
            regreso.append(jsonR)

        tablaActual = result[3]
        for simbolo in tablaActual:
            nuevoSimbolo = tablaActual[simbolo]
            if nuevoSimbolo.type == TIPO_DATO.ENTERO: tipo = "Entero"
            elif nuevoSimbolo.type == TIPO_DATO.DECIMAL: tipo = "Decimal"
            elif nuevoSimbolo.type == TIPO_DATO.CADENA: tipo = "Cadena"
            elif nuevoSimbolo.type == TIPO_DATO.CARACTER: tipo = "Caracter"
            elif nuevoSimbolo.type == TIPO_DATO.BOOLEANO: tipo = "Boolean"
            elif nuevoSimbolo.type == TIPO_DATO.NULL: tipo = "Nulo"
            elif nuevoSimbolo.type == TIPO_DATO.LISTA: tipo = "Lista"
            elif nuevoSimbolo.type == TIPO_DATO.STRUCTN: tipo = "Struct No Mutable"
            elif nuevoSimbolo.type == TIPO_DATO.STRUCTM: tipo = "Struct Mutable"
            elif nuevoSimbolo.type == TIPO_DATO.FUNCION: tipo = "Funcion"
            jsonR = {
                'nombre': simbolo,
                'tipo': tipo,
                'ambito': 'global',
                'fila': nuevoSimbolo.file,
                'columna': nuevoSimbolo.column
            }
            regreso.append(jsonR)
    prueba = {
        'tabla': regreso
    }
    return prueba

@app.route('/Compiler', methods=['POST'])
def getC3D():
    entrada = flask.request.json['entrada']
    global result
    global errores
    result = parseC3D(entrada)
    errores = result[1]
    retorno = {"salida": result[0].getC3D()}
    return retorno

@app.route('/Mirilla', methods=['POST'])
def getMirilla():
    entrada = flask.request.json['entrada']
    global result
    global reporteOpt
    result = parseMirilla(entrada)
    reporteOpt.extend(result[1])
    retorno = {"salida": result[0]}
    return retorno

@app.route('/ReporteOpt', methods = ['GET'])
def getReporteOPT():
    global reporteOpt
    regreso = []
    tipo = ""
    regla = ""
    for reporte in reporteOpt:
        if reporte.tipoOpt == TipoOPT.MIRILLA:
            tipo = "Mirilla"
        elif reporte.tipoOpt == TipoOPT.BLOQUEG:
            tipo = "Bloque Global"
        elif reporte.tipoOpt == TipoOPT.BLOQUEL:
            tipo = "Bloque Global"

        if reporte.regla == ReglasMir.REGLA1:
            regla = "Regla 1"
        elif reporte.regla == ReglasMir.REGLA2:
            regla = "Regla 2"
        elif reporte.regla == ReglasMir.REGLA3:
            regla = "Regla 3"
        elif reporte.regla == ReglasMir.REGLA4:
            regla = "Regla 4"
        elif reporte.regla == ReglasMir.REGLA5:
            regla = "Regla 5"
        elif reporte.regla == ReglasMir.REGLA6:
            regla = "Regla 6"
        elif reporte.regla == ReglasMir.REGLA7:
            regla = "Regla 7"
        elif reporte.regla == ReglasMir.REGLA8:
            regla = "Regla 8"
        jsonR = {
            'tipo': tipo,
            'regla': regla,
            'expA': reporte.expOld,
            'expN': reporte.expNuev,
            'fila': reporte.fila
        }
        regreso.append(jsonR)
    prueba = {
        'reporte': regreso
    }
    return prueba

if(__name__ == '__main__'):
    app.run(port = 5000, debug = False)