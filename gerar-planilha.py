import oracledb
import pandas as pd
import re

# Conexão Oracle
db_host = "ip-do-servidor"
db_port = 12345
db_user = "user"
db_pass = "password"
db_database = "db_name"

# Montar manualmente o DSN
dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={db_host})(PORT={db_port}))(CONNECT_DATA=(SERVICE_NAME={db_database})))"

def remover_caracteres_invalidos(valor):
    if isinstance(valor, str):
        return re.sub(r'[\x00-\x1F\x7F]', '', valor)
    return valor

def buscar_dados_categoria(categoria):
    connection = oracledb.connect(user=db_user, password=db_pass, dsn=dsn)
    cursor = connection.cursor()
    query = f"""
        SELECT COD_ARTICULO, DESCRIPCION, PRECO, CATEGORIA, SUBCATEGORIA, MARCA
        FROM MV_PRODUCTOS
        WHERE UPPER(CATEGORIA) = UPPER('{categoria}')
    """
    cursor.execute(query)
    colunas = [col[0] for col in cursor.description]
    resultados = cursor.fetchall()
    connection.close()
    resultados_limpados = [[remover_caracteres_invalidos(celula) for celula in linha] for linha in resultados]
    return pd.DataFrame(resultados_limpados, columns=colunas)

# Categorias a buscar
categorias = [
    "CASA/COCINA",
    "DEPORTES",
    "COMESTIBLES",
    "MODA ROPA Y ACCES.",
    "NIÑOS",
    "INFORMATICA",
    "CAMPING/PESCA/FERR/JARD/AUTO",
    "PERFUMERIA",
    "BEBIDAS",
    "ELECTRONICA",
    "COSMETICOS SALUD E HIG."
]

# Junta todas em um único DataFrame
df_total = pd.DataFrame()
for cat in categorias:
    df_total = pd.concat([df_total, buscar_dados_categoria(cat)], ignore_index=True)

# Remove duplicados por SKU
df_total.drop_duplicates(subset='COD_ARTICULO', inplace=True)

# Salva em uma única planilha
df_total.to_excel("Produtos.xlsx", index=False)
print("Planilha única 'Produtos.xlsx' gerada com sucesso.")
