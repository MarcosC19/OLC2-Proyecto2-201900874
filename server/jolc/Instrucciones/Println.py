from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.IdLista import IdLista
from tablaSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from Expresiones.Primitivo import Primitivo
from Expresiones.Logica import Logica
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST
from tablaSimbolos.Tipo import TIPO_DATO
from Expresiones.Identificador import Identificador
from C3D.variableC3D import TipoVar
from C3D.variableC3D import TipoVariable


class Println(AST):

    def __init__(self, expression, line, column):
        super().__init__(TIPO_DATO.CADENA, line, column)
        self.expresion = expression
        self.listImprimir = []

    def getNode(self):
        nodo = nodeAST("PRINTLN")
        nodo.addChild("println")
        nodo.addChild("(")
        if isinstance(self.expresion, list):
            nodoImprimir = nodeAST("VALORES")
            for expresion in self.expresion:
                nodoImprimir.addChildrenNode(expresion.getNode())
                if expresion != self.expresion[-1]:
                    nodoImprimir.addChild(",")
            nodo.addChildrenNode(nodoImprimir)
        else:
            nodo.addChildrenNode(self.expresion.getNode())
        nodo.addChild(")")
        nodo.addChild(";")
        return nodo
    
    def interpretar(self, table, tree):
        value = None
        if isinstance(self.expresion, list):
            texto = ""
            for expresion in self.expresion:
                valor = None
                valor = expresion.interpretar(table, tree)
                if isinstance(valor, Excepcion):
                    return valor
                if isinstance(valor, Primitivo):
                    valor = valor.interpretar(table, tree)
                if isinstance(valor, list):
                    valor = self.recorrerList(valor, table, tree)
                if isinstance(valor, Simbolo):
                    valores = valor.getValor()
                    text = valor.getId() + "("
                    for parametro in valores:
                        parte1 = parametro.getValor()
                        if isinstance(parte1, Primitivo):
                            if parte1.type == TIPO_DATO.CADENA:
                                text += "\""
                            elif parte1.type == TIPO_DATO.CARACTER:
                                text += "'"

                            parte2 = parte1.interpretar(table, tree)
                            text += str(parte2)

                            if parte1.type == TIPO_DATO.CADENA:
                                text += "\""
                            elif parte1.type == TIPO_DATO.CARACTER:
                                text += "'"
                        else:
                            if isinstance(parte1, Simbolo):
                                parte3 = self.recorrerAtr(parte1, table, tree)
                                text += parte3
                            else:
                                parte2 = parte1.interpretar(table, tree)
                                if isinstance(parte2, Simbolo):
                                    parte3 = self.recorrerAtr(parte2, table, tree)
                                    text += parte3

                        if parametro != valores[-1]:
                            text += ", "
                    text += ")"
                    valor = text

                texto += str(valor)
            value = texto

        tree.updateConsole(str(value) + '\n')
        return None

    def getC3D(self, c3dObj):
        C3D = "    /* EJECUCION PRINTLN */\n"
        for expresion in self.expresion:
            if isinstance(expresion, Primitivo):
                contadorTP = c3dObj.getContadorT()
                C3D += "    /* IMPRIMIENDO PRIMITIVO */\n"
                contenido = expresion.getC3D(c3dObj)
                if isinstance(contenido, list):
                    for valor in contenido:
                        if expresion.type == TIPO_DATO.ENTERO:
                            C3D += "    fmt.Printf(\"%d\", int(" + str(valor) + "));\n"
                        elif expresion.type == TIPO_DATO.DECIMAL:
                            C3D += "    fmt.Printf(\"%fn\", " + str(valor) + ");\n"
                else:
                    C3D += contenido
                    C3D += c3dObj.endString()
                    C3D += c3dObj.printString(contadorTP)
            elif isinstance(expresion, Aritmetica):
                contadorTP = c3dObj.getContadorT()
                C3D += "    /* IMPRIMIENDO ARITMETICA */\n"
                contenido = expresion.getC3D(c3dObj)
                if expresion.operating2 == None:    # OPERADOR UNARIO
                    if expresion.type == TIPO_DATO.ENTERO:
                        C3D += "    fmt.Printf(\"%d\", int(" + contenido[0] + "));\n"
                    elif expresion.type == TIPO_DATO.DECIMAL:
                        C3D += "    fmt.Printf(\"%f\", " + contenido[0] + ");\n"
                else:                           # OPERACIONES DOS OPERADORES
                    C3D += contenido[0]
                    if expresion.type == TIPO_DATO.ENTERO:
                            C3D += "    fmt.Printf(\"%d\", int(t" + str(contenido[1]) + "));\n"
                    elif expresion.type == TIPO_DATO.DECIMAL:
                        C3D += "    fmt.Printf(\"%f\", t" + str(contenido[1]) + ");\n"
                    else:
                        C3D += c3dObj.endString()
                        C3D += c3dObj.printString(contadorTP)
            elif isinstance(expresion, Relacional):
                C3D += "    /* IMPRIMIENDO RELACIONAL */\n"
                contenido = expresion.getC3D(c3dObj)
                C3D += contenido[0]
                C3D += "    L" + str(contenido[1]) + ":\n"
                C3D += c3dObj.printTrue()
                C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                temporalLS = c3dObj.getContadorL()
                c3dObj.addContadorL()
                C3D += "    L" + str(contenido[2]) + ":\n"
                C3D += c3dObj.printFalse()
                C3D += "    L" + str(temporalLS) + ":\n"
            elif isinstance(expresion, Logica):
                C3D += "    /* IMPRIMIENDO LOGICA */\n"
                contenido = expresion.getC3D(c3dObj)
                C3D += contenido[0]
                for valor in contenido[1]:
                    C3D += "    L" + str(valor) + ":\n"
                C3D += c3dObj.printTrue()
                C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                temporalLS = c3dObj.getContadorL()
                c3dObj.addContadorL()
                for valor in contenido[2]:
                    C3D += "    L" + str(valor) + ":\n"
                C3D += c3dObj.printFalse()
                C3D += "    L" + str(temporalLS) + ":\n"
            elif isinstance(expresion, Identificador):
                C3D += "    /* IMPRIMIENDO VARIABLE */\n"
                myVar = expresion.getC3D(c3dObj)
                if myVar != None:
                    C3D += myVar[0]
                    if myVar[2].getTypeVariable() == TipoVariable.VARIABLE:
                        if myVar[2].getType() == TipoVar.VALOR:
                            if expresion.type == TIPO_DATO.DECIMAL:
                                C3D += "    fmt.Printf(\"%f\", t" + str(myVar[1]) + ");\n"
                            elif expresion.type == TIPO_DATO.ENTERO:
                                C3D += "    fmt.Printf(\"%d\", int(t" + str(myVar[1]) + "));\n"
                        elif myVar[2].getType() == TipoVar.APUNTADOR:
                            C3D += c3dObj.printString(myVar[1])
                    elif myVar[2].getTypeVariable() == TipoVariable.LISTA:
                        C3D += "    fmt.Printf(\"%c\", 91);\n"
                        if myVar[2].getTypeVal() == TIPO_DATO.CADENA:
                            C3D += c3dObj.printString(myVar[1])
                        else:
                            C3D += c3dObj.printList(myVar[1])
                        C3D += "    fmt.Printf(\"%c\", 93);\n"
            elif isinstance(expresion, IdLista):
                C3D += "    /* IMPRIMIENDO VALOR LISTA */\n"
                resultado = expresion.getC3D(c3dObj)
                C3D += resultado[0]
                C3D += "    fmt.Printf(\"%f\", t" + str(resultado[1]) + ");\n"
                for etiqueta in resultado[2]:
                    C3D += "    L" + str(etiqueta) + ":\n"
        C3D += "    fmt.Printf(\"%c\\n\", 32);\n"
        return C3D
        
    def recorrerList(self, lista, table, tree):
        texto = "["
        for valor in lista:
            if isinstance(valor, list):
                    texto += self.recorrerList(valor, table, tree)
            else:
                content = valor.interpretar(table, tree)
                if valor.type == TIPO_DATO.CADENA:
                    texto += "\""
                elif valor.type == TIPO_DATO.CARACTER:
                    texto += "'"
                
                if isinstance(content, Primitivo):
                    content = content.interpretar(table, tree)
                texto += str(content)

                if valor.type == TIPO_DATO.CADENA:
                    texto += "\""
                elif valor.type == TIPO_DATO.CARACTER:
                    texto += "'"
            if valor != lista[-1]:
                texto += ", "
        texto += "]"
        return texto

    def recorrerAtr(self, valor, table, tree):
        valores = valor.getValor()
        text = valor.getId() + "("
        for parametro in valores:
            parte1 = parametro.getValor()
            if isinstance(parte1, Primitivo):
                if parte1.type == TIPO_DATO.CADENA:
                    text += "\""
                elif parte1.type == TIPO_DATO.CARACTER:
                    text += "'"

                parte2 = parte1.interpretar(table, tree)
                text += str(parte2)

                if parte1.type == TIPO_DATO.CADENA:
                    text += "\""
                elif parte1.type == TIPO_DATO.CARACTER:
                    text += "'"
            else:
                parte2 = parte1.interpretar(table, tree)
                if isinstance(parte2, Simbolo):
                    parte3 = self.recorrerAtr(parte2, table, tree)

            if parametro != valores[-1]:
                text += ", "
        text += ")"
        return text