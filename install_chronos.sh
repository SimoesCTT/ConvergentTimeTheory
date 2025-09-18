#!/bin/bash
echo "Installing Chronos Compiler..."
python3 -m venv chronos_venv
source chronos_venv/bin/activate
pip install numpy scipy ply matplotlib
echo "Chronos installed successfully!"
echo "Run: python src/chronos_compiler.py"
