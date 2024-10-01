import os
import pandas as pd

# Função para listar arquivos .xlsx na pasta atual
def listar_planilhas():
    return [f for f in os.listdir() if f.endswith('.xlsx')]

# Função para juntar todas as planilhas em um único arquivo txt com colunas separadas por "|"
# garantindo que o SKU seja tratado como string e o preço tenha 2 casas decimais
def juntar_planilhas_em_txt():
    arquivos_planilhas = listar_planilhas()
    with open('produtos.txt', 'w') as arquivo_txt:
        for planilha in arquivos_planilhas:
            # Carregar a planilha
            df = pd.read_excel(planilha, dtype=str)  # Carregar tudo como string
            # Garantir que o preço tenha 2 casas decimais
            for _, row in df.iterrows():
                linha_formatada = []
                for i, item in enumerate(row):
                    if i == len(row) - 1:  # Se for a última coluna (preço)
                        try:
                            # Tentar formatar o item como float com 2 casas decimais
                            linha_formatada.append(f'{float(item):.2f}')
                        except ValueError:
                            # Se não for número (por erro), adicionar como string
                            linha_formatada.append(str(item).strip())
                    else:
                        linha_formatada.append(str(item).strip())  # Garantir que o restante seja string
                # Juntar os itens com "|"
                arquivo_txt.write(' | '.join(linha_formatada) + '\n')
    print('Planilhas unidas com sucesso no arquivo produtos.txt')

# Executar a função
juntar_planilhas_em_txt()
