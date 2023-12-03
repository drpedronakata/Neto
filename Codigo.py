#TENTATIVA 5
import re

# Exemplo de código Pascal simplificado
pascal_code = """
program Example;
var
  a: integer;
  b: integer = 5;

begin
  read(a);
  write(a,b);
  write(b);
end.
"""
pascal_code1 = """
program Example;
var
  b: integer;
  a: integer = 5;

begin
  if a > 0 then
    write(a);
    a:= a - 1;
end.
"""
pascal_code2 = """
program Example;
var
  a, b, c: integer;
  d_t: integer = 15;

var 
  d_t2: integer = 6;

begin
  a := 0;
  while a < 5 do
  begin
    read(b, d_t);
    if b == 3 then
      c := c + 1;
    a := a + 1;
  end;
  write(c);
end.
"""

OPERATORS = {
    '+': 'ADD_',
    '-': 'SUBT',
    '*': 'MULT',
    '/': 'DIVI',
    '=': 'EQUA',
    '==': 'EQUA',
    '<>': 'DIFF',
    '<': 'LETH',
    '>': 'GRTH',
    '<=': 'LEEQ',
    '>=': 'GREQ',
    'and': 'AND_',
    'or': '_OR_',
}

intermediate_code = []
variables = []

def is_valid_variable_name(variable_name):
    # Expressão regular para verificar se o nome da variável é válido
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')
    return bool(pattern.match(variable_name))

def get_variable_position(variable, variables):
    # Retorna a posicao da variavel na lista variables
    i = 0
    for var in variables:
        if variable == var:
            break
        else: i += 1
    return i

def pascal_to_intermediate(tokens):
    print(tokens)

    current_label = 1  # Começa com o label L1
    current_memory_position = 0  # Posição inicial da memória
    store_memory_position = 19

    stack_labels = []  # Usado para controlar os rótulos associados aos loops
    stack_if_labels = []  # Usado para controlar os rótulos associados aos blocos "if"

    i = 0
    j = 0

    while i < len(tokens):
        token = tokens[i]

        if token == 'program':  # Token de inicio do programa
            intermediate_code.append(f' INIP ;        Iniciando o programa {tokens[i+1]}')
        # Declaração das variaveis dentro do VAR
        if token == 'var':
            # Limite o Escopo até o begin
            while tokens[i] != 'begin':
                token = tokens[i]
                # Verifica se token é variavel
                if is_valid_variable_name(token) and (tokens[i+1] == ',' or tokens[i+1] == ':'):
                    # Guarda as variavel em lista variables
                    variables.append(token)
                # Verifica se token é numero
                elif token.isnumeric():
                    # Guarda valor do token, na memoria da variavel.
                    j = get_variable_position(tokens[i-4], variables)
                    store_memory_position = 19 - j
                    token_val = token
                    token_var = tokens[i-4]

                    intermediate_code.append(f' LDCT {token_val} ;       Valor {token_val}')
                    intermediate_code.append(f' STOR {store_memory_position} ;      M{store_memory_position} {token_var} = {token_val}')
                    intermediate_code.append(f' DUMP ')
                i += 1   
            print(variables) #VARIAVEIS CRIADAS
            print(tokens[i], i)

        elif token == ':=' :
            intermediate_code.append(f' ATRB ')
        elif token == 'read' :  # Comando de leitura ['read', '(', 'b', ',', 'c', ')', ';']
            # Limite o Escopo até o fim do READ
            while tokens[i] != ';':
                token = tokens[i]
                # Verifica se token é variable
                if token in variables:
                    # Guarda valor do token, na memoria da variavel.
                    j = get_variable_position(token, variables)
                    store_memory_position = 19 - j

                    intermediate_code.append(f' READ ;         Read({token})')
                    intermediate_code.append(f' STOR {store_memory_position} ;      M{store_memory_position} {token_var} = READ')
                    intermediate_code.append(f' DUMP ')  #PRINT DO VALOR DA VARIAVEL
                i += 1
            #intermediate_code.append(f' READ ')
        elif token == 'write' :
            # Limite o Escopo até o fim do READ
            while tokens[i] != ';':
                token = tokens[i]
                # Verifica se token é variable
                if token in variables:
                    # Guarda valor do token, na memoria da variavel.
                    j = get_variable_position(token, variables)
                    store_memory_position = 19 - j

                    intermediate_code.append(f' LDVL {store_memory_position} ;      Write({token})')
                    intermediate_code.append(f' SHOW ;         Show({token})')
                    intermediate_code.append(f' DUMP ')  #PRINT DO VALOR DA VARIAVEL
                i += 1
            #intermediate_code.append(f' WRTE ')
        elif token == 'if' :
            intermediate_code.append(f' IFFF ')
        elif token == 'while' :
            intermediate_code.append(f' WHIL ')
        elif token in OPERATORS:
            intermediate_code.append(f' OPER ')


        i += 1
    intermediate_code.append('\n')
    return '\n'.join(intermediate_code)

# Converte o código Pascal para código intermediário
tokens = re.findall(r'\b\w+\b|:=|==|<=|>=|<>|[^\w\s]', pascal_code)

intermediate_code = pascal_to_intermediate(tokens)
print(intermediate_code)