import csv
from collections import Counter
import os
from colorama import Fore, Style, init
# Inicializa o colorama para suportar cores no Windows
init(autoreset=True)
# Para cores no terminal
class Color:
    GREEN = '\033[92m'
    RESET = '\033[0m'

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignora o cabeçalho
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

def color_sequence(sequence, search_set):
    return [
        f"{Fore.GREEN}{num}{Style.RESET_ALL}" if num in search_set else str(num)
        for num in sequence
    ]

def main(arg_out_number, arg_out_file, arg_out_search: str):
    """
    arg_out_number: Número mínimo de acertos para exibir a sequência
    arg_out_file: Caminho do arquivo CSV com as sequências
    arg_out_search: Números a serem pesquisados nas sequências
    """
    # Lê os números de busca e as sequências do arquivo CSV
    search_numbers = list(map(int, arg_out_search.split(",")))
    search_set = set(search_numbers)
    sequences = read_csv(arg_out_file)

    # Busca as sequências com acertos
    results = search_sequences(sequences, search_numbers)

    # Contadores de acertos
    count = Counter([match_count for _, match_count in results if match_count >= arg_out_number])
    count_2 = Counter([match_count for _, match_count in results if match_count > 1])

    print("\nResultados encontrados:")
    for seq, match_count in results:
        num_acertos = 3 if len(search_numbers) else 10
        if match_count >= num_acertos:
            colored_seq = color_sequence(seq, search_set)
            print(f"(Soma: {sum(seq)}) Sequência: {', '.join(colored_seq)} - Acertos: {match_count}")

    print(f"\nTotal de sequências com pelo menos {arg_out_number} acertos: {count}")
    print(f"Total de sequências com mais de 1 acerto: {count_2}\n")

if __name__ == "__main__":
    #os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o terminal
    resultados_gerados_por_ia = "Mega-Sena.csv"  # Nome do arquivo CSV
    main(6, resultados_gerados_por_ia, "2,4,15,28,34,39")
