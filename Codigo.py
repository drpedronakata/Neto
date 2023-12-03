""" 
Leonardo Franco de Oliveira Marques – 2823671
Luiz Felipe Silva Santos – 1402342
Milton Manuel Coelho Ramos – 9838805
Pedro Henrique Nakata – 9970141
Pedro Leandro de Andrade Cruz - 2478271 
"""

"""
No Slide está o GTIF, mas o asmr não reconhece o comando.
O comando que ele aceita é GOIF.

O Li: NOPE não é muito explicado seu uso com o GOTO e GOIF....
Pensei que Li fosse linha do codigo, mas é uma LABEL.

GOIF foi dificil compreender pelo Slide, caso 1, ele continua, caso 0 ele vai para o Li

INVI não funcionou nos meu testes.
"""

import re

# Exemplo de código Pascal simplificado
pascal_code000 = """
program Example;
var
  a: integer;
  b: integer = -5;

begin
  read(a);
  b := 2;
  b := a * b;
  write(b);
end.
"""
pascal_code100 = """
program Example;
var
  b: integer;
  a: integer = 5;

begin
  if  a > 0 then
    begin
    write(a);
    a := a * -1;
    end;
  write(a);
end.
"""
pascal_code = """
program Example;
var
  a, b, c: integer;
  d_t: integer = 15;

var 
  d_t2: integer = 6;

begin
  a := 0;
  while a <= 1 do
  begin
    read(b, c);
    if b != c then
      c := c + dt;
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

# Variaveis Globais
intermediate_code = []
variables = []
current_line =  1 # Começa com o label L1
current_memory = 0  # Posição inicial da memória


def is_valid_variable_name(variable_name):
    # Expressão regular para verificar se o nome da variável é válido
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')
    return bool(pattern.match(variable_name))

def is_valid_number(variable_name):
    # Substituio o isnumeric(), pois ele não pega negativos
    pattern = re.compile(r'^[+-]?\d+$')
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
    global current_line
    store_memory_position = 19

    stack_labels = []  # Usado para controlar os rótulos associados aos loops

    i = 0
    j = 0

    while i < len(tokens):
        token = tokens[i]

        if token == 'program' : # Token de inicio do programa
            intermediate_code.append(f' INIP ;          Iniciando o programa {tokens[i+1]}')
            current_line = current_line + 1
        if token == 'var' : # Declaração das variaveis dentro do VAR
            # Limite o Escopo até o begin
            while tokens[i] != 'begin':
                token = tokens[i]
                # Verifica se token é variavel
                if is_valid_variable_name(token) and (tokens[i+1] == ',' or tokens[i+1] == ':'):
                    # Guarda as variavel em lista variables
                    variables.append(token)
                # Verifica se token é numero
                elif is_valid_number(token):
                    # Guarda valor do token, na memoria da variavel.
                    j = get_variable_position(tokens[i-4], variables)
                    store_memory_position = 19 - j
                    token_val = token
                    token_var = tokens[i-4]

                    intermediate_code.append(f' LDCT {token_val} ;        Write({token_val})')
                    current_line += 1
                    intermediate_code.append(f' STOR {store_memory_position} ;        M{store_memory_position} {token_var} = {token_val}')
                    current_line += 1
                    intermediate_code.append(f' DUMP ;          L{current_line}') #PRINT DO VALOR DA VARIAVEL
                    current_line += 1
                i += 1   
            print(f'\nVARIAVEIS = {variables}') #VARIAVEIS CRIADAS

        elif token == ':=' :
            expression_tokens = []
            token_var = tokens[i-1]
            i += 1

            # Pega expressao dentro de :=
            while  i < len(tokens) and tokens[i] != ';':
                expression_tokens.append(tokens[i])
                i += 1

            # Caso a expressao for maior que 1, ela ira chamar o comando de OPERACOES dentro de pascal_to_intermediate
            if len(expression_tokens) == 1:
                token =  expression_tokens[0]
                 # Caso o token é variavel
                if token in variables:
                    j = get_variable_position(token, variables)
                    store_memory_position = 19 - j
                    intermediate_code.append(f' LDVL {store_memory_position} ;        Write({token})')
                    current_line += 1
                # Caso o token é numero
                else:
                    intermediate_code.append(f' LDCT {token} ;        Write({token})')
                    current_line += 1
            else:
                pascal_to_intermediate(expression_tokens)
                token = 'OPER'
                #print("TESTE" , pascal_to_intermediate(expression_tokens))
                #print('\n')

            # Atribuir valor a variavel
            j = get_variable_position(token_var, variables)
            store_memory_position = 19 - j
            intermediate_code.append(f' STOR {store_memory_position} ;        M{store_memory_position} {token_var} = {token}')
            current_line += 1
            intermediate_code.append(f' DUMP ;          L{current_line}')  #PRINT DO VALOR DA VARIAVEL
            current_line += 1
        elif token == 'read' : # Comando de leitura ['read', '(', 'b', ',', 'c', ')', ';']
            # Limite o Escopo até o fim do READ
            while tokens[i] != ';':
                token = tokens[i]
                # Verifica se token é variable
                if token in variables:
                    # Guarda valor do token, na memoria da variavel.
                    j = get_variable_position(token, variables)
                    store_memory_position = 19 - j

                    intermediate_code.append(f' READ ;          Read({token})')
                    current_line += 1
                    intermediate_code.append(f' STOR {store_memory_position} ;        M{store_memory_position} {token} = READ')
                    current_line += 1
                    intermediate_code.append(f' DUMP ;          L{current_line}')  #PRINT DO VALOR DA VARIAVEL
                    current_line += 1
                i += 1
        elif token == 'write' : # Comando de Escrita ['write', '(', 'a', ',', 'b', ')', ';]
            # pLimite o Escoo até o fim do WRITE
            while tokens[i] != ';':
                token = tokens[i]
                # Verifica se token é variable
                if token in variables:
                    # Guarda valor do token, na memoria da variavel.
                    j = get_variable_position(token, variables)
                    store_memory_position = 19 - j

                    intermediate_code.append(f' LDVL {store_memory_position} ;        Write({token})')
                    current_line += 1
                    intermediate_code.append(f' SHOW ;          Show({token})')
                    current_line += 1
                i += 1
        elif token == 'if' :
            expression_tokens = []
            token_var = tokens[i-1]
            i += 1

            # Pegar expressao dentro do IF
            while tokens[i] != 'then':
                expression_tokens.append(tokens[i])
                i += 1

            # Caso a expressao for maior que 1, chama OPERACOES, 
            if len(expression_tokens) == 1:
                token =  expression_tokens[0]
                 # Caso o token é variavel
                if token in variables:
                    j = get_variable_position(token, variables)
                    store_memory_position = 19 - j
                    intermediate_code.append(f' LDVL {store_memory_position} ;        Write({token})')
                    current_line += 1
                # Caso o token é numero
                else:
                    intermediate_code.append(f' LDCT {token} ;        Write({token})')
                    current_line += 1
            else:
                pascal_to_intermediate(expression_tokens)
                token = 'OPER'

            # Adicionar o GOIF Li, e salvar a Li para depois.
            intermediate_code.append(f' GOIF L{current_line} ; ')
            stack_labels.append(current_line)
            current_line += 1

            # Pegar bloco dentro do IF
            expression_tokens = []
            i += 1
            if tokens[i] == 'begin':
                while tokens[i] != 'end':
                    expression_tokens.append(tokens[i])
                    i += 1
            else:
                while tokens[i] != ';':
                    expression_tokens.append(tokens[i])
                    i += 1
            # Envia o bloco IF a funcao de comandos
            pascal_to_intermediate(expression_tokens)

            # Adiciona a Li: NOPE do GOIF Li
            token = stack_labels.pop()
            intermediate_code.append(f'L{token}: NOPE ;       Label do IF') 
            current_line += 1   
        elif token == 'while' :
            # Adicionar o Li no inicio do WHILE
            intermediate_code.append(f'L{current_line}: NOPE ;       Label_B do WHILE L{token}')
            stack_labels.append(current_line)

            expression_tokens = []
            token_var = tokens[i-1]
            i += 1
            # Pegar expressao dentro do WHILE
            while tokens[i] != 'do':
                expression_tokens.append(tokens[i])
                i += 1

            # Caso a expressao for maior que 1, chama OPERACOES, 
            if len(expression_tokens) == 1:
                token =  expression_tokens[0]
                 # Caso o token é variavel
                if token in variables:
                    j = get_variable_position(token, variables)
                    store_memory_position = 19 - j
                    intermediate_code.append(f' LDVL {store_memory_position} ;        Write({token})')
                    current_line += 1
                # Caso o token é numero
                else:
                    intermediate_code.append(f' LDCT {token} ;        Write({token})')
                    current_line += 1
            else:
                pascal_to_intermediate(expression_tokens)
                token = 'OPER'

            # Adicionar o GOIF Li, e salvar a Li para depois.
            intermediate_code.append(f' GOIF L{current_line} ; ')
            stack_labels.append(current_line)
            current_line += 1

            # Pegar bloco dentro do IF
            expression_tokens = []
            i += 1
            if tokens[i] == 'begin':
                while tokens[i] != 'end':
                    expression_tokens.append(tokens[i])
                    i += 1
            else:
                while tokens[i] != ';':
                    expression_tokens.append(tokens[i])
                    i += 1
            # Envia o bloco IF a funcao de comandos
            pascal_to_intermediate(expression_tokens)
            
            #Adiciona o GOTO Li, para voltar ao incio do WHILE.
            intermediate_code.append(f' GOTO L{stack_labels[0]} ; ')
            current_line += 1
            # Adiciona a Li: NOPE do GOIF Li
            intermediate_code.append(f'L{stack_labels[1]}: NOPE ;       Label do IF') 
            current_line += 1   
        elif token in OPERATORS : # Comando para expressoes [c', '+', '1', ';]  
            # Adiciona os token na operação em uma lista temporaria
            temp_tokens = [tokens[i-1], tokens[i+1]]
            
            for token1 in temp_tokens:
                # Caso o token é variavel
                if token1 in variables:
                    j = get_variable_position(token1, variables)
                    store_memory_position = 19 - j
                    intermediate_code.append(f' LDVL {store_memory_position} ;        Write({token1})')
                    current_line += 1
                # Caso o token é numero
                elif is_valid_number(token1):
                    intermediate_code.append(f' LDCT {token1} ;        Write({token1})')
                    current_line += 1
            # Adiciona a Operacao no Final
            intermediate_code.append(f' {OPERATORS[token]} ;          ({tokens[i-1]} {tokens[i]} {tokens[i+1]})')
            current_line += 1
            intermediate_code.append(f' DUMP ;          L{current_line}')  #PRINT DO VALOR DA VARIAVEL
            current_line += 1
            i += 1
        i += 1
    return '\n'.join(intermediate_code)

# Converte o código Pascal para código intermediário
tokens = re.findall(r'\b\w+\b|:=|==|<=|>=|<>|-\d+|[^\w\s]', pascal_code)
print(f'\nTOKEN = {tokens}')

intermediate_code.append("\n'''")
intermediate_code = pascal_to_intermediate(tokens)
intermediate_code = intermediate_code + "\n\n'''"
print(intermediate_code)