import cx_Oracle
import pandas as pd
import re

# Configurações de conexão ao Oracle
from acesso_oracle import db_host, db_port, db_user, db_pass, db_database

# String de conexão
dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_database)

# Função para remover caracteres inválidos
def remover_caracteres_invalidos(valor):
    if isinstance(valor, str):
        # Remover todos os caracteres de controle ASCII, como \x02
        return re.sub(r'[\x00-\x1F\x7F]', '', valor)
    return valor

# Função para executar a query e salvar a planilha
def gerar_planilha_por_categoria(categoria, nome_arquivo):
    try:
        # Conectar ao banco de dados
        connection = cx_Oracle.connect(user=db_user, password=db_pass, dsn=dsn)
        print(f"Conectado ao banco para a categoria: {categoria}")

        # Criar um cursor
        cursor = connection.cursor()

        # Query para buscar os dados da categoria
        query = f"""
        SELECT COD_ARTICULO, DESCRIPCION, PRECO
        FROM MV_PRODUCTOS
        WHERE UPPER(CATEGORIA) = UPPER('{categoria}')
        """

        # Executar a query
        cursor.execute(query)

        # Obter os resultados e transformar em DataFrame
        colunas = [col[0] for col in cursor.description]
        resultados = cursor.fetchall()

        # Limpar os dados removendo caracteres inválidos
        resultados_limpados = [[remover_caracteres_invalidos(celula) for celula in linha] for linha in resultados]

        # Transformar em DataFrame
        df = pd.DataFrame(resultados_limpados, columns=colunas)

        # Salvar DataFrame em uma planilha Excel
        df.to_excel(f"{nome_arquivo}", index=False)
        print(f"Planilha '{nome_arquivo}' gerada com sucesso.")

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao conectar ou executar query: {e}")
    finally:
        if connection:
            connection.close()

# Dicionário mapeando as categorias do banco de dados aos nomes dos arquivos Excel
categorias_planilhas = {
    "CASA/COCINA": "Casa Cocina.xlsx",
    "DEPORTES": "Deportes.xlsx",
    "COMESTIBLES": "Comestibles.xlsx",
    "MODA ROPA Y ACCES.": "Modas.xlsx",
    "NIÑOS": "Ninos.xlsx",
    "INFORMATICA": "Informatica.xlsx",
    "CAMPING/PESCA/FERR/JARD/AUTO": "Camping.xlsx",
    "PERFUMERIA": "Perfumeria.xlsx",
    "BEBIDAS": "Bebidas.xlsx",
    "ELECTRONICA": "Electronica.xlsx",
    "COSMETICOS SALUD E HIG.": "Cosmeticos.xlsx"
}

# Gerar as planilhas para cada categoria
for categoria, nome_arquivo in categorias_planilhas.items():
    gerar_planilha_por_categoria(categoria, nome_arquivo)
