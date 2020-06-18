#!/usr/bin/python3

import ply.yacc as yacc
from dsl_lex import tokens, lexer
from language_dsl import text
import datetime
import time
import re

def get_spec(p, var):
    return p.parser.specs

def check_nested_label(spec, var):
    # expand keyword if matches
    if "search" in spec:
        for s in spec["search"]:
            for k in s["keywords"]:
                if var == k["keyword"]:
                    var = k["search"]

    # check nested
    nested = []
    if "nested" in spec:
        for doc in spec["nested"]:
            if var.startswith(doc + "."):
                nested.append(doc)
    if not nested: nested=None
    return nested, var

def doc_value(spec, var):
    value="doc['"+var+"'].value"
    if "types" in spec:
        if var in spec["types"]:
            if spec["types"][var]=="date": 
                return value+".toInstant().toEpochMilli()"
    return value

def nested_query(nested, query):
    if nested is None: return query
    for nest1 in nested:
        query = {"nested": {"path": nest1, "query": query}}
    return query

def range_dsl(spec, var, ops, number):
    (nested, var1)=check_nested_label(spec, var)
    query={"range":{var1:{ops:number}}}
    if "types" in spec:
        if var1 in spec["types"]:
            if spec["types"][var1]=="date":
                query={"range":{var1:{ops:int(number)}}}
    return nested_query(nested,query)

def painless_code(optree, params, nested):
    if "number" in optree:
        try:
            pidx = params.index(optree["number"])
        except ValueError:
            pidx = len(params)
            params.append(optree["number"])
        return nested, "params.v[" + str(pidx) + "]"

    if "var" in optree:
        (nested1, var1) = check_nested_label(optree["spec"], optree["var"])
        if nested is None: nested = nested1
        return (nested, doc_value(optree["spec"],var1))

    op = optree["op"]

    SUPPORTED_OPERATIONS = [">=", ">", "<", "<=", "==", "!=", "+", "-", "*", "/", "%"]
    if op[0] in SUPPORTED_OPERATIONS:
        (nested1, code1) = painless_code(op[1], params, nested)
        if nested is None:
            nested = nested1
        (nested2, code2) = painless_code(op[2], params, nested)
        if nested is None:
            nested = nested2
        code = code1 + op[0] + code2
        return (nested, code)
    if op[0] == "()":
        (nested1, code1) = painless_code(op[1], params, nested)
        if nested is None:
            nested = nested1
        code = '(' + code1 + ')'
        return (nested, code)
    if op[0] == "bool":
        (nested1, code) = painless_code(op[1], params, nested)
        if nested is None:
            nested = nested1
        return (nested, code)

def painless_query(optree):
    params = []
    (nested, code) = painless_code(optree, params, None)
    return nested_query(nested, {"script": {"script": {"lang": "painless", "source": code, "params": {"v": params}}}})

start = 'query'
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQUAL', 'NOTEQUAL', 'CONTAINS'),
    ('nonassoc', 'GREATEREQUAL', 'GREATERTHAN', 'LESSEQUAL', 'LESSTHAN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'REMAINDER'),
    ('left', 'NOT'),
    ('left', 'LPAREN', 'RPAREN'),
    ('nonassoc', 'LBRACKET', 'RBRACKET', 'COMMA'),
    ('right', 'UMINUS'),
)

def p_expr_plus(p):
    """expr : expr PLUS term"""
    if "number" in p[1] and "number" in p[3]:
        p[0] = {"number": p[1]["number"] + p[3]["number"]}
    else:
        p[0] = {"op": ["+", p[1], p[3]]}

def p_expr_minus(p):
    """expr : expr MINUS term"""
    if "number" in p[1] and "number" in p[3]:
        p[0] = {"number": p[1]["number"] - p[3]["number"]}
    else:
        p[0] = {"op": ["-", p[1], p[3]]}

def p_expr_term(p):
    """expr : term"""
    p[0]=p[1]

def p_term_multiply(p):
    """term : term MULTIPLY factor"""
    if "number" in p[1] and "number" in p[3]:
        p[0] = {"number": p[1]["number"] * p[3]["number"]}
    else:
        p[0] = {"op": ["*", p[1], p[3]]}

def p_term_divide(p):
    """term : term DIVIDE factor"""
    if "number" in p[1] and "number" in p[3]:
        if p[3]["number"] == 0:
            raise Exception(text["math error"].format(p[1]["number"],p[3]["number"]))
        p[0] = {"number": p[1]["number"] / p[3]["number"]}
    else:
        p[0] = {"op": ["/", p[1], p[3]]}

def p_term_reminder(p):
    """term : term REMAINDER factor"""
    if "number" in p[1] and "number" in p[3]:
        p[0] = {"number": p[1]["number"] % p[3]["number"]}
    else:
        p[0] = {"op": ["%", p[1], p[3]]}

def p_term_factor(p):
    """term : factor"""
    p[0]=p[1]

