import os
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuracoes da API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials-automacao-atendimento-zendesk.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# IDs das planilhas no Google Sheets para cada setor
spreadsheet_ids = {
    'BEBIDAS': '1Tvi73W85NpqbRFxhMQWlq2_-D1d3PAp1KZ2Iej6alk4',
    'CAMPING': '1cCaViGYU_027Pl3z2j2ThKCCj6wGlbxEtxZQzvrUfUQ',
    'CASA COCINA': '1l-vEHPwAu0JcLDcbaxaarIr-XwQua-JlZlgtMpWYOno',
    'COMESTIBLES': '1t3aYnWKok0G4A_GtwYSaZ007WUozflDkkqmCTptKCPY',
    'COSMETICOS': '1KaWVLm1J-s13XXdjsYvFxEW1NynV1PirxVyPTTRPujI',
    'DEPORTES': '1Kzyy5ZOMuyXWKVtlchroEHsFRVz0TLEhQfwqpyvw5G0',
    'ELECTRONICA': '14KnaCb9D9SeCU-imtKk36IUaTPC4slbHeDtQdpv8HvI',
    'MODAS': '1drlVmNLKGP-oe6jIUkSecv29GF5fJoFUvnanqQ0yi60',
    'NINOS': '1tsWjoz1wrTzF3eqrIIAMp4EpDkxqQ4XZBYarZfA8Qo4',
    'PERFUMERIA': '1Vt7Q9Qy9djHhVYhIZa64JMfJf3bnqatMJxx-2_NJqfo'
}

# Funcao para limpar o conteudo de uma planilha no Google Sheets
def limpar_planilha(sheet_id):
    try:
        service.spreadsheets().values().clear(
            spreadsheetId=sheet_id,
            range="Hoja 1"  # Define a aba e a faixa de células a serem limpas
        ).execute()
    except HttpError as e:
        print(f"Erro ao limpar a planilha: {e}")

# Funcao para carregar os dados de uma planilha Excel local e subir para o Google Sheets
def upload_to_google_sheets(filename, sheet_id):
    try:
        # Verifica se o arquivo local existe antes de limpar a planilha no Google Sheets
        if os.path.exists(filename):
            # Lê o arquivo Excel
            df = pd.read_excel(filename, engine='openpyxl')

            # Substituir valores NaN por strings vazias
            df = df.fillna('')

            # Converte o DataFrame para uma lista de listas (necessário para a API do Google Sheets)
            data = df.values.tolist()

            # Limpa a planilha existente no Google Sheets
            limpar_planilha(sheet_id)

            # Faz upload dos dados
            body = {
                'values': data
            }

            service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range="Hoja 1",
                valueInputOption="RAW",
                body=body
            ).execute()
        else:
            print(f"--------> Arquivo {filename} nao encontrado <--------- Nada sera feito!")
    except HttpError as e:
        print(f"Erro ao subir para Google Sheets: {e}")
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo {filename}: {e}")

# Diretorio onde estao as planilhas Excel
diretorio = "./"

# Mapeamento de nomes de arquivos para setores no Google Sheets
arquivos_planilhas = {
    'Bebidas.xlsx': 'BEBIDAS',
    'Camping.xlsx': 'CAMPING',
    'Casa Cocina.xlsx': 'CASA COCINA',
    'Comestibles.xlsx': 'COMESTIBLES',
    'Cosmeticos.xlsx': 'COSMETICOS',
    'Deportes.xlsx': 'DEPORTES',
    'Electronica.xlsx': 'ELECTRONICA',
    'Modas.xlsx': 'MODAS',
    'Ninos.xlsx': 'NINOS',
    'Perfumeria.xlsx': 'PERFUMERIA'
}

# Itera sobre os arquivos locais e faz o upload para a respectiva planilha no Google Sheets
for arquivo, setor in arquivos_planilhas.items():
    caminho_arquivo = os.path.join(diretorio, arquivo)
    if os.path.exists(caminho_arquivo):
        print(f"Limpando planilha e fazendo upload de {arquivo} para o setor {setor}...")
        upload_to_google_sheets(caminho_arquivo, spreadsheet_ids[setor])
        print(f"Upload de {arquivo} concluido.")
    else:
        print(f"--------> Arquivo {arquivo} nao encontrado <--------- Nada sera feito!")
