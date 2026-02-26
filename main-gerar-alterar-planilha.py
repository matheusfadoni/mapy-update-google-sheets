#!/usr/local/bin/python3

import os
import sys
import subprocess
from datetime import datetime
import time
import traceback

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

# Remove o arquivo antigo antes de gerar um novo
produtos_path = os.path.join(diretorio, "Produtos.xlsx")
try:
    os.remove(produtos_path)
    print(f"Removido arquivo antigo: {produtos_path}")
except FileNotFoundError:
    print(f"Nenhum arquivo antigo para remover: {produtos_path}")

# Função para executar arquivo Python
def executar_arquivo(script):
    try:
        print(f"Executando: {script}")
        subprocess.run(["python3", os.path.join(diretorio, script)], check=True, cwd=diretorio)
        print(f"{script} executado com sucesso.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {script}: {e}")
        print(f"Detalhes: script={script} returncode={e.returncode} cmd={e.cmd}")
        traceback.print_exc()
        return False

# Ordem de execução dos scripts
scripts_para_executar = [
    "gerar-planilha.py",      # Gera a planilha
    "atualizar-planilha.py",   # Atualiza no Google Sheets do Mapy (para tradução de produtos em Português)
    "atualizar-planilha-neuralgenius.py"  # Atualiza no Google Sheets da NeuralGenius
]

# Executar os scripts na ordem
falhas = []
for script in scripts_para_executar:
    if not executar_arquivo(script):
        falhas.append(script)

if falhas:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] main-gerar-alterar-planilha.py finalizado COM ERROS")
    print(f"Scripts com erro: {', '.join(falhas)}\n")
else:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] main-gerar-alterar-planilha.py executado\n")
print("_________________________")
log_file.close()
