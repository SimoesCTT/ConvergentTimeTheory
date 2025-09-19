# File: ctt_clean_test.py
#!/usr/bin/env python3

"""Clean CTT Test without comments"""

import sys
sys.path.append('src')

from chronos_compiler import ChronosCompiler

def test_clean_ctt():
    """Test CTT without any comments"""
    compiler = ChronosCompiler()
    
    # Clean test without comments
    code = """
    timeline electron = [MINUS 1.0, 0.0, 1.0];
    timeline positron = [MINUS 1.0, 0.0, 1.0];
    electron <~ 0.0;
    positron <~ 0.0;
    electron <~ converge(positron);
    quantum_state = converge(electron);
    """
    
    print("🧪 CLEAN CTT TEST")
    print("=" * 60)
    print("Testing without comments to avoid parsing issues")
    print("=" * 60)
    
    compiler.compile(code)
    
    return True

if __name__ == "__main__":
    test_clean_ctt()
