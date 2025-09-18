#!/usr/bin/env python3

"""
Basic test for Chronos compiler with list support
"""

import sys
sys.path.append('src')

from chronos_compiler import ChronosCompiler

def test_basic():
    """Test basic functionality with lists"""
    print("Testing Chronos Compiler with List Support")
    print("=" * 50)
    
    compiler = ChronosCompiler()
    
    # Test with list
    code = """
    timeline values = [1, 2, 3, 4, 5];
    values <~ 3.2;
    result = converge(values);
    """
    
    compiler.compile(code)

if __name__ == "__main__":
    test_basic()
