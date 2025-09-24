import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURAÇÃO DA API GOOGLE SHEETS ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(
    '/app/credentials-automacao-atendimento-zendesk.json',
    scopes=SCOPES
)
service = build('sheets', 'v4', credentials=creds)

spreadsheet_id = '1sbQasVfVH2cEhUHL4mNRATKOsveEKtmlgICK9C5Ku2w'
sheet_name = 'Hoja 1'
range_leitura = f"{sheet_name}!A2:C"  # Apenas A–C (COD_ARTICULO, DESCRIPCION, PRECO)

try:
    # --- 1) LÊ PLANILHA LOCAL ---
    # Lê arquivo Excel local e garante que não haja NaN
    df_local = pd.read_excel('/app/Produtos.xlsx', engine='openpyxl').fillna('')
    # Mantém apenas colunas relevantes
    df_local = df_local[['COD_ARTICULO', 'DESCRIPCION', 'PRECO', 'CATEGORIA', 'SUBCATEGORIA', 'MARCA']]
    df_local = df_local.astype(str)

    # --- 2) LÊ PLANILHA ONLINE ---
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_leitura
    ).execute()
    valores = result.get('values', [])
    # Garante que cada linha tenha pelo menos 3 colunas (A–C)
    for i in range(len(valores)):
        while len(valores[i]) < 3:
            valores[i].append('')
    df_google = pd.DataFrame(valores, columns=['COD_ARTICULO', 'DESCRIPCION', 'PRECO']).astype(str)

    # --- 3) ATUALIZA PREÇOS EXISTENTES ---
    # Junta local e Google pela chave COD_ARTICULO
    df_merged = pd.merge(
        df_google, df_local,
        on='COD_ARTICULO', how='inner',
        suffixes=('_google', '_local')
    )
    # Filtra apenas os que têm preço diferente
    df_merged = df_merged[df_merged['PRECO_google'] != df_merged['PRECO_local']]
    df_merged['PRECO'] = df_merged['PRECO_local']
    df_merged = df_merged[['COD_ARTICULO', 'PRECO']]

    # Prepara requests de atualização em lote
    updates = []
    for _, row in df_merged.iterrows():
        linha_google = df_google.index[df_google['COD_ARTICULO'] == row['COD_ARTICULO']]
        linha = int(linha_google[0]) + 2  # +2 para compensar o cabeçalho
        updates.append({
            "range": f"{sheet_name}!C{linha}",
            "values": [[row['PRECO']]]
        })

    # Envia atualização apenas se houver preços modificados
    if updates:
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"valueInputOption": "RAW", "data": updates}
        ).execute()

    # --- 4) INSERE NOVOS PRODUTOS ---
    novos = df_local[~df_local['COD_ARTICULO'].isin(df_google['COD_ARTICULO'])].copy()

    if not novos.empty:
        # Preenche valores default para colunas extras (mantém checkbox intacto)
        novos['CORRIGIDO_IA'] = 'FALSE'
        novos['REVISADO'] = 'FALSE'
        novos['DESCRIPCION_ANTIGA'] = novos['DESCRIPCION']

        # Prepara payload para inserção
        valores_novos = novos[['COD_ARTICULO', 'DESCRIPCION', 'PRECO',
                               'CATEGORIA', 'SUBCATEGORIA', 'MARCA',
                               'CORRIGIDO_IA', 'REVISADO', 'DESCRIPCION_ANTIGA']].values.tolist()

        # Faz append de novas linhas no Google Sheets
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:I",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={'values': valores_novos}
        ).execute()

    # --- 5) REMOVE PRODUTOS INEXISTENTES ---
    linhas_remover = df_google.index[~df_google['COD_ARTICULO'].isin(df_local['COD_ARTICULO'])].tolist()
    linhas_remover = [linha + 2 for linha in linhas_remover]  # +2 para compensar cabeçalho

    if linhas_remover:
        # Cria requests de exclusão de linhas em ordem reversa (de baixo para cima)
        requests = [{
            "deleteDimension": {
                "range": {
                    "sheetId": 0,
                    "dimension": "ROWS",
                    "startIndex": linha - 1,
                    "endIndex": linha
                }
            }
        } for linha in sorted(linhas_remover, reverse=True)]

        # Executa batchUpdate para remover todas as linhas de uma vez
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests}
        ).execute()

    print("Google Sheets actualizado con éxito.")

except HttpError as e:
    print(f"Error Google API: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
