from Instrucciones.ModificacionAtributo import ModiAtributo
from Instrucciones.AccesoAtributo import AccesoAtributo
from Instrucciones.AsignStructN import StructN
from Expresiones.Atributo import Atributo
from Instrucciones.ModificacionLista import ModLista
from Instrucciones.Pop import Pop
from Instrucciones.Push import Push
from Instrucciones.Length import Length
from Instrucciones.GlobalVar import Global
from Instrucciones.Return import Return
from Instrucciones.LlamFuncion import LlamadaFuncion
from Instrucciones.DeclaFuncion import Funcion
from Expresiones.Parametro import Parametro
from Instrucciones.Uppercase import UpperCase
from Instrucciones.Lowercase import LowerCase
from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from Expresiones.IdLista import IdLista
from Instrucciones.AsignacionLista import Lista
from Instrucciones.For import For
from Instrucciones.While import While
from Instrucciones.If import If
from Instrucciones.Typeof import Typeof
from Instrucciones.String import String
from Instrucciones.Float import Float
from Instrucciones.Trunc import Truncate
from Instrucciones.Parse import Parse
from Instrucciones.AsignacionVar import Asignacion
from Expresiones.Identificador import Identificador
from tablaSimbolos.Simbolo import Simbolo
from tablaSimbolos.Tipo import OPERADOR_RELACIONAL
from Expresiones.Relacional import Relacional
from tablaSimbolos.Tipo import OPERADOR_LOGICO
from Expresiones.Logica import Logica
from tablaSimbolos.Tipo import OPERADOR_ARITMETICO
from Expresiones.Aritmetica import Aritmetica
from tablaSimbolos.Tipo import TIPO_DATO
from C3D.sentC3D import C3D
import re

errores = []
reservadas = {
    'print'         : 'RIMPRIMIR',
    'println'       : 'RIMPRIMIRLN',
    'true'          : 'RTRUE',
    'false'         : 'RFALSE',
    'nothing'       : 'RNULL',
    'log10'         : 'LOG10',
    'log'           : 'LOG',
    'sin'           : 'SENO',
    'cos'           : 'COSENO',
    'tan'           : 'TANG',
    'sqrt'          : 'RAIZ',
    'Int64'         : 'TIPENTERO',
    'Float64'       : 'TIPDECIMAL',
    'Null'          : 'TIPNULL',
    'Bool'          : 'TIPBOOL',
    'Char'          : 'TIPCHAR',
    'String'        : 'TIPSTRING',
    'parse'         : 'RPARSE',
    'trunc'         : 'RTRUNC',
    'float'         : 'RFLOAT',
    'string'        : 'RSTRING',
    'typeof'        : 'RTYPEOF',
    'lowercase'     : 'RLOWER',
    'uppercase'     : 'RUPPER',
    'global'        : 'RGLOBAL',
    'if'            : 'RIF',
    'elseif'        : 'RELSEIF',
    'else'          : 'RELSE',
    'end'           : 'REND',
    'while'         : 'RWHILE',
    'for'           : 'RFOR',
    'in'            : 'RIN',
    'break'         : 'RBREAK',
    'continue'      : 'RCONTINUE',
    'return'        : 'RRETURN',
    'function'      : 'RFUNCTION',
    'struct'        : 'RSTRUCT',
    'mutable'       : 'RMUTABLE',
    'length'        : 'RLENGTH',
    'pop'          : 'RPOP',
    'push'         : 'RPUSH'
}   

tokens = [
    'PTCOMA',
    'PUNTO',
    'IGUAL',
    'DOSPTS',
    'COMA',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POT',
    'MOD',
    'AND',
    'OR',
    'NOT',
    'MAYOR',
    'MAYORIGUAL',
    'MENOR',
    'MENORIGUAL',
    'IGUALDAD',
    'DIFERENTE',
    'ENTERO',
    'CADENA',
    'DECIMAL',
    'CARACTER',
    'ID'
] + list(reservadas.values())

