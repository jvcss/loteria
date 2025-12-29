import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from itertools import combinations
import random

# Carrega dados de treinamento e avaliação
def load_lottery_data(file_path):
    """Carrega jogos da loteria do arquivo"""
    games = []
    with open(file_path, 'r') as f:
        for line in f:
            numbers = [int(n.strip()) for n in line.strip().split(',')]
            games.append(sorted(numbers))
    return games

training_games = load_lottery_data("training_data.csv")
evaluation_games = load_lottery_data("evaluation_data.csv")

# Extrai features: frequência, pares, ímpares, distribuição por dezena
def extract_features(games, num_range=60):
    """Extrai características estatísticas dos jogos"""
    frequency = np.zeros(num_range + 1)
    pair_frequency = {}
    
    for game in games:
        for num in game:
            frequency[num] += 1
        
        # Conta frequência de pares
        for pair in combinations(game, 2):
            pair_frequency[pair] = pair_frequency.get(pair, 0) + 1
    
    return frequency, pair_frequency

freq_train, pairs_train = extract_features(training_games)
freq_eval, pairs_eval = extract_features(evaluation_games)

# Gera candidatos baseados em padrões aprendidos
def generate_candidates(frequency, pair_freq, num_games=100, num_size=6, num_range=60):
    """Gera jogos candidatos usando distribuição de probabilidade"""
    # Normaliza frequências para probabilidades
    prob = frequency[1:] / np.sum(frequency[1:])
    
    candidates = []
    for _ in range(num_games):
        # Seleciona números com probabilidade proporcional à frequência
        selected = set()
        
        while len(selected) < num_size:
            num = np.random.choice(range(1, num_range + 1), p=prob)
            selected.add(num)
        
        candidates.append(sorted(list(selected)))
    
    return candidates

# Avalia candidatos comparando com jogos reais
def evaluate_candidate(candidate, real_games):
    """Calcula score de acerto do candidato contra jogos reais"""
    scores = []
    candidate_set = set(candidate)
    
    for game in real_games:
        # Conta quantos números em comum
        matches = len(candidate_set & set(game))
        scores.append(matches)
    
    # Retorna média e máximo de acertos
    return np.mean(scores), max(scores), scores

# Gera e avalia candidatos
print("Gerando candidatos baseados em padrões de treinamento...\n")
candidates = generate_candidates(freq_train, pairs_train, num_games=1000)

# Avalia cada candidato
results = []
for candidate in candidates:
    avg_train, max_train, _ = evaluate_candidate(candidate, training_games)
    avg_eval, max_eval, _ = evaluate_candidate(candidate, evaluation_games)
    
    # Score combinado (média de acertos em ambos os conjuntos)
    combined_score = (avg_train + avg_eval) / 2
    
    results.append({
        'game': candidate,
        'avg_train': avg_train,
        'max_train': max_train,
        'avg_eval': avg_eval,
        'max_eval': max_eval,
        'combined': combined_score
    })

# Ordena por melhor performance combinada
results.sort(key=lambda x: x['combined'], reverse=True)

# Mostra os top 10 melhores candidatos
print("=" * 80)
print("TOP 10 JOGOS COM MAIOR ACERTABILIDADE")
print("=" * 80)

for i, result in enumerate(results[:10], 1):
    game_str = ','.join(map(str, result['game']))
    print(f"\n#{i}: {game_str}")
    print(f"  Média de acertos (treino):    {result['avg_train']:.2f} números")
    print(f"  Máximo de acertos (treino):   {result['max_train']} números")
    print(f"  Média de acertos (avaliação): {result['avg_eval']:.2f} números")
    print(f"  Máximo de acertos (avaliação):{result['max_eval']} números")
    print(f"  Score combinado:              {result['combined']:.2f}")

# Análise de frequência dos números mais presentes nos top candidatos
print("\n" + "=" * 80)
print("ANÁLISE DE FREQUÊNCIA NOS TOP 50 CANDIDATOS")
print("=" * 80)

top_numbers_freq = {}
for result in results[:50]:
    for num in result['game']:
        top_numbers_freq[num] = top_numbers_freq.get(num, 0) + 1

sorted_freq = sorted(top_numbers_freq.items(), key=lambda x: x[1], reverse=True)
print("\nNúmeros mais frequentes nos melhores jogos:")
for num, freq in sorted_freq[:15]:
    print(f"  Número {num:2d}: aparece em {freq} dos top 50 jogos")