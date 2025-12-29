import re


def read_input_file(file_path):
    """Lê arquivo e retorna conjunto de tuplas de números"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # Converte cada linha em tupla de números para comparação
    number_sets = set()
    for line in lines:
        # Remove espaços e quebras de linha
        clean_line = line.strip()
        if clean_line:
            # Converte string "1,2,3" em tupla (1,2,3)
            numbers = tuple(int(num.strip()) for num in clean_line.split(','))
            number_sets.add(numbers)
    return number_sets

result = read_input_file('resultado.csv')
evaluation_data = read_input_file('evaluation_data.csv')
training_data = read_input_file('training_data.csv')

# Valores que existem nos três arquivos (interseção)
common_in_all = result & evaluation_data & training_data
print(f"Valores presentes nos 3 arquivos ({len(common_in_all)}):")
for numbers in sorted(common_in_all):
    print(','.join(map(str, numbers)))

# Valores de result que também estão em evaluation_data
in_eval = result & evaluation_data
print(f"\nValores de result presentes em evaluation_data ({len(in_eval)}):")
for numbers in sorted(in_eval):
    print(','.join(map(str, numbers)))

# Valores de result que também estão em training_data
in_train = result & training_data
print(f"\nValores de result presentes em training_data ({len(in_train)}):")
for numbers in sorted(in_train):
    print(','.join(map(str, numbers)))

# Valores únicos de result (que não aparecem nos outros)
unique_result = result - evaluation_data - training_data
print(f"\nValores únicos em result ({len(unique_result)}):")
for numbers in sorted(unique_result):
    print(','.join(map(str, numbers)))