def p_factor_uminus(p):
    """factor : MINUS NUMBER %prec UMINUS"""
    p[0] = {"number": -p[2]}

def p_factor_number(p):
    """factor : NUMBER"""
    p[0] = {"number": p[1]}

def p_factor_date(p):
    """factor : DATE"""
    p[0] = { "number": p[1] }

def p_factor_time(p):
    """factor : time"""
    p[0] = { "number": p[1] }

def p_datetime_date_time(p):
    """factor : DATE time"""
    today=int(time.mktime(datetime.date.today().timetuple())*1000)
    p[0] = {"number": p[1]+p[2]-today}

def p_factor_now(p):
    """factor : NOW"""
    p[0] = {"number": p[1]}

def p_time_time(p):
    """time : TIME"""
    p[0] = p[1]

def p_time_am(p):
    """time : TIME AM"""
    p[0] = p[1]
    dt=datetime.datetime.fromtimestamp(p[1]/1000)
    if dt.hour>12 or dt.hour==0: raise Exception(text["syntax error"].format("AM"))
    if dt.hour==12: p[0]=p[0]-12*3600*1000

def p_time_pm(p):
    """time : TIME PM"""
    p[0] = p[1]
    dt=datetime.datetime.fromtimestamp(p[1]/1000)
    print(dt)
    if dt.hour==0 or dt.hour>12: raise Exception(text["syntax error"].format("PM"))
    if dt.hour!=12: p[0]=p[0]+p[2]

def p_factor_variable(p):
    """factor : VAR"""
    p[0] = {"var": str(p[1]["name"]), "spec": get_spec(p,p[1])}

def p_factor_parened(p):
    """factor : LPAREN expr RPAREN"""
    if "number" in p[2]:
        p[0] = p[2]
    else:
        p[0] = {"op": ["()", p[2]]}

def p_query_geo_within(p):
    """query : VAR CONTAINS LBRACKET expr COMMA expr RBRACKET"""
    if "number" not in p[4]: raise Exception(text["syntax error"].format(p[4]))
    if "number" not in p[6]: raise Exception(text["syntax error"].format(p[6]))
    (nested, var) = check_nested_label(get_spec(p,p[1]), p[1]["name"])
    p[0]=nested_query(nested,{"geo_distance":{"distance":100,str(var):{"lat":p[4]["number"],"lon":p[6]["number"]}}})

def p_query_geo_within_distance(p):
    """query : VAR CONTAINS LBRACKET expr COMMA expr COMMA expr RBRACKET"""
    if "number" not in p[4]: raise Exception(text["syntax error"].format(p[4]))
    if "number" not in p[6]: raise Exception(text["syntax error"].format(p[6]))
    if "number" not in p[8]: raise Exception(text["syntax error"].format(p[8]))
    (nested, var) = check_nested_label(get_spec(p,p[1]), p[1]["name"])
    p[0]=nested_query(nested,{"geo_distance":{"distance":p[8]["number"],str(var):{"lat":p[4]["number"],"lon":p[6]["number"]}}})

def p_query_var_matches_all(p):
    """query : VAR CONTAINS MULTIPLY"""
    (nested, var)=check_nested_label(get_spec(p,p[1]), p[1]["name"])
    p[0] = nested_query(nested, { "exists": { "field": var }})
    
def p_query_var_contains_string(p):
    """query : VAR CONTAINS STRING"""
    (nested, var) = check_nested_label(get_spec(p,p[1]), p[1]["name"])
    value = re.sub(r"[^A-Za-z0-9_\*.]", ' +', str(p[3]))
    p[0] = nested_query(nested,{"simple_query_string":{"fields":[var],"query":value}})

def p_query_gte(p):
    """query : expr GREATEREQUAL expr"""
    if "number" in p[1] and "number" in p[3]:
        if p[1]["number"] >= p[3]["number"]:
            p[0]= { "match_all": {} }
        else:
            p[0]= { "match_none": {} }
    elif "var" in p[1] and "number" in p[3]:
        p[0] = range_dsl(p[1]["spec"], p[1]["var"], "gte", p[3]["number"])
    else:
        p[0] = painless_query({"op": [">=", p[1], p[3]]})

def p_query_gt(p):
    """query : expr GREATERTHAN expr"""
    if "number" in p[1] and "number" in p[3]:
        if p[1]["number"] > p[3]["number"]:
            p[0]= { "match_all": {} }
        else:
            p[0]= { "match_none": {} }
    elif "var" in p[1] and "number" in p[3]:
        p[0] = range_dsl(p[1]["spec"], p[1]["var"], "gt", p[3]["number"])
    else:
        p[0] = painless_query({"op": [">", p[1], p[3]]})

