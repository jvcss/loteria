import csv

def remover_linhas_duplicadas(input_file, output_file):
    # Abrir o arquivo CSV de entrada
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Lista para armazenar as linhas sem duplicatas
        unique_rows = set()
        
        # Nome das colunas de interesse
        columns = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
        
        # Ler as linhas e processar
        for row in reader:
            # Ordenar os valores das bolas para garantir que a ordem não importe
            bolas_sorted = tuple(sorted([row[col] for col in columns]))
            
            # Adicionar a tupla ao conjunto (set) para garantir que não haja duplicatas
            unique_rows.add(bolas_sorted)
    
    # Escrever as linhas únicas no arquivo de saída
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = columns
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Escrever o cabeçalho
        writer.writeheader()
        
        # Escrever as linhas únicas no arquivo
        for bolas_sorted in unique_rows:
            # Criar um dicionário a partir da tupla ordenada
            row_dict = {columns[i]: bolas_sorted[i] for i in range(len(columns))}
            writer.writerow(row_dict)

# Exemplo de uso
input_file = 'resultado.csv'  # Substitua pelo nome do seu arquivo de entrada
output_file = 'saida.csv'    # Substitua pelo nome do seu arquivo de saída

remover_linhas_duplicadas(input_file, output_file)
