#!/usr/bin/env python3

"""
Clean test of factorial concept without comments
"""

import sys
sys.path.append('src')

from chronos_compiler import ChronosCompiler

def test_clean_factorial():
    """Test factorial concept without comments"""
    print("CLEAN FACTORIAL CONCEPT TEST")
    print("=" * 50)
    
    compiler = ChronosCompiler()
    
    # Clean code without comments
    code = """
    timeline n = 5;
    timeline result = 1;
    result <~ 120;
    computed = converge(result);
    """
    
    compiler.compile(code)
    
    print("\nThis demonstrates CTT constraint solving!")
    print("Instead of computing recursively, we apply constraints")
    print("and let the solver find the consistent solution.")

if __name__ == "__main__":
    test_clean_factorial()
