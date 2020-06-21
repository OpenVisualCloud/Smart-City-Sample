#!/usr/bin/python3

import datetime
import time
import ply.lex as lex
from language_dsl import text

tokens=('VAR','LPAREN','RPAREN','AND','OR','NOT','NUMBER','STRING', 'DATE', 'TIME',
        'CONTAINS','LESSEQUAL','LESSTHAN','GREATEREQUAL','GREATERTHAN',
        'EQUAL','NOTEQUAL','PLUS','MINUS','MULTIPLY','DIVIDE','REMAINDER',
        'NOW','BOOLEAN','COMMA','LBRACKET','RBRACKET','AM', 'PM', 'IP')

def t_TIME(t):
    r'[0-2]?\d:[0-5]?\d:[0-5]?\d\.?\d*'
    today=datetime.date.today()
    dt=None
    for format1 in ["%H:%M:%S.%f","%H:%M:%S"]:
        try:
            dt = datetime.datetime.strptime(str(today)+" "+t.value, "%Y-%m-%d "+format1)
            break
        except:
            pass
    if dt is None: raise Exception(text["syntax error"].format(t.value))
    t.value = int(time.mktime(dt.timetuple())*1000+dt.microsecond)
    return t

def t_AM(t):
    r'[Aa][Mm]'
    t.value=0
    return t

def t_PM(t):
    r'[Pp][Mm]'
    t.value=12*3600*1000
    return t

def t_DATE(t):
    r'[01]\d/[0-3]\d/\d\d\d\d'
    dt = datetime.datetime.strptime(t.value,"%m/%d/%Y")
    t.value = int(time.mktime(dt.timetuple())*1000)
    return t

def t_NOW(t):
    r'[Nn][Oo][Ww]'
    t.value = int(time.time()*1000)
    return t

def t_IP(t):
    r'[12]?[0-9]?[0-9]\.[12]?[0-9]?[0-9]\.[12]?[0-9]?[0-9]\.[12]?[0-9]?[0-9](\/[123]?[0-9])?'
    return t

def t_NUMBER(t):
    r'[0-9]*\.?[0-9]+'
    t.value = float(t.value)
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'\-'
    return t

def t_MULTIPLY(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'\/'
    return t

def t_REMAINDER(t):
    r'\%'
    return t

def t_EQUAL(t):
    r'==?'
    return t

def t_LESSEQUAL(t):
    r'<='
    return t

def t_LESSTHAN(t):
    r'<'
    return t

def t_GREATEREQUAL(t):
    r'>='
    return t

def t_GREATERTHAN(t):
    r'>'
    return t

def t_AND(t):
    r'(\&\&?|[Aa][Nn][Dd])'
    return t

def t_OR(t):
    r'(\|\|?|[oO][rR])'
    return t

def t_NOTEQUAL(t):
    r'\!='
    return t

def t_NOT(t):
    r'(\!|[Nn][Oo][Tt])'
    return t

def t_BOOLEAN(t):
    r'([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])'
    if str(t.value).lower()=='true':
        t.value=True
    else:
        t.value=False
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_\.0-9]*'
    t.value={ "name": t.value }
    return t

t_ignore = ' \t'

def t_CONTAINS(t):
    r'\:'
    return t

def t_COMMA(t):
    r','
    return t

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

def t_STRING(t):
    r'(\'[^\']*\'|"[^"]*")'
    t.value=str(t.value)[1:-1]
    return t

def t_error(t):
    raise Exception(text["syntax error"].format(t.value))

lexer = lex.lex(debug=0, optimize=0, lextab='dsl_lex_tab')

if __name__ == '__main__':
    while True:
        s = None
        try:
            s = input('dsl > ')
        except EOFError:
            break
        if not s:
            continue
        lexer.input(s)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
