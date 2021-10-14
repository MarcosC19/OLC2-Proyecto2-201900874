import flask
import graphviz
from flask import Flask
from flask_cors import CORS
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.nodoAST import nodeAST
from gramaticaP import parse

app = Flask(__name__)
CORS(app)
result = None
errores = []

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
    tablaActual = result[2]
    while tablaActual != None:
        miTabla = tablaActual.tabla
        tipo = ""
        for simbolo in miTabla:
            nuevoSimbolo = miTabla[simbolo]
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
                'fila': nuevoSimbolo.getFile(),
                'columna': nuevoSimbolo.getColumn()
            }
            regreso.append(jsonR)
        tablaActual = tablaActual.anterior
    prueba = {
        'tabla': regreso
    }
    return prueba

@app.route('/Compiler', methods=['POST'])
def getC3D():
    entrada = flask.request.json['entrada']
    global result
    global errores
    result = parse(entrada)
    errores = result[1]
    retorno = {"salida": result[3].getC3D()}
    return retorno

if(__name__ == '__main__'):
    app.run(port = 5000, debug = True)