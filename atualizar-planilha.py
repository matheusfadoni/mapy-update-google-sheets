import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuración de la API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(
    '/app/credentials-automacao-atendimento-zendesk.json',
    scopes=SCOPES
)
service = build('sheets', 'v4', credentials=creds)

spreadsheet_id = '1sbQasVfVH2cEhUHL4mNRATKOsveEKtmlgICK9C5Ku2w'
sheet_name = 'Hoja 1'
range_leitura = f"{sheet_name}!A2:C"

try:
    # Lee la planilla local
    df_local = pd.read_excel('/app/Produtos.xlsx', engine='openpyxl').fillna('')
    df_local = df_local[['COD_ARTICULO', 'DESCRIPCION', 'PRECO', 'CATEGORIA', 'SUBCATEGORIA', 'MARCA']]
    df_local = df_local.astype(str)

    # Lee datos actuales de Google Sheets (solo A-C)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_leitura
    ).execute()
    valores = result.get('values', [])
    for i in range(len(valores)):
        while len(valores[i]) < 3:
            valores[i].append('')
    df_google = pd.DataFrame(valores, columns=['COD_ARTICULO', 'DESCRIPCION', 'PRECO']).astype(str)

    # Atualiza preços apenas onde houve mudança
    df_merged = pd.merge(
        df_google, df_local,
        on='COD_ARTICULO', how='inner',
        suffixes=('_google', '_local')
    )
    df_merged = df_merged[df_merged['PRECO_google'] != df_merged['PRECO_local']]
    df_merged['PRECO'] = df_merged['PRECO_local']
    df_merged = df_merged[['COD_ARTICULO', 'PRECO', 'DESCRIPCION_local']]

    # Atualiza preços com batchUpdate
    updates = []
    for _, row in df_merged.iterrows():
        cod_articulo = row['COD_ARTICULO']
        linha_google = df_google.index[df_google['COD_ARTICULO'] == cod_articulo]
        linha = int(linha_google[0]) + 2  # +2 por causa do cabeçalho
        preco_novo = row['PRECO']
        updates.append({
            "range": f"{sheet_name}!C{linha}",
            "values": [[preco_novo]]
        })

    if updates:
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "RAW",
                "data": updates
            }
        ).execute()

    # Filtra produtos novos
    novos = df_local[~df_local['COD_ARTICULO'].isin(df_google['COD_ARTICULO'])].copy()

    # Preenche colunas extras direto no DataFrame
    novos['CORRIGIDO_IA'] = False
    novos['REVISADO'] = False

    # Duplica a descrição para a coluna I
    novos['DESCRIPCION_ANTIGA'] = novos['DESCRIPCION']

    # Prepara os dados nas colunas A–F e I (pulando G e H)
    valores_novos = novos[['COD_ARTICULO', 'DESCRIPCION', 'PRECO', 'CATEGORIA', 'SUBCATEGORIA', 'MARCA', 'CORRIGIDO_IA', 'REVISADO', 'DESCRIPCION_ANTIGA']].values.tolist()

    # Insere no Google Sheets
    if valores_novos:
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:I",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={'values': valores_novos}
        ).execute()


    # Remove linhas de produtos que não estão mais no Excel
    linhas_remover = df_google.index[~df_google['COD_ARTICULO'].isin(df_local['COD_ARTICULO'])].tolist()
    linhas_remover = [linha + 2 for linha in linhas_remover]  # +2 por causa do cabeçalho

    requests = []
    for linha in sorted(linhas_remover, reverse=True):
        requests.append({
            "deleteDimension": {
                "range": {
                    "sheetId": 0,
                    "dimension": "ROWS",
                    "startIndex": linha - 1,
                    "endIndex": linha
                }
            }
        })

    if requests:
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests}
        ).execute()

    print("Google Sheets actualizado con éxito.")

except HttpError as e:
    print(f"Error Google API: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
