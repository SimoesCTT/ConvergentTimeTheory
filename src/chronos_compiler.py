#!/usr/bin/env python3

"""
CHRONOS COMPILER - IMPROVED CONSTRAINT HANDLING
Better handling of constraint solving and error reporting
"""

import numpy as np
from scipy.optimize import minimize
from parser_implementation import ChronosParser

class ChronosCompiler(ChronosParser):
    def __init__(self):
        super().__init__()
        self.timelines = {}
        self.constraints = []
        self.current_scope = {}
    
    # CTT Engine Methods
    def declare_timeline(self, var_name, value):
        """Create a timeline variable"""
        print(f"Creating timeline {var_name} = {value}")
        
        if not isinstance(value, list):
            value = [value]
        
        self.timelines[var_name] = np.array(value)
        # Create Gaussian weights
        xi = np.linspace(-3, 3, len(value))
        weights = np.exp(-xi**2)
        self.timelines[var_name + '_weights'] = weights / np.sum(weights)
    
    def add_constraint(self, var_name, target_value):
        """Add a retrocausal constraint"""
        print(f"Adding constraint: {var_name} <~ {target_value}")
        self.constraints.append(('constraint', var_name, target_value))
    
    def converge_function(self, var_name):
        """Execute the converge function"""
        print(f"Executing converge({var_name})")
        if var_name in self.timelines:
            values = self.timelines[var_name]
            weights = self.timelines[var_name + '_weights']
            result = np.sum(values * weights)
            print(f"Converging {var_name}: {values} -> {result:.3f}")
            return result
        elif var_name in self.current_scope:
            return self.current_scope[var_name]
        else:
            print(f"Warning: Variable {var_name} not found")
            return 0
    
    def solve_constraints(self):
        """Solve all retrocausal constraints"""
        if not self.constraints:
            print("No constraints to solve")
            return
            
        print(f"Solving {len(self.constraints)} constraints...")
        
        variables_to_solve = set()
        for constr in self.constraints:
            variables_to_solve.add(constr[1])
        
        initial_guess = {}
        for var_name in variables_to_solve:
            if var_name in self.timelines:
                initial_guess[var_name] = np.mean(self.timelines[var_name])
            elif var_name in self.current_scope:
                initial_guess[var_name] = self.current_scope[var_name]
            else:
                initial_guess[var_name] = 0
                print(f"Warning: Constrained variable {var_name} not found in timelines or scope")
        
        def loss_function(current_values):
            total_error = 0
            values_dict = {}
            for i, var_name in enumerate(initial_guess.keys()):
                values_dict[var_name] = current_values[i]
            
            for constr in self.constraints:
                _, var_name, target = constr
                current_val = values_dict[var_name]
                total_error += (current_val - target)**2
            return total_error
            
        if initial_guess:
            try:
                initial_guess_list = list(initial_guess.values())
                result = minimize(loss_function, initial_guess_list, method='BFGS')
                
                optimized_values = result.x
                for i, var_name in enumerate(initial_guess.keys()):
                    old_value = initial_guess[var_name]
                    new_value = optimized_values[i]
                    
                    if var_name in self.timelines:
                        self.timelines[var_name] = np.array([new_value])
                    else:
                        self.current_scope[var_name] = new_value
                    
                    print(f"Optimized {var_name}: {old_value:.3f} -> {new_value:.3f}")
            except Exception as e:
                print(f"Constraint solving failed: {e}")
    
    def evaluate_expression(self, expr):
        """Evaluate an expression"""
        if isinstance(expr, (int, float)):
            return expr
        elif isinstance(expr, str):
            # Variable reference
            if expr in self.current_scope:
                return self.current_scope[expr]
            elif expr in self.timelines:
                return np.mean(self.timelines[expr])
            else:
                print(f"Warning: Variable {expr} not found")
                return 0
        elif isinstance(expr, list):
            return expr
        elif isinstance(expr, tuple):
            if expr[0] == 'binop':
                op, left, right = expr[1], expr[2], expr[3]
                left_val = self.evaluate_expression(left)
                right_val = self.evaluate_expression(right)
                
                if op == '+': return left_val + right_val
                elif op == '-': return left_val - right_val
                elif op == '*': return left_val * right_val
            elif expr[0] == 'function_call':
                func_name, arg = expr[1], expr[2]
                if func_name == 'converge':
                    return self.converge_function(arg)
        return 0
    
    def execute_ast(self, ast):
        """Execute the abstract syntax tree"""
        if ast is None:
            print("Error: AST is None - parsing failed")
            return
            
        if ast[0] == 'program':
            for stmt in ast[1]:
                self.execute_ast(stmt)
        elif ast[0] == 'timeline_decl':
            _, var_name, expr = ast
            value = self.evaluate_expression(expr)
            self.declare_timeline(var_name, value)
        elif ast[0] == 'retro_constraint':
            _, var_name, target_expr = ast
            target_value = self.evaluate_expression(target_expr)
            self.add_constraint(var_name, target_value)
        elif ast[0] == 'assign':
            _, var_name, expr = ast
            value = self.evaluate_expression(expr)
            self.current_scope[var_name] = value
            print(f"Assigned {var_name} = {value}")
        elif ast[0] == 'converge':
            var_name = ast[1]
            result = self.converge_function(var_name)
            self.current_scope[var_name] = result
            print(f"Convergence result: {var_name} = {result}")
        else:
            print(f"Unknown AST node: {ast[0]}")
    
    def compile(self, code):
        """Compile and execute Chronos code"""
        print("Compiling Chronos program...")
        print("Code:", code.strip())
        print("-" * 50)
        
        try:
            ast = self.parser.parse(code)
            if ast is None:
                print("Error: Parsing failed - AST is None")
                return
                
            self.execute_ast(ast)
            self.solve_constraints()
            
            print("\nFinal state:")
            for var_name, value in self.current_scope.items():
                print(f"  {var_name} = {value}")
            for var_name in self.timelines:
                if '_weights' not in var_name:
                    print(f"  timeline {var_name} = {self.timelines[var_name]}")
                    
        except Exception as e:
            print(f"Compilation error: {e}")
            import traceback
            traceback.print_exc()

# Test the compiler
if __name__ == "__main__":
    compiler = ChronosCompiler()
    
    # Test with the full program
    test_code = """
    timeline x = [1, 2, 3, 4, 5];
    x <~ 3.5;
    result = converge(x);
    """
    
    print("Testing Chronos Compiler with Improved Constraint Handling")
    print("=" * 70)
    compiler.compile(test_code)
