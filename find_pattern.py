import re
import random

# Função para adicionar um número aleatório entre 1 e 60 na segunda vírgula
def adicionar_numero_aleatorio(linha):
    # Encontrar a posição da primeira vírgula dupla (,,)
    pos = linha.find(',,')
    if pos != -1:
        # Gerar um número aleatório entre 1 e 60
        numero_aleatorio = random.randint(1, 60)
        # Inserir o número aleatório logo após a primeira vírgula dupla
        linha = linha[:pos+2] + str(numero_aleatorio) + ',' + linha[pos+2:]
    return linha

# Lendo o arquivo de entrada 'resultado.txt'
with open('resultado.txt', 'r') as arquivo_entrada:
    linhas = arquivo_entrada.readlines()

# Expressão regular para encontrar linhas com o formato esperado
expressao = r'^\d+,,\d+,\d+,\d+,\d+,\d+.*$'

# Lista para armazenar as linhas filtradas e modificadas
linhas_modificadas = []

for linha in linhas:
    if re.match(expressao, linha):
        linha_modificada = adicionar_numero_aleatorio(linha)
        linhas_modificadas.append(linha_modificada)

# Gravando as linhas modificadas no arquivo de saída 'resultado_modificado.csv'
with open('resultado_modificado.csv', 'w') as arquivo_saida:
    arquivo_saida.writelines(linhas_modificadas)

print("Arquivo 'resultado_modificado.csv' criado com sucesso.")
