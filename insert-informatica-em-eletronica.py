import pandas as pd
import os

# Lê as planilhas de Informática e Eletrônica
informatica_df = pd.read_excel('Informatica.xlsx')
eletronica_df = pd.read_excel('Electronica.xlsx')

# Insere o conteúdo de Informática dentro de Eletrônica
combined_df = pd.concat([eletronica_df, informatica_df], ignore_index=True)

# Remove SKUs duplicados (assumindo que a primeira coluna é o SKU)
combined_df.drop_duplicates(subset=combined_df.columns[0], inplace=True)

# Salva o resultado na planilha Eletronica.xlsx
combined_df.to_excel('Electronica.xlsx', index=False)

# Deleta a planilha Informatica.xlsx
os.remove('Informatica.xlsx')

print("Conteúdo de Informática inserido em Eletrônica, SKUs duplicados removidos e planilha Informática deletada com sucesso!")
