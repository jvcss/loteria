import csv
from collections import Counter
import os
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
# Inicializa o colorama para suportar cores no Windows
init(autoreset=True)

def plot_acertos_por_categoria(count_data, title="Total de Acertos por Categoria"):
    """
    Plota um gráfico de barras para representar o total de acertos por categoria.
    
    :param count_data: Um objeto Counter contendo os acertos e suas respectivas contagens.
    :param title: O título do gráfico.
    """
    categories = list(count_data.keys())
    totals = list(count_data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, totals, color='skyblue', edgecolor='blue')
    plt.xlabel("Número de Acertos", fontsize=12)
    plt.ylabel("Total de Sequências", fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xticks(categories)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

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

def color_sequence(sequence, search_set, color=Fore.GREEN):
    return [
        f"{color}{num}{Style.RESET_ALL}" if num in search_set else str(num)
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
    num_acertos = 3 if len(search_numbers) else 10
    for seq, match_count in results:
        if match_count >= num_acertos:
            colored_seq = color_sequence(seq, search_set)
            print(f"(Soma: {sum(seq)}) Sequência: {', '.join(colored_seq)} - Acertos: {match_count}")
        elif match_count > 1:
            colored_seq = color_sequence(seq, search_set, color=Fore.YELLOW)
            print(f"(Soma: {sum(seq)}) Sequência: {', '.join(colored_seq)} - Acertos: {match_count}")

    print(f"\nTotal de sequências com pelo menos {num_acertos} acertos: {count}")
    print(f"Total de sequências com mais de 1 acerto: {count_2}\n")
    return count_2

def compare_with_other_csv(file_path, comparison_file):
    """
    Compara as sequências do arquivo CSV com outro arquivo CSV e conta os acertos em comum.
    
    :param file_path: Caminho do arquivo CSV contendo as sequências principais
    :param comparison_file: Caminho do arquivo CSV contendo as sequências para comparação
    """
    # Lê as sequências dos dois arquivos
    main_sequences = read_csv(file_path)
    comparison_sequences = read_csv(comparison_file)
    
    # Realiza a comparação entre as sequências dos dois arquivos
    comparison_results = []
    for main_seq in main_sequences:
        for compare_seq in comparison_sequences:
            match_count = len(set(main_seq).intersection(compare_seq))
            if match_count > 0:
                comparison_results.append((main_seq, compare_seq, match_count))
    
    comparison_results.sort(key=lambda x: x[2], reverse=True)
    
    # Exibe os resultados
    print("\nResultados da comparação entre os dois CSVs:")
    for main_seq, compare_seq, match_count in comparison_results:
        colored_main_seq = color_sequence(main_seq, set(main_seq))
        colored_compare_seq = color_sequence(compare_seq, set(compare_seq), color=Fore.YELLOW)
        print(f"Sequência principal: {', '.join(colored_main_seq)} - Comparada com: {', '.join(colored_compare_seq)} - Acertos: {match_count}")

    return comparison_results

if __name__ == "__main__":
    res = "resultado.csv"
    result = "resultado_modificado.csv"
    mega = "Mega-Sena.csv"
    resultados_gerados_por_ia = "resultado_modificado.csv"  # Nome do arquivo CSV
    training_data = "training_data.csv"
    evaluation_data = "evaluation_data.csv"

    # Comparar o arquivo 'resultado.csv' com 'Mega-Sena.csv'
    comparison_results = compare_with_other_csv(res, mega)
    
    # Caso queira realizar uma análise de acertos após a comparação
    # plot_acertos_por_categoria(todos_resultados, title="Distribuição de Acertos")
