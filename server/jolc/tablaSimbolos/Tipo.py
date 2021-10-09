from enum import Enum

class TIPO_DATO(Enum):
    ENTERO = 1,
    DECIMAL = 2,
    CADENA = 3,
    CARACTER = 4,
    BOOLEANO = 5,
    LISTA = 6,
    NULL = 7,
    ERROR = 8,
    FUNCION = 9,
    STRUCTN = 10,
    STRUCTM = 11

class OPERADOR_ARITMETICO(Enum):
    SUMA = 1,
    RESTA = 2,
    MULTIPLICACION = 3,
    DIVISON = 4,
    POTENCIA = 5,
    MODULO = 6,
    UMENOS = 7,
    LOG10 = 8,
    LOG = 9,
    SENO = 10,
    COSENO = 11,
    TANGENTE = 12,
    RAIZ = 13

class OPERADOR_RELACIONAL(Enum):
    MAYORQUE = 1,
    MENORQUE = 2,
    MAYORIGUAL = 3,
    MENORIGUAL = 4,
    IGUAL = 5,
    DIFERENTE = 6

class OPERADOR_LOGICO(Enum):
    OR = 1,
    AND = 2,
    NOT = 3