"""
run.py — Quick Start Runner
=============================
AI Engineering Roadmap 2026 · Episode 3

The simplest way to start the assistant:
  python run.py

This is a thin wrapper around app/main.py that sets the Python path
correctly so you don't need to install the package.
"""

import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()