# LISTA DE TOKENS
t_PTCOMA            = r';'
t_PUNTO             = r'\.'
t_IGUAL             = r'='
t_DOSPTS            = r':'
t_COMA              = r','
t_PARIZQ            = r'\('
t_PARDER            = r'\)'
t_CORIZQ            = r'\['
t_CORDER            = r'\]'
t_MAS               = r'\+'
t_MENOS             = r'-'
t_POR               = r'\*'
t_DIV               = r'/'
t_POT               = r'\^'
t_MOD               = r'%'
t_AND               = r'&&'
t_OR                = r'\|\|'
t_NOT               = r'!'
t_MAYOR             = r'>'
t_MAYORIGUAL        = r'>='
t_MENOR             = r'<'
t_MENORIGUAL        = r'<='
t_IGUALDAD          = r'=='
t_DIFERENTE         = r'!='

# NUMEROS DECIMALES
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Valor del float muy extenso: %d", t.value)
        t.value = 0
    return t

# NUMEROS ENTEROS
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor del integer demasiado grande %d", t.value)
        t.value = 0
    return t

# IDENTIFICADORES
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

# CADENAS DE CARACTERES
def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

# CARACTERES
def t_CARACTER(t):
    r'\'.?\''
    t.value = t.value[1:-1]
    return t

