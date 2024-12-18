import csv
from collections import Counter
import os

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Ignora o cabeçalho
        next(reader)
        data = [list(map(int, row)) for row in reader]
    return data

def search_sequences(sequences, search_numbers):
    results = []
    search_set = set(search_numbers)
    for seq in sequences:
        match_count = len(search_set.intersection(seq))
        if match_count > 0:
            results.append((seq, match_count))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def main(arg_out_number, arg_out_file, arg_out_search: str):
    """
    arg_out_number: Número mínimo de acertos para exibir a sequência
    arg_out_file: "C:\\Users\\vitim\\tutorial\\resultado_mega.csv"
        description: Caminho do arquivo CSV com as sequências
    arg_out_search: "3,9,18,54,59,60"
        description: Números a serem pesquisados nas sequências
    """
    file_path = arg_out_file
    search_numbers = list(map(int, arg_out_search.split(",")))
    sequences = read_csv(file_path)[1:] # Ignora o cabeçalho
    results = search_sequences(sequences, search_numbers)

    start_win_number =  0
    if len(search_numbers ) == 6:
           start_win_number = 3 
    elif len(search_numbers ) == 15:
        start_win_number = 11
    count = Counter([match_count for _, match_count in results if match_count >= 3])
    count_2 = Counter([match_count for _, match_count in results if match_count > 1])
    for seq, match_count in results:
        if match_count >= arg_out_number:
            print(f"( {sum(seq)} ) Sequência: {seq} - Contagem de Acertos: {match_count}")
            continue

    print(f"\nTotal de sequências com acertos: \t{count.__str__()}")
    print(f"Total de sequências com acertos de tudo: \t{count_2.__str__()}\n")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    resultados_gerados_por_ia = "resultado.csv"
    main(6, resultados_gerados_por_ia, "2,11,21,30,35,52")