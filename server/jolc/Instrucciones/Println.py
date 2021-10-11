from tablaSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from Expresiones.Primitivo import Primitivo
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST
from tablaSimbolos.Tipo import TIPO_DATO


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

    def getC3D(self, contador):
        C3D = ""
        for expresion in self.expresion:
            if isinstance(expresion, Primitivo):
                contenido = expresion.getC3D(contador)
                for valor in contenido:
                    if expresion.type == TIPO_DATO.ENTERO:
                        C3D += "    fmt.Printf(\"%d\\n\", int(" + str(valor) + "));\n"
                    elif expresion.type == TIPO_DATO.DECIMAL:
                        C3D += "    fmt.Printf(\"%f\\n\", " + str(valor) + ");\n"
                    else:
                        if valor == contenido[-1]:
                            C3D += "    fmt.Printf(\"%c\\n\", " + str(valor) + ");\n"
                        else:
                            C3D += "    fmt.Printf(\"%c\", " + str(valor) + ");\n"
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