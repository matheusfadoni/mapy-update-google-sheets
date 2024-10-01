# -*- coding: utf-8 -*-

import os
import subprocess

# Diretorio onde estao os scripts
diretorio = "/var/www/html/planilhas-produtos-chatbot"

# Funcao para executar um arquivo Python
def executar_arquivo(script):
    try:
        print(f"Executando: {script}")
        # subprocess para rodar o script Python 3.8 no diretorio especificado
        subprocess.run(["python3.8", os.path.join(diretorio, script)], check=True)
        print(f"{script} executado com sucesso.\n")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {script}: {e}")

# Ordem de execucao dos scripts
scripts_para_executar = [
    "gerar-planilhas.py",  # Primeiro script
    "insert-informatica-em-eletronica.py",  # Segundo script
    "subir-planilhas.py"  # Terceiro script
]

# Executar os scripts na ordem
for script in scripts_para_executar:
    executar_arquivo(script)
