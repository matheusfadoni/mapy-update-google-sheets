#!/usr/local/bin/python3

import os
import sys
import subprocess
from datetime import datetime
import time

# Define timezone correto (-03:00)
os.environ['TZ'] = 'America/Asuncion'
time.tzset()

# Redireciona stdout e stderr para o log
log_path = "/app/planilhas-chatbot.log"
log_file = open(log_path, "a")
sys.stdout = log_file
sys.stderr = log_file

print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Início da execução do main-gerar-alterar-planilha.py")

# Diretório onde estão os scripts
diretorio = "/app"

# Função para executar um arquivo Python
def executar_arquivo(script):
    try:
        print(f"Executando: {script}")
        subprocess.run(["python3", os.path.join(diretorio, script)], check=True)
        print(f"{script} executado com sucesso.\n")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {script}: {e}")

# Ordem de execução dos scripts
scripts_para_executar = [
    "gerar-planilha.py",      # Gera a planilha
    "atualizar-planilha.py",   # Atualiza no Google Sheets do Mapy (para tradução de produtos em Português)
    "atualizar-planilha-neuralgenius.py"  # Atualiza no Google Sheets da NeuralGenius
]

# Executar os scripts na ordem
for script in scripts_para_executar:
    executar_arquivo(script)

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] main-gerar-alterar-planilha.py executado\n")
print("_________________________")
log_file.close()