# COMENTARIOS MULTILINEA
def t_COMENTARIO_MULTILINEA(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count('\n')

# COMENTARIOS UNILINEA
def t_COMENTARIO_SIMPLE(t):
    r'\#.*'
    t.lexer.lineno += t.value.count('\n')


# CARACTERES IGNORADOS
t_ignore = ' \t'

# NUEVA LINEA
def t_newLine(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# RECONOCIMIENTO DE ERRORES LEXICOS
def t_error(t):
    errores.append(Excepcion("Lexico", "No se reconocio el caracter: " + t.value[0], t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# CONSTRUYENDO ANALIZADOR LEXICO
import ply.lex as lex
lexer = lex.lex()

# ASOCIACION Y PRECEDENCIA DE OPERADORES
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'IGUALDAD', 'DIFERENTE', 'MENOR', 'MAYOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR', 'DIV', 'MOD'),
    ('left', 'POT'),
    ('right','UMENOS')
    )


# DEFINICION DE LA GRAMATICA
from Expresiones.Primitivo import Primitivo
from Instrucciones.Print import Print
from Instrucciones.Println import Println
from Excepciones.Excepcion import Excepcion


def p_init(t):
    'init           : instrucciones'
    t[0] = t[1]

# -------------- LISTADO INSTRUCCIONES ----------------
def p_instrucciones_lista(t):
    'instrucciones      :  instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t):
    'instrucciones      : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

# ------------------ INSTRUCCION -----------------
def p_instruccion(t):
    '''instruccion      : imprimirSimple PTCOMA
                        | imprimirCompuesto PTCOMA
                        | asignacionVars PTCOMA
                        | asignacionLista PTCOMA
                        | add_valores PTCOMA
                        | delete_valores PTCOMA
                        | modificar_lista PTCOMA
                        | if_instruccion REND PTCOMA
                        | while_instruccion REND PTCOMA
                        | for_instruccion REND PTCOMA
                        | break_instruccion PTCOMA
                        | continue_instruccion PTCOMA
                        | retorno_instruccion PTCOMA
                        | def_funcion REND PTCOMA
                        | llamada_funcion PTCOMA
                        | def_global_var PTCOMA
                        | decla_structN REND PTCOMA
                        | modificar_struct PTCOMA'''

    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion        : error PTCOMA'
    errores.append(Excepcion("Sintactico", "Error sintactico con: " + str(t[1].value), t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""

# ---------------- PRINTS ------------------
def p_imprimir(t):
    'imprimirSimple     : RIMPRIMIR PARIZQ lista_expresion PARDER'
    t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_imprimir_con_salto(t) :
    'imprimirCompuesto     : RIMPRIMIRLN PARIZQ lista_expresion PARDER'
    t[0] = Println(t[3], t.lineno(1), find_column(input, t.slice[1]))

# ---------------- ASIGNACION VARIABLES --------------
def p_asignacion_vars(t):
    '''asignacionVars       :   ID IGUAL expresion DOSPTS DOSPTS TIPOVAL
                            |   ID IGUAL expresion'''
    
    if len(t) > 4:
        t[0] = Asignacion(t.lineno(1), find_column(input, t.slice[1]), t[1], t[3], t[6])
    else:
        t[0] = Asignacion(t.lineno(1), find_column(input, t.slice[1]), t[1], t[3])

def p_tipo_val(t):
    '''TIPOVAL          :   TIPENTERO
                        |   TIPDECIMAL
                        |   TIPNULL
                        |   TIPBOOL
                        |   TIPCHAR
                        |   TIPSTRING
                        |   ID'''

    if t[1] == 'Int64':
        t[0] = TIPO_DATO.ENTERO
    elif t[1] == 'Float64':
        t[0] = TIPO_DATO.DECIMAL
    elif t[1] == 'Null':
        t[0] = TIPO_DATO.NULL
    elif t[1] == 'Bool':
        t[0] = TIPO_DATO.BOOLEANO
    elif t[1] == 'Char':
        t[0] = TIPO_DATO.CARACTER
    elif t[1] == 'String':
        t[0] = TIPO_DATO.CADENA
    else:
        t[0] = t[1]

# ----------------- LISTAS ----------------
def p_asignacion_list_list(t):
    '''asignacionLista      : ID IGUAL CORIZQ lista_expresion CORDER'''
    t[0] = Lista(TIPO_DATO.LISTA, t.lineno(1), find_column(input, t.slice[1]), t[1], t[4])

def p_add_valores(t):
    'add_valores        : RPUSH NOT PARIZQ ID COMA expresion PARDER'
    t[0] = Push(TIPO_DATO.LISTA, t.lineno(1), find_column(input, t.slice[1]), t[4], t[6], None)

def p_add_valores_i(t):
    'add_valores        : RPUSH NOT PARIZQ ID CORIZQ expresion CORDER COMA expresion PARDER'
    t[0] = Push(TIPO_DATO.LISTA, t.lineno(1), find_column(input, t.slice[1]), t[4], t[9], t[6])

def p_delete_values(t):
    'delete_valores     : RPOP NOT PARIZQ ID PARDER'
    t[0] = Pop(TIPO_DATO.LISTA, t.lineno(1), find_column(input, t.slice[1]), t[4])

def p_mod_list(t):
    'modificar_lista    : ID conj_acceso IGUAL expresion'
    t[0] = ModLista(TIPO_DATO.LISTA, t.lineno(1), find_column(input, t.slice[1]), t[1], t[2], t[4])

# ------------- ASIGNACION GLOBAL ------------
def p_global_asignacion(t):
    'def_global_var     : RGLOBAL ID'
    t[0] = Global(t.lineno(1), find_column(input, t.slice[1]), t[2], None)

def p_global_asignacion_exp(t):
    'def_global_var     : RGLOBAL ID IGUAL expresion'
    t[0] = Global(t.lineno(1), find_column(input, t.slice[1]), t[2], t[4])

# ------------- IF --------------
def p_instruccion_if(t):
    '''if_instruccion   :   RIF expresion instrucciones'''
    t[0] = If(TIPO_DATO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), t[2], t[3], None, None)

def p_instruccion_elseIf(t):
    '''if_instruccion   :   RIF expresion instrucciones RELSEIF if_instruccion'''
    t[0] = If(TIPO_DATO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), t[2], t[3], None, t[5])

def p_instruccion_else(t):
    '''if_instruccion   :   RIF expresion instrucciones RELSE instrucciones'''
    t[0] = If(TIPO_DATO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), t[2], t[3], t[5], None)

def p_instruccion_normal1(t):
    '''if_instruccion   :   expresion instrucciones'''
    t[0] = If(TIPO_DATO.BOOLEANO, t.lineno, t.slice, t[1], t[2], None, None)

def p_instruccion_normal2(t):
    '''if_instruccion   :   expresion instrucciones RELSEIF if_instruccion'''
    t[0] = If(TIPO_DATO.BOOLEANO, t.lineno, t.slice, t[1], t[2], None, t[4])

def p_instruccion_normal3(t):
    '''if_instruccion   :   expresion instrucciones RELSE instrucciones'''
    t[0] = If(TIPO_DATO.BOOLEANO, t.lineno, t.slice, t[1], t[2], t[4], None)

# ------------------CICLOS--------------------
# ---------------- WHILE ----------------
def p_instruccion_while(t):
    '''while_instruccion        :   RWHILE expresion instrucciones'''
    t[0] = While(TIPO_DATO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), t[2], t[3])

