#!/usr/bin/env python3
"""
Script de inicialização do Diário Inteligente
Execute este arquivo para iniciar o programa.
"""

import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa e executa o main
from src.main import main

if __name__ == "__main__":
    main()