def p_query_lte(p):
    """query : expr LESSEQUAL expr"""
    if "number" in p[1] and "number" in p[3]:
        if p[1]["number"] <= p[3]["number"]:
            p[0]= { "match_all": {} }
        else:
            p[0]= { "match_none": {} }
    elif "var" in p[1] and "number" in p[3]:
        p[0] = range_dsl(p[1]["spec"], p[1]["var"], "lte", p[3]["number"])
    else:
        p[0] = painless_query({"op": ["<=", p[1], p[3]]})

def p_query_lt(p):
    """query : expr LESSTHAN expr"""
    if "number" in p[1] and "number" in p[3]:
        if p[1]["number"] < p[3]["number"]:
            p[0]= { "match_all": {} }
        else:
            p[0]= { "match_none": {} }
    elif "var" in p[1] and "number" in p[3]:
        p[0] = range_dsl(p[1]["spec"], p[1]["var"], "lt", p[3]["number"])
    else:
        p[0] = painless_query({"op": ["<", p[1], p[3]]})

def p_query_eq(p):
    """query : expr EQUAL expr"""
    if "number" in p[1] and "number" in p[3]:
        if p[1]["number"] == p[3]["number"]:
            p[0]= { "match_all": {} }
        else:
            p[0]= { "match_none": {} }
    elif "var" in p[1] and "number" in p[3]:
        (nested, var) = check_nested_label(p[1]["spec"], p[1]["var"])
        p[0] = nested_query(nested, {"term": {var: p[3]["number"]}})
    else:
        p[0] = painless_query({"op": ["==", p[1], p[3]]})

def p_query_eq_boolean(p):
    """query : expr EQUAL BOOLEAN"""
    if "var" not in p[1]: raise Exception(text["var first"])
    (nested, var) = check_nested_label(p[1]["spec"], p[1]["var"])
    p[0] = nested_query(nested, {"term": { var: True } })
    if not p[3]: p[0] = {"bool": { "must_not": p[0] } }
        
def p_query_eq_string(p):
    """query : expr EQUAL STRING"""
    if "var" not in p[1]: raise Exception(text["var first"])
    (nested, var) = check_nested_label(p[1]["spec"], p[1]["var"])
    if var == "_id":
        p[0] = { "ids": { "values": [ p[3] ] }}
    else:
        p[0] = nested_query(nested, {"term": { var+".keyword": p[3] } })
    
def p_query_eq_ip(p):
    """query : expr EQUAL IP"""
    if "var" not in p[1]: raise Exception(text["var first"])
    (nested, var) = check_nested_label(p[1]["spec"], p[1]["var"])
    p[0] = nested_query(nested, {"term": { var: p[3] } })
    
def p_query_eq_all(p):
    """query : expr EQUAL MULTIPLY"""
    if "var" not in p[1]: raise Exception(text["var first"])
    (nested, var)=check_nested_label(p[1]["spec"], p[1]["var"])
    p[0] = nested_query(nested, { "exists": { "field": var }})
    
def p_query_neq(p):
    """query : expr NOTEQUAL expr"""
    if "number" in p[1] and "number" in p[3]:
        if p[1]["number"] != p[3]["number"]:
            p[0]= { "match_all": {} }
        else:
            p[0]= { "match_none": {} }
    elif "var" in p[1] and "number" in p[3]:
        (nested, var) = check_nested_label(p[1]["spec"], p[1]["var"])
        p[0] = nested_query(nested, {"bool": {"must_not": {"term": {var: p[3]["number"]}}}})
    else:
        p[0] = painless_query({"op": ["!=", p[1], p[3]]})

def p_query_neq_boolean(p):
    """query : expr NOTEQUAL BOOLEAN"""
    if "var" not in p[1]: raise Exception(text["var!=boolean only"])
    (nested, var) = check_nested_label(p[1]["spec"], p[1]["var"])
    p[0] = nested_query(nested, {"term": { var: True } })
    if p[3]: p[0] = {"bool": { "must_not": p[0] } }
        
def p_query_and(p):
    """query : query AND query"""
    p[0] = {"bool": {"must": [p[1], p[3]]}}

def p_query_or(p):
    """query : query OR query"""
    p[0] = {"bool": {"should": [p[1], p[3]]}}

def p_query_not(p):
    """query : NOT query"""
    p[0] = {"bool": {"must_not": [p[2]]}}

def p_query_parened(p):
    """query : LPAREN query RPAREN"""
    p[0] = p[2]

def p_error(p):
    if p is None:
        raise Exception(text["unexpected eol"])
    raise Exception(text["syntax error"].format(p.value))

parser = yacc.yacc(tabmodule='dsl_yacc_tab', debug=1, optimize=0, write_tables=False)

def compile(queries,specs={}):
    parser.specs = specs
    dsl = parser.parse(queries, lexer=lexer)
    if dsl is None: dsl = {"match_none":{}}
    return dsl

if __name__ == '__main__':
    import json

    while True:
        s = None
        try:
            s = input('dsl > ')
        except EOFError:
            break
        if not s:
            continue

        print(json.dumps(compile(s,specs={"types":{"time":"date"}})))