# ---------------- FOR ----------------
def p_instruccion_forCad(t):
    '''for_instruccion          : RFOR ID RIN expresion instrucciones'''
    t[0] = For(TIPO_DATO.CADENA, t.lineno(1), find_column(input, t.slice[1]), t[2], t[4], None, t[5])

def p_instruccion_forNum(t):
    '''for_instruccion          : RFOR ID RIN expresion DOSPTS expresion instrucciones'''
    t[0] = For(TIPO_DATO.ENTERO, t.lineno(1), find_column(input, t.slice[1]), t[2], t[4], t[6], t[7])

# ------- SENTENCIAS DE TRANSFERENCIA ---------
def p_instruccion_break(t):
    '''break_instruccion        : RBREAK'''
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

def p_instruccion_continue(t):
    '''continue_instruccion        : RCONTINUE'''
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))

## ---------- DECLARACION DE FUNCIONES ------------
def p_decla_funcion_params(t):
    '''def_funcion      : RFUNCTION ID PARIZQ lista_params PARDER instrucciones'''
    t[0] = Funcion(TIPO_DATO.FUNCION, t.lineno(1), find_column(input, t.slice[1]), t[2], t[4], t[6])

def p_decla_funcion(t):
    '''def_funcion      : RFUNCTION ID PARIZQ PARDER instrucciones'''
    t[0] = Funcion(TIPO_DATO.FUNCION, t.lineno(1), find_column(input, t.slice[1]), t[2], None, t[5])

def p_lista_parametros(t):
    '''lista_params      : lista_params COMA parametro'''
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_parametro(t):
    '''lista_params      : parametro'''
    t[0] = [t[1]]

def p_parametro_id(t):
    '''parametro        : expresion'''
    t[0] = t[1]

# ------------ LLAMADA DE FUNCIONES ------------   
def p_llamada_funcion_params(t):
    '''llamada_funcion      : ID PARIZQ lista_params PARDER'''
    t[0] = LlamadaFuncion(t.lineno(1), find_column(input, t.slice[1]), t[1], t[3])

def p_llamada_funcion(t):
    '''llamada_funcion      : ID PARIZQ PARDER'''
    t[0] = LlamadaFuncion(t.lineno(1), find_column(input, t.slice[1]), t[1], None)

# ---------------- RETORNO ----------------
def p_retorno(t):
    'retorno_instruccion    : RRETURN expresion'
    t[0] = Return(t.lineno(1), find_column(input, t.slice[1]), t[2])

# --------------- STRUCTS NM --------------
def p_declaracion_structN(t):
    'decla_structN      : RSTRUCT ID lista_atributos '
    t[0] = StructN(TIPO_DATO.STRUCTN, t.lineno(1), find_column(input, t.slice[1]), t[2], t[3])

def p_declaracion_structM(t):
    'decla_structN      : RMUTABLE RSTRUCT ID lista_atributos '
    t[0] = StructN(TIPO_DATO.STRUCTM, t.lineno(1), find_column(input, t.slice[1]), t[3], t[4])

# ------------- ATRIBUTOS STRUCT -------------
def p_decla_atributos(t):
    'lista_atributos    : lista_atributos atributo'
    t[1].append(t[2])
    t[0] = t[1]

def p_decla_atributo(t):
    'lista_atributos    : atributo'
    t[0] = [t[1]]

def p_atributo_tipo(t):
    'atributo           : ID DOSPTS DOSPTS TIPOVAL PTCOMA'
    t[0] = Atributo(t.lineno, t.slice, t[1], None, t[4])

def p_atributo(t):
    'atributo           : ID PTCOMA'
    t[0] = Atributo(t.lineno, t.slice, t[1], None, None)

# ------------ MODIFICACION STRUCTS ------------
def p_modificar_struct(t):
    'modificar_struct   : ID PUNTO ID IGUAL expresion'
    t[0] = ModiAtributo(TIPO_DATO.NULL, t.lineno(1), find_column(input, t.slice[1]), t[1], t[3], t[5])

# ------------- ACCESO STRUCTS ----------
def p_expresion_struct(t):
    'expresion  : ID PUNTO ID'
    t[0] = AccesoAtributo(TIPO_DATO.NULL, t.lineno(1), find_column(input, t.slice[1]), t[1], t[3])

def p_expresion_struct_l(t):
    'expresion  : expresion PUNTO ID'
    t[0] = AccesoAtributo(TIPO_DATO.NULL, t.lineno, t.slice, t[1], t[3])

# ---------------- EXPRESIONES ----------------
def p_expresiones_aritmeticas(t):
    '''expresion        :   expresion MAS expresion 
                        |   expresion MENOS expresion
                        |   expresion POR expresion
                        |   expresion DIV expresion
                        |   expresion POT expresion
                        |   expresion MOD expresion
                        |   LOG10 PARIZQ expresion PARDER 
                        |   LOG PARIZQ expresion COMA expresion PARDER
                        |   SENO PARIZQ expresion PARDER
                        |   COSENO PARIZQ expresion PARDER
                        |   TANG PARIZQ expresion PARDER
                        |   RAIZ PARIZQ expresion PARDER'''

    if t[2] == '+':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.SUMA, t[1], t[3])
    elif t[2] == '-':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.RESTA, t[1], t[3])
    elif t[2] == '*':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.MULTIPLICACION, t[1], t[3])
    elif t[2] == '/':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.DIVISON, t[1], t[3])
    elif t[2] == '^':
        t[0] = Aritmetica(t[1].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.POTENCIA, t[1], t[3])
    elif t[2] == '%':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.MODULO, t[1], t[3])
    elif t[1] == 'log10':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.LOG10, t[3])
    elif t[1] == 'log':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.LOG, t[3], t[5])
    elif t[1] == 'sin':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.SENO, t[3])
    elif t[1] == 'cos':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.COSENO, t[3])
    elif t[1] == 'tan':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.TANGENTE, t[3])
    elif t[1] == 'sqrt':
        t[0] = Aritmetica(t[3].type, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_ARITMETICO.RAIZ, t[3])

def p_expresion_unaria_aritmetica(t):
    'expresion          :   MENOS expresion %prec UMENOS'
    t[0] = Aritmetica(t[2].type, t.lineno(1), find_column(input, t.slice[1]), OPERADOR_ARITMETICO.UMENOS, t[2])

def p_expresiones_logicas(t):
    '''expresion        :   expresion OR expresion
                        |   expresion AND expresion'''
    if t[2] == '&&':
        t[0] = Logica(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_LOGICO.AND, t[1], t[3])
    elif t[2] == '||':
        t[0] = Logica(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_LOGICO.OR, t[1], t[3])

def p_expresion_unaria_logica(t):
    'expresion          :   NOT expresion'
    t[0] = Logica(TIPO_DATO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), OPERADOR_LOGICO.NOT, t[2])

def p_expresiones_relacionales(t):
    '''expresion        :   expresion MAYOR expresion
                        |   expresion MAYORIGUAL expresion
                        |   expresion MENOR expresion
                        |   expresion MENORIGUAL expresion
                        |   expresion IGUALDAD expresion
                        |   expresion DIFERENTE expresion'''
    if t[2] == '>':
        t[0] = Relacional(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_RELACIONAL.MAYORQUE, t[1], t[3])
    elif t[2] == '>=':
        t[0] = Relacional(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_RELACIONAL.MAYORIGUAL, t[1], t[3])
    elif t[2] == '<':
        t[0] = Relacional(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_RELACIONAL.MENORQUE, t[1], t[3])
    elif t[2] == '<=':
        t[0] = Relacional(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_RELACIONAL.MENORIGUAL, t[1], t[3])
    elif t[2] == '==':
        t[0] = Relacional(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_RELACIONAL.IGUAL, t[1], t[3])
    elif t[2] == '!=':
        t[0] = Relacional(TIPO_DATO.BOOLEANO, t.lineno(2), find_column(input, t.slice[2]), OPERADOR_RELACIONAL.DIFERENTE, t[1], t[3])

