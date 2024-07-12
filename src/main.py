from collections import namedtuple
import re

Token = namedtuple('Token', ['lexeme', 'token_type', 'line', 'value'])


# Definição dos tipos de tokens
TOKEN_TYPES = {
    # Diretivas
    'program': 'DIR_PROGRAM',
    'var': 'DIR_VAR',
    'procedure': 'DIR_PROC',
    'function': 'DIR_FUNC',
    'begin': 'DIR_BEGIN',
    'end': 'DIR_END',
    'type': 'DIR_TYPE',
    'of': 'DIR_OF',
    'const': 'DIR_CONST',
    'with': 'DIR_WITH',
    # Comandos
    'if': 'STMT_IF',
    'then': 'STMT_THEN',
    'else': 'STMT_ELSE',
    'while': 'STMT_WHILE',
    'repeat': 'STMT_REPEAT',
    'for': 'STMT_FOR',
    'do': 'STMT_DO',
    'until': 'STMT_UNTIL',
    'to': 'STMT_TO',
    'downto': 'STMT_DOWNTO',
    'case': 'STMT_CASE',
    # Tipos de dados
    'array': 'TYPE_ARRAY',
    'set': 'TYPE_SET',
    'record': 'TYPE_RECORD',
    'file': 'TYPE_FILE',
    'integer': 'TYPE_INT',
    'real': 'TYPE_REAL',
    'character': 'TYPE_CHAR',
    'boolean': 'TYPE_BOOL',
    'string': 'TYPE_STRING',
    # Funções built-in
    'read': 'FN_READ',
    'readln': 'FN_READLN',
    'write': 'FN_WRITE',
    'writeln': 'FN_WRITELN',
    # Operadores
    ':=': 'OP_ATRIB',
    '+': 'OP_SUM',
    '-': 'OP_SUM',
    '*': 'OP_MUL',
    '/': 'OP_MUL',
    'div': 'OP_MUL',
    'mod': 'OP_MUL',
    '=': 'OP_REL',
    '<>': 'OP_REL',
    '<=': 'OP_REL',
    '>=': 'OP_REL',
    '>': 'OP_REL',
    '<': 'OP_REL',
    'and': 'OP_LOGIC',
    'or': 'OP_LOGIC',
    'not': 'OP_LOGIC',
    '..': 'OP_RANGE',
    # Outros operadores
    '(': 'OP_OPAR',
    ')': 'OP_CPAR',
    '[': 'OP_OBRA',
    ']': 'OP_CBRA',
    ',': 'OP_COMMA',
    ';': 'OP_EOC',
    '.': 'OP_PERIOD'
}

# Expressões regulares para identificar tokens
TOKEN_REGEX = r"""
    (?P<ID>[a-zA-Z_]\w*)|                        # Identificadores
    (?P<LIT_INT>\d+)|                            # Números inteiros
    (?P<LIT_REAL>\d+\.\d+|\d+\.\d+e[\+\-]?\d+)|  # Números de ponto flutuante
    (?P<LIT_STRING>'[^']'|"[^"]")|               # Cadeias de caracteres
    (?P<COMMENT>\(\.?\\)|\{.?\})|                # Comentários
    (?P<MULTI_LINE_COMMENT>\(\.?\*\))|     # Comentários de múltiplas linhas
    (?P<OP_ATRIB>:=)|                            # Atribuição
    (?P<OP_SUM>[+\-])|                           # Operadores aritméticos
    (?P<OP_MUL>[*/]|div|mod)|                    # Operadores aritméticos
    (?P<OP_REL>=|<>|<=|>=|>|<)|                  # Operadores relacionais
    (?P<OP_LOGIC>and|or|not)|                    # Operadores lógicos
    (?P<OP_RANGE>\.\.)|                          # Operador de range
    (?P<OP_OPAR>\()|                             # Parêntese de abertura
    (?P<OP_CPAR>\))|                             # Parêntese de fechamento
    (?P<OP_OBRA>\[)|                             # Colchete de abertura
    (?P<OP_CBRA>\])|                             # Colchete de fechamento
    (?P<OP_COMMA>,)|                             # Vírgula
    (?P<OP_EOC>;)|                               # Ponto e vírgula
    (?P<OP_PERIOD>\.)|                           # Ponto
    (?P<OP_EOL>//)|                              # Fim de linha
    (?P<OP_NIL>nil)                              # Representação de valor nulo
"""


def lexer(input_string):
    tokens = []
    line_number = 1
    for match in re.finditer(TOKEN_REGEX, input_string, re.VERBOSE | re.MULTILINE | re.DOTALL):
        token_type = next((key for key, value in match.groupdict().items() if value is not None), None)
        token_value = match.group(token_type)
        if token_type == 'COMMENT' or token_type == 'MULTI_LINE_COMMENT':
            # Ignora comentários
            pass
        elif token_type == 'OP_EOL':
            # Incrementa o número da linha
            line_number += 1
        else:
            # Adiciona o token à lista de tokens
            tokens.append({
                'value': token_value,
                'type': TOKEN_TYPES[token_type],
                'line_number': line_number
            })
    return tokens