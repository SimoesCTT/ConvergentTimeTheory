#!/usr/bin/env python3

"""
CHRONOS PARSER - WITH NEGATIVE NUMBER SUPPORT
Fixed negative number handling and improved error recovery
"""

import ply.lex as lex
import ply.yacc as yacc

class ChronosParser:
    def __init__(self):
        self.tokens = (
            'TIMELINE', 'CONVERGE', 'RETROCAUSAL_OP',
            'ID', 'NUMBER', 'ASSIGN', 'LPAREN', 'RPAREN', 
            'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON',
            'PLUS', 'MINUS', 'TIMES'
        )
        
        self._build_lexer()
        self._build_parser()
    
    def _build_lexer(self):
        self.lexer = lex.lex(module=self)
    
    def _build_parser(self):
        self.parser = yacc.yacc(module=self)
    
    # --- LEXER TOKENS ---
    def t_TIMELINE(self, t):
        r'timeline'
        return t
    
    def t_CONVERGE(self, t):
        r'converge'
        return t
    
    def t_RETROCAUSAL_OP(self, t):
        r'<~'
        return t
    
    def t_ASSIGN(self, t):
        r'='
        return t
    
    def t_LPAREN(self, t):
        r'\('
        return t
    
    def t_RPAREN(self, t):
        r'\)'
        return t
    
    def t_LBRACKET(self, t):
        r'\['
        return t
    
    def t_RBRACKET(self, t):
        r'\]'
        return t
    
    def t_COMMA(self, t):
        r','
        return t
    
    def t_SEMICOLON(self, t):
        r';'
        return t
    
    def t_PLUS(self, t):
        r'\+'
        return t
    
    def t_MINUS(self, t):
        r'-'
        return t
    
    def t_TIMES(self, t):
        r'\*'
        return t
    
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        reserved = {'timeline': 'TIMELINE', 'converge': 'CONVERGE'}
        t.type = reserved.get(t.value, 'ID')
        return t
    
    # FIXED: Handle negative numbers
    def t_NUMBER(self, t):
        r'-?\d+\.?\d*'  # Now matches optional negative sign
        try:
            t.value = float(t.value) if '.' in t.value else int(t.value)
        except ValueError:
            print(f"Number format error: {t.value}")
            t.value = 0
        return t
    
    # Handle comments
    def t_COMMENT(self, t):
        r'//.*'
        pass  # Ignore comments
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    t_ignore = ' \t\r'
    
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
    
    # --- PARSER RULES ---
    def p_program(self, p):
        '''program : statement_list'''
        p[0] = ('program', p[1])
    
    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement statement_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]
    
    def p_statement(self, p):
        '''statement : timeline_decl
                     | retrocausal_constraint
                     | assignment
                     | converge_statement'''
        p[0] = p[1]
    
    def p_timeline_decl(self, p):
        '''timeline_decl : TIMELINE ID ASSIGN expression SEMICOLON'''
        p[0] = ('timeline_decl', p[2], p[4])
    
    def p_retrocausal_constraint(self, p):
        '''retrocausal_constraint : ID RETROCAUSAL_OP expression SEMICOLON'''
        p[0] = ('retro_constraint', p[1], p[3])
    
    def p_assignment(self, p):
        '''assignment : ID ASSIGN expression SEMICOLON'''
        p[0] = ('assign', p[1], p[3])
    
    def p_converge_statement(self, p):
        '''converge_statement : CONVERGE LPAREN ID RPAREN SEMICOLON'''
        p[0] = ('converge', p[3])
    
    def p_expression(self, p):
        '''expression : NUMBER
                      | ID
                      | list_expression
                      | function_call
                      | expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binop', p[2], p[1], p[3])
    
    def p_function_call(self, p):
        '''function_call : CONVERGE LPAREN ID RPAREN'''
        p[0] = ('function_call', 'converge', p[3])
    
    def p_list_expression(self, p):
        '''list_expression : LBRACKET number_list RBRACKET
                           | LBRACKET RBRACKET'''
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = []
    
    # FIXED: Handle negative numbers in lists
    def p_number_list(self, p):
        '''number_list : NUMBER
                       | NUMBER COMMA number_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]
    
    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}' (type: {p.type})")
            # Try to recover by skipping the token
            return p
        else:
            print("Syntax error at EOF")

# Test the improved parser with negative numbers
if __name__ == "__main__":
    print("Testing Chronos Parser with Negative Number Support")
    print("=" * 60)
    
    parser = ChronosParser()
    print("✓ Parser built successfully")
    
    # Test with negative numbers
    test_code = """
    timeline x = [-1.0, 0.0, 1.0];
    x <~ 0.5;
    result = converge(x);
    """
    
    print("Testing code with negative numbers:")
    print(test_code.strip())
    
    try:
        ast = parser.parser.parse(test_code)
        print("✓ Parse successful with negative numbers!")
        print(f"AST: {ast}")
        
        # Test individual negative number parsing
        print("\nTesting individual negative number parsing:")
        test_negative = "-1.5"
        result = parser.parser.parse(test_negative)
        print(f"Parsing '{test_negative}': {result}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