def p_expresion_agrupacion(t):
    '''expresion          :    PARIZQ expresion PARDER'''
    t[0] = t[2]

def p_expresion_lista(t):
    '''mas_lista        : CORIZQ expresion CORDER'''
    t[0] = [t[2]]

def p_expresion_lista1(t):
    '''mas_lista        : CORIZQ lista_expresion CORDER'''
    t[0] = t[2]

def p_expresion_listExp(t):
    '''lista_expresion       :   lista_expresion COMA expresion'''
    t[1].append(t[3])
    t[0] = t[1]

def p_expresion_fin(t):
    '''lista_expresion      :   expresion'''
    t[0] = [t[1]]

# ------------- EXPRESIONES NORMALES ---------------
def p_expresion_entero(t):
    '''expresion        : ENTERO'''
    t[0] = Primitivo(TIPO_DATO.ENTERO, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_decimal(t):
    '''expresion        : DECIMAL'''
    t[0] = Primitivo(TIPO_DATO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_cadena(t):
    '''expresion        : CADENA'''
    t[0] = Primitivo(TIPO_DATO.CADENA, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_caracter(t):
    '''expresion        : CARACTER'''
    t[0] = Primitivo(TIPO_DATO.CARACTER, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_nulo(t):
    '''expresion        : RNULL'''
    t[0] = Primitivo(TIPO_DATO.NULL, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_rtrue(t):
    '''expresion        : RTRUE'''
    t[0] = Primitivo(TIPO_DATO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_rfalse(t):
    '''expresion        : RFALSE'''
    t[0] = Primitivo(TIPO_DATO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), t[1])

# ------------- FUNCIONES NATIVAS -------------
def p_expresion_parse(t):
    '''expresion        : RPARSE PARIZQ TIPOVAL COMA expresion PARDER
                        | RPARSE PARIZQ expresion PARDER'''
    if len(t) > 5:
        t[0] = Parse(t.lineno(1), find_column(input, t.slice[1]), t[5], t[3])
    else:
        t[0] = Parse(t.lineno(1), find_column(input, t.slice[1]), t[3])

def p_expresion_trunc(t):
    '''expresion        : RTRUNC PARIZQ expresion PARDER'''
    t[0] = Truncate(t.lineno(1), find_column(input, t.slice[1]), t[3], TIPO_DATO.ENTERO)

def p_expresion_float(t):
    '''expresion        : RFLOAT PARIZQ expresion PARDER'''
    t[0] = Float(t.lineno(1), find_column(input, t.slice[1]), t[3], TIPO_DATO.DECIMAL)

def p_expresion_string(t):
    'expresion          : RSTRING PARIZQ expresion PARDER'
    t[0] = String(TIPO_DATO.CADENA, t.lineno(1), find_column(input, t.slice[1]), t[3])

def p_expresion_typeof(t):
    'expresion          : RTYPEOF PARIZQ expresion PARDER'
    t[0] = Typeof(TIPO_DATO.NULL, t.lineno(1), find_column(input, t.slice[1]), t[3])

def p_expresion_lower(t):
    '''expresion        : RLOWER PARIZQ expresion PARDER'''
    t[0] = LowerCase(TIPO_DATO.CADENA, t.lineno(1), find_column(input, t.slice[1]), t[3])

def p_expresion_upper(t):
    '''expresion        : RUPPER PARIZQ expresion PARDER'''
    t[0] = UpperCase(TIPO_DATO.CADENA, t.lineno(1), find_column(input, t.slice[1]), t[3])

# ---------- IDENTIFICADORES ----------------
def p_expresion_id(t):
    '''expresion        : ID'''
    t[0] = Identificador(TIPO_DATO.CADENA, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_lista_id(t):
    '''expresion        : ID conj_acceso'''
    t[0] = IdLista(TIPO_DATO.LISTA, t.lineno(1), find_column(input, t.slice[1]), t[1], t[2])

def p_conj_acceso(t):
    '''conj_acceso      : conj_acceso mas_lista'''
    t[0] = [t[1], t[2]]

def p_conj_acceso2(t):
    '''conj_acceso      : mas_lista'''
    t[0] = t[1]

def p_expresion_listas(t):
    '''expresion        : mas_lista'''
    t[0] = t[1]

def p_expresion_function(t):
    'expresion      : llamada_funcion'
    t[0] = t[1]

def p_expresion_length(t):
    'expresion  : RLENGTH PARIZQ expresion PARDER'
    t[0] = Length(TIPO_DATO.ENTERO, t.lineno(1), find_column(input, t.slice[1]), t[3])

def p_expresion_pop(t):
    'expresion  : delete_valores'
    t[0] = t[1]

import ply.yacc as yacc
parser = yacc.yacc()

from tablaSimbolos.Arbol import Arbol
from tablaSimbolos.Tabla import Tabla


def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    instrucciones=parser.parse(inp)
    ast = Arbol(instrucciones)
    TSGlobal = Tabla()
    ast.setGlobal(TSGlobal)

    if ast.getInstructions() != None:
        for instruccion in ast.getInstructions():
            if isinstance(instruccion, Funcion):
                simbolo = Simbolo(TIPO_DATO.FUNCION, instruccion.identificador, instruccion.line, instruccion.column, instruccion)
                TSGlobal.setVariable(simbolo)

        for instruccion in ast.getInstructions():
            myInstruction = None
            if isinstance(instruccion, If):
                myInstruction = instruccion.interpretar(TSGlobal, ast, None)
            elif isinstance(instruccion, Break):
                myInstruction = Excepcion("Semantico", "Break se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
            elif isinstance(instruccion, Continue):
                myInstruction = Excepcion("Semantico", "Continue se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
            else:
                myInstruction = instruccion.interpretar(TSGlobal, ast)
            if isinstance(myInstruction, Excepcion): 
                errores.append(myInstruction)
                ast.updateConsole(myInstruction.imprimir())

    return [ast, errores, ast.getGlobal()]

def parseC3D(inp) :
    global errores
    global lexer
    global parser
    errores = []
    c3d = C3D()
    c3d.initC3D()
    instC3D = ""
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    instrucciones=parser.parse(inp)
    ast = Arbol(instrucciones)
    TSGlobal = Tabla()
    ast.setGlobal(TSGlobal)

    if ast.getInstructions() != None:
        for instruccion in ast.getInstructions():
            if isinstance(instruccion, Funcion):
                simbolo = Simbolo(TIPO_DATO.FUNCION, instruccion.identificador, instruccion.line, instruccion.column, instruccion)
                TSGlobal.setVariable(simbolo)

        for instruccion in ast.getInstructions():
            if isinstance(instruccion, Excepcion): 
                errores.append(instruccion)
                ast.updateConsole(instruccion.imprimir())
            elif isinstance(instruccion, If):
                instC3D += instruccion.getC3D(c3d, None, None)
            elif isinstance(instruccion, Break):
                instC3D += instruccion.getC3D(c3d, None)
            else:
                instC3D += instruccion.getC3D(c3d)

        instC3D += "}"
        c3d.addLastIMP()
        potCode = c3d.addPotencia()
        printList = c3d.addPrintList()
        printCode = c3d.addPrintString()
        compareStr = c3d.addCompareString()
        if c3d.getContadorT() > 0:
            contadores = "var "
            for i in range(0, c3d.getContadorT()):
                contadores += "t" + str(i)
                if i != c3d.getContadorT() -1:
                    contadores += ", "
            contadores += " float64;\n\n"
            c3d.addC3D(contadores)
        else:
            c3d.addC3D("\n")
        c3d.addC3D("/* MIS FUNCIONES */\n")
        c3d.addC3D(potCode)
        c3d.addC3D(printList)
        c3d.addC3D(printCode)
        c3d.addC3D(compareStr)
        c3d.addC3D("/* MAIN */\n")
        c3d.addC3D("func main(){\n")
        c3d.addC3D(instC3D)

    return [c3d, errores, ast.getGlobal()]