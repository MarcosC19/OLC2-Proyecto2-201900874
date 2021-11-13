reservadas = {
    'package'       : 'RPACK',
    'main'          : 'RMAIN',
    'import'        : 'RIMPORT',
    'var'           : 'RVAR',
    'fmt'           : 'RFMT',
    'Printf'        : 'RPRINT',
    'math'          : 'RMATH',
    'int'           : 'RINT',
    'stack'         : 'RSTACK',
    'heap'          : 'RHEAP',
    'P'             : 'RP',
    'H'             : 'RH',
    'if'            : 'RIF',
    'float64'       : 'RFLOAT',
    'func'          : 'RFUNC',
    'goto'          : 'RGOTO',
    'return'        : 'RRETURN',
    'Mod'           : 'RMOD'
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
    'LLAVIZQ',
    'LLAVDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'MAYOR',
    'MAYORIGUAL',
    'MENOR',
    'MENORIGUAL',
    'IGUALDAD',
    'DIFERENTE',
    'ENTERO',
    'CADENA',
    'DECIMAL',
    'ID',
    'PORCENTAJE',
    'COMI'
] + list(reservadas.values())

# LISTA DE TOKENS
t_PTCOMA            = r';'
t_COMI              = r'\"'
t_PUNTO             = r'\.'
t_IGUAL             = r'='
t_DOSPTS            = r':'
t_COMA              = r'\,'
t_PARIZQ            = r'\('
t_PARDER            = r'\)'
t_LLAVIZQ           = r'\{'
t_LLAVDER           = r'\}'
t_CORIZQ            = r'\['
t_CORDER            = r'\]'
t_MAS               = r'\+'
t_MENOS             = r'-'
t_POR               = r'\*'
t_DIV               = r'/'
t_MAYOR             = r'>'
t_MAYORIGUAL        = r'>='
t_MENOR             = r'<'
t_MENORIGUAL        = r'<='
t_IGUALDAD          = r'=='
t_DIFERENTE         = r'!='
t_PORCENTAJE        = r'%'

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

# COMENTARIOS MULTILINEA
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# CARACTERES IGNORADOS
t_ignore = ' \t'

# NUEVA LINEA
def t_newLine(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# CONSTRUYENDO ANALIZADOR LEXICO
import re
import ply.lex as lex

from .Instrucciones.Expresion import Expresion
from .Instrucciones.LlamadaFuncion import LLamFuncion
from .Instrucciones.Return import Return
from .Instrucciones.Etiqueta import Etiqueta
from .Instrucciones.If import If
from .Instrucciones.Salto import Salto
from .Instrucciones.Comparacion import Comparacion
from .Instrucciones.Imprimir import Imprimir
from .contC3D import contC3D
from .Instrucciones.Funcion import Funcion
from .Instrucciones.Asignacion import Asignacion
lexer = lex.lex()

# ASOCIACION Y PRECEDENCIA DE OPERADORES
precedence = (
    ('left', 'IGUALDAD', 'DIFERENTE', 'MENOR', 'MAYOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR', 'DIV'),
    ('right','UMENOS')
)

def p_init(t):
    'init           : encabezado'
    t[0] = t[1]

# -------------- ENCABEZADO ----------------
def p_encabezado(t):
    '''encabezado           : RPACK RMAIN PTCOMA sigEnc funciones'''
    t[0] = contC3D(t[1] + " " + t[2] + t[3] + "\n" + t[4], t[5])

def p_sig_encabezado(t):
    '''sigEnc               : RIMPORT PARIZQ conjLibs'''
    t[0] = t[1] + t[2] + "\n" + t[3] 
    
def p_conjLibs(t):
    '''conjLibs             : CADENA PARDER variables'''
    t[0] = '\"' + t[1] + '\"' + "\n )\n" + t[3]
    
def p_conjLibs2(t):
    '''conjLibs             : CADENA PTCOMA CADENA PARDER variables'''
    t[0] = '\"' + t[1] + '\"' + ";\n" + '\"' + t[3] + '\"' + "\n)\n" + t[5]
    
def p_varExp(t):
    '''variables            : RVAR RSTACK CORIZQ ENTERO CORDER RFLOAT PTCOMA variables1'''
    t[0] = t[1] + " " + t[2] + t[3] + str(t[4]) + t[5] + t[6] + ";\n" + t[8]
    
def p_varExp1(t):
    '''variables1               : RVAR RHEAP CORIZQ ENTERO CORDER RFLOAT PTCOMA variables2'''
    t[0] = t[1] + " " + t[2] + t[3] + str(t[4]) + t[5] + t[6] + ";\n" + t[8]
    
def p_varExp2(t):
    '''variables2               : RVAR RP COMA RH RFLOAT PTCOMA variables3'''
    t[0] = t[1] + " " + t[2]  + t[3] + " " + t[4] + " " + t[5] + ";\n" + t[7]
    
def p_varExp3(t):
    '''variables3               : RVAR listaTMP RFLOAT PTCOMA'''
    t[0] = t[1] + " " + t[2] + " " + t[3] + ";\n\n"
    
def p_temporales(t):
    '''listaTMP               : listaTMP COMA ID'''
    t[0] = t[1] + t[2] + " " + t[3]
    
def p_temporales2(t):
    '''listaTMP               : ID'''
    t[0] = t[1]

# -------------- LISTADO FUNCIONES ----------------
def p_funciones_lista(t):
    'funciones      :  funciones funcion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_funciones_funcion(t):
    'funciones      : funcion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

# ------------------ FUNCION -----------------
def p_funcion(t):
    '''funcion      : RFUNC ID PARIZQ PARDER LLAVIZQ instrucciones LLAVDER'''
    t[0] = Funcion(t[2], t[6])


def p_funcion1(t):
    '''funcion      : RFUNC RMAIN PARIZQ PARDER LLAVIZQ instrucciones LLAVDER'''
    t[0] = Funcion(t[2], t[6])


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


# -------------- INSTRUCCIONES ----------------
def p_instruccion(t):
    '''
    instruccion         : asignacion PTCOMA
                        | imprimir PTCOMA
                        | salto
                        | if_inst
                        | llamada_func PTCOMA
                        | etiqueta_instr
                        | return_instr PTCOMA
    '''
    t[0] = t[1]

# -------------- RETURN ----------------
def p_llamada_func(t):
    '''
    llamada_func            : ID PARIZQ PARDER
    '''
    t[0] = LLamFuncion(t[1], t.lineno(1))

# -------------- RETURN ----------------
def p_return(t):
    '''
    return_instr            : RRETURN
    '''
    t[0] = Return(t.lineno(1))

# -------------- ETIQUETA ----------------
def p_etiqueta(t):
    '''
    etiqueta_instr            : ID DOSPTS
    '''
    t[0] = Etiqueta(t[1], t.lineno(1))

# -------------- IF ----------------
def p_if(t):
    '''
    if_inst            : RIF expresion LLAVIZQ salto LLAVDER
    '''
    t[0] = If(t[2], t[4], t.lineno(1))

# -------------- SALTO ----------------
def p_salto(t):
    '''
    salto            : RGOTO ID PTCOMA
    '''
    t[0] = Salto(t[2], t.lineno(1))

# -------------- IMPRIMIR ----------------
def p_imprimir(t):
    '''
    imprimir            : RFMT PUNTO RPRINT PARIZQ CADENA COMA expresion PARDER
    '''
    t[0] = Imprimir(t[5], t[7], t.lineno(1))

# -------------- ASIGNACIONES ----------------
def p_asignacion_exp(t):
    '''
    asignacion          : expresion IGUAL expresion MAS expresion
                        | expresion IGUAL expresion MENOS expresion
                        | expresion IGUAL expresion POR expresion
                        | expresion IGUAL expresion DIV expresion
    '''
    t[0] = Asignacion(t[1], Expresion(t[3], t[4], t[5]), t.lineno(2))

def p_asignacion_exp1(t):
    '''
    asignacion          : expresion IGUAL expresion
    '''
    t[0] = Asignacion(t[1], t[3], t.lineno(2))

def p_asignacion_exp2(t):
    '''
    asignacion          : expresion IGUAL RSTACK CORIZQ RINT PARIZQ expresion PARDER CORDER
                        | expresion IGUAL RHEAP CORIZQ RINT PARIZQ expresion PARDER CORDER
    '''
    t[0] = Asignacion(t[1], t[3] + t[4] + t[5] + t[6] + t[7] + t[8] + t[9], t.lineno(2))

def p_asignacion_exp3(t):
    '''
    asignacion          : RSTACK CORIZQ RINT PARIZQ expresion PARDER CORDER IGUAL expresion
                        | RHEAP CORIZQ RINT PARIZQ expresion PARDER CORDER IGUAL expresion
    '''
    t[0] = Asignacion(t[1] + t[2] + t[3] + t[4] + t[5] + t[6] + t[7], t[9], t.lineno(1))

def p_asignacion_exp5(t):
    '''
    asignacion          : expresion IGUAL RMATH PUNTO RMOD PARIZQ expresion COMA expresion PARDER
    '''
    t[0] = Asignacion(t[1], t[3] + t[4] + t[5] + t[6] + str(t[7]) + t[8] + str(t[9]) + t[10], t.lineno(2))

# -------------- EXPRESIONES ----------------
def p_expresiones(t):
    '''
    expresion       : DECIMAL
                    | ENTERO
                    | RP
                    | RH
                    | ID
    '''
    t[0] = t[1]

def p_expresiones2(t):
    '''
    expresion           : expresion MAYOR expresion
                        | expresion MAYORIGUAL expresion
                        | expresion MENOR expresion
                        | expresion MENORIGUAL expresion
                        | expresion IGUALDAD expresion
                        | expresion DIFERENTE expresion
    '''
    t[0] = Comparacion(t[1], t[2], t[3], t.lineno(2))

def p_expresiones1(t):
    '''
    expresion       : RINT PARIZQ expresion PARDER
    '''
    t[0] = t[1] + "(" + str(t[3]) + ")"

def p_expresion_unaria_aritmetica(t):
    'expresion          :   MENOS expresion %prec UMENOS'
    t[0] = "-" + str(t[2])

# -------------- GENERAR PARSER ----------------
import ply.yacc as yacc
parser = yacc.yacc()

def parseMirilla(inp):
    global lexer
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    reporte = []
    instrucciones=parser.parse(inp)
    nuevoC3D = instrucciones.OptMirilla()
    return nuevoC3